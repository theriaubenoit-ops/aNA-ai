#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Thalamus implementation for aNA AI Project v5.3

Communicates with:
Input: (<- Thalamic Hub: Routed sensory payloads & Gating instructions)
Input: (<- Hippocampus: Contextual memory states)
Input: (<- Amygdala: Emotional urgency & Saliency)
Input/Output: (<-> Cortical Columns L4/L6: Direct metabolic feedback)
Output: (-> Pulse/BPM: Heart rate frequency modulation)
Output: (-> Neuromodulator: Global chemical gain & ATP management)

Description: This module implements the Thalamus as the central sensory relay and rhythmic pacemaker of aNA. It orchestrates the flow between subcortical structures and the Neocortex, specifically managing the L4 excitation and L6 feedback loops. It integrates with the ChemicalCore to modulate signal gain based on arousal and directs the Pulse (BPM) frequency, ensuring the organism maintains homeostatic stability during stimulus processing.

Architecture, concept and supervision: Benoit Theriault
Collaboration, research and code: Gemini, Cline
"""

import os
import sys
import asyncio
from typing import Dict, Any

# Alignement du path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# from src.registry import SIGNALS, ORGANS
from anatomy.cortical.cortical_column import SimplifiedCorticalColumn
from config import get_config
from registry import ORGANS

class Thalamus:
    def __init__(self, hippocampus, pulse, neuromodulator_core):
        """
        Initialisation unifiée.
        """
        # 1 configuration dynamique depuis le registre et le config
        config = get_config()
        self.l6_gain = config.get("L6_GAIN", 0.5)
        self.base_bpm = config.get("BASE_BPM", 120.0)
        self.atp_critical = config.get("ATP_CRITICAL_THRESHOLD", 0.20)
        self.atp_fatigue_zone = config.get("ATP_FATIGUE_ZONE", 0.40)
        self.system_strain = 0.0

        # 2 nouvelles propriétés pour la gestion de la fatigue
        thalamus_struct = ORGANS.get("THALAMUS", {})
        self.nuclei = ORGANS["THALAMUS"]["NUCLEI"]

        # 3. Initialiser les organes et l'état
        self.hippo = hippocampus
        self.pulse = pulse
        self.neurom = neuromodulator_core
        self.is_autonomous = False
        self.current_bpm = self.base_bpm
        self.nuclei_activity = {n: 0.0 for n in self.nuclei}

    def apply_cortical_feedback(self, current_signal, previous_l6, config):
        resonance = config.get("CORTICAL_RESONANCE_FACTOR", 0.5)
        # Plus la résonance est haute, plus la prédiction L6 stabilise 
        # le signal entrant, facilitant le "Known!"
        visual_column = SimplifiedCorticalColumn(column_id="COL_V1")
        dynamic_res = 0.74 - (visual_column.get_average_myelination() * 0.2) # * 0.61 Test correction temporaire (calibration du plafond "Signal L6" à 1.48 mV)
        stabilized_signal = current_signal + (previous_l6 * resonance) * dynamic_res
        return stabilized_signal

    def update_strain_level(self, usage_cycles: int, recovery_rate: float):
        """
        Calcule l'épuisement du système. 
        Plus 'strain' est haut, moins le thalamus peut filtrer les alertes.
        """
        self.system_strain = min(1.0, usage_cycles * 0.01) # Accumulation
    
    def get_current_bpm(self, l6_feedback: float) -> float:
        atp = self.pulse.atp
        nora = self.neurom.get_matrix().get("noradrenaline", 0.1)
        
        # On peut recharger la config ici si on veut que les changements 
        # du Persona Lab soient instantanés sans redémarrer
        config = get_config()
        
        system_strain = 1.0 - atp
        sensibilité = 1.0 + (system_strain * 0.5)
        excitation = 1.0 + (nora * 2.0 * sensibilité)
        
        # Utilisation du gain dynamique
        frein_efficace = l6_feedback * config["L6_GAIN"] * (1.0 - system_strain)
        
        target_bpm = config["BASE_BPM"] * (excitation / (1.0 + frein_efficace))
        
        # Sécurité biologique : Plancher dynamique
        # Si fatigue intense, on utilise BRADYCARDIA_BPM (45.0) défini en config
        min_bpm = config["BASE_BPM"] if atp > config["ATP_FATIGUE_ZONE"] else config["BRADYCARDIA_BPM"]
        if atp < config["ATP_CRITICAL_THRESHOLD"]:
            min_bpm = config["BRADYCARDIA_BPM"]
        
        self.current_bpm = max(min_bpm, min(config["MAX_VIGILANCE_BPM"], target_bpm))
        return self.current_bpm

    async def process_payload(self, stimulus: Dict[str, Any], l6_feedback: float = 0.5):
        """
        Traite le signal et ajuste le Pulse en temps réel.
        """
        # --- NOUVEAUTÉ v5.1 : VERROU DE RÉCUPÉRATION ---
        # Si le coeur est en mode réfractaire, on ferme les vannes sensorielles.
        if self.pulse.is_refractory:
            return {
                "bpm": self.pulse.bpm,
                "thalamic_gain": 0.05,
                "status": "REFRACTORY_REST"
            }
        signal_label = stimulus.get("signal_label", "unknown")
        nucleus_target = stimulus.get("nucleus", "MGN")
        intensity = stimulus.get("intensity", 0.5) # Remplacé 'payload' par 'stimulus'

        # 1. Évaluation par l'Hippocampe (Prédiction)
        # On utilise le signal_label pour vérifier si c'est déjà connu
        prediction_error = await self.hippo.evaluate_prediction(stimulus.get("signal_label", ""))        
        
        # 2. Mise à jour du ChemicalCore via l'Amygdale (Simulée ici)
        # Si erreur forte + intensité forte = Noradrénaline boost
        if prediction_error > 0.7 and intensity > 0.6:
            self.neurom.update_from_limbic({"noradrenaline": 0.8, "dopamine_boost": 0.0})
        else:
            self.neurom.update_from_limbic({"dopamine_boost": 0.1})

        # 3. Ajustement du Pulse (Le rythme de calcul)
        new_bpm = self.get_current_bpm(l6_feedback)
        self.pulse.update_frequency(new_bpm)

        # 4. Activité des noyaux pour le Dashboard
        self.nuclei_activity[nucleus_target] = intensity
        
        return {
            "bpm": new_bpm,
            "thalamic_gain": 1.0 / (1.0 + l6_feedback)
        }
    
    async def internal_consciousness_loop(self):
        """Boucle de veille autonome avec gestion homéostatique"""
        print("  [Thalamus] Autonomous consciousness activated.")
        base_target = self.config.get("THALAMUS_BASE_BPM", 72.0)
        decay_factor = self.config.get("THALAMUS_DECAY_FACTOR", 0.1)
        
        try:
            while self.is_autonomous:
                # 1. Lecture du succès cognitif via le Registre (Lien invisible)
                hippo_match = self.registry.get("last_hippo_match", 0.0)
                
                # 2. Calcul de la cible dynamique
                # On applique le drop si la reconnaissance est confirmée (> 85%)
                drop_val = self.config.get("RECOGNITION_METABOLIC_DROP", 4.0)
                current_target -= (drop_val * confidence_factor)
                if hippo_match > 50.0: # On commence à relaxer dès 50%
                    # On calcule un ratio de confiance (entre 0 et 1) pour les valeurs au-dessus de 50
                    confidence_factor = (hippo_match - 50.0) / 50.0 
                    # Le drop maximal (ex: 4) est appliqué seulement à 100% de match
                    metabolic_drop = self.config.get("RECOGNITION_METABOLIC_DROP", 4.0)
                    current_target -= (metabolic_drop * confidence_factor)

                # 3. Gestion du BPM
                if self.pulse.bpm > current_target:
                    diff = self.pulse.bpm - current_target
                    self.pulse.bpm -= diff * decay_factor
                
                # 4. Sécurité : Plafond absolu (Hard Cap)
                max_allowed = self.config.get("THALAMUS_MAX_BPM", 150.0)
                if self.pulse.bpm > max_allowed:
                    self.pulse.bpm = max_allowed
                    print(f"  [Safety] BPM capped at {max_allowed} to prevent metabolic collapse.")
                
                # 5. Rythme de la boucle influencé par la Dopamine
                matrix = self.neurom.get_matrix()
                wait_time = 2.0 / (matrix['dopamine'] + 0.5)
                
                # --- AJOUT : Mécanisme de retour au calme ---
                if self.pulse.bpm > base_target:
                    # On réduit l'écart proportionnellement pour une courbe de descente naturelle
                    diff = self.pulse.bpm - base_target
                    self.pulse.bpm -= diff * decay_factor
                # --------------------------------------------

                if matrix['noradrenaline'] < 0.3:
                    print(f"  [Auto] aNA is calm... BPM: {self.pulse.bpm:.1f}")
                else:
                    print(f"  [Auto] aNA is on alert! BPM: {self.pulse.bpm:.1f}")
                
                await asyncio.sleep(wait_time)
        except asyncio.CancelledError:
            print("  [Thalamus] Consciousness put on standby.")
