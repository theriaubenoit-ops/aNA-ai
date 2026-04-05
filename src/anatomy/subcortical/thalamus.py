#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Thalamus implementation for aNA v5.1

Communicates with: 
Input: (<- InputGateway) (<- Hippocampus) (<- Amygdala)
Input/Output: (<-> Cortical Columns L4/L6) 
Output: (-> Pulse/BPM) (-> Neuromodulator Gain)

This module implements the Thalamus as the central sensory relay and rhythmic pacemaker of aNA. It orchestrates the flow between subcortical structures and the Neocortex, specifically managing the L4 excitation and L6 feedback loops. It integrates with the ChemicalCore to modulate signal gain based on arousal and directs the Pulse (BPM) frequency, ensuring the organism maintains homeostatic stability during stimulus processing.

Architecture, concept and supervision: Benoit Theriault
Collaboration, research and code: Gemini, Cline
"""

import asyncio
from typing import Dict, Any
import sys
import os

# Alignement du path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from src.registry import SIGNALS, ORGANS

class Thalamus:
    def __init__(self, hippocampus, pulse, neuromodulator_core):
        """
        Initialisation v5.1 unifiée.
        """
        self.hippo = hippocampus
        self.pulse = pulse
        self.neurom = neuromodulator_core
        self.is_autonomous = False
        
        # Configuration extraite du registre
        config = ORGANS["THALAMUS"]
        self.l6_gain = 1.2 # Force de l'inhibition corticale
        self.base_bpm = 120.0
        self.current_bpm = 120.0
        
        # État des noyaux (MGN: Médian, LGN: Latéral, RTN: Réticulaire)
        self.nuclei_activity = {n: 0.0 for n in config["NUCLEI"]}

    def update_strain_level(self, usage_cycles: int, recovery_rate: float):
        """
        Calcule l'épuisement du système. 
        Plus 'strain' est haut, moins le thalamus peut filtrer les alertes.
        """
        self.system_strain = min(1.0, usage_cycles * 0.01) # Accumulation
    
    def get_current_bpm(self, l6_feedback: float) -> float:
        # 1. On récupère l'état global (Énergie vs Stress)
        # L'ATP vient du Pulse, la Noradrénaline du ChemicalCore
        atp = self.pulse.atp
        nora = self.neurom.get_matrix().get("noradrenaline", 0.1)
        
        # 2. Calcul du 'Strain' (Tension du système)
        # Plus l'ATP est bas, plus le strain est élevé (0.0 à 1.0)
        system_strain = 1.0 - atp
        
        # 3. L'excitation brute (Nouveauté/Danger)
        # En cas de fatigue (strain haut), la sensibilité à la Noradrénaline augmente
        # Le système est "à fleur de peau"
        sensibilité = 1.0 + (system_strain * 0.5)
        excitation = 1.0 + (nora * 2.0 * sensibilité)
        
        # 4. L'inhibition corticale affaiblie par la fatigue
        # C'est ici que le "frein" lâche : si system_strain est à 0.8, 
        # l'inhibition n'est plus qu'à 20% de son efficacité.
        frein_efficace = l6_feedback * self.l6_gain * (1.0 - system_strain)
        
        # 5. Résultante : BPM
        target_bpm = self.base_bpm * (excitation / (1.0 + frein_efficace))
        
        # 6. Sécurité biologique avec "mode survie"
        # Si fatigue intense, on baisse le plancher pour forcer le repos (bradycardie protectrice)
        min_bpm = 110.0 if atp > 0.3 else 45.0 
        
        self.current_bpm = max(min_bpm, min(240.0, target_bpm))
        return self.current_bpm
    
    async def process_payload(self, stimulus, l6_feedback):
        # Sécurité Sommeil : Si le coeur bat trop lentement, on ignore l'input
        if self.pulse.bpm < 60.0:
            return {"status": "sleep_mode", "gain": 0.0, "bpm": self.pulse.bpm}

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
        """Boucle de veille autonome de William v5.1"""
        print("  [Thalamus] Autonomous consciousness activated.")
        try:
            while self.is_autonomous:
                # 1. On vérifie l'état chimique (Dopamine = Curiosité)
                matrix = self.neurom.get_matrix()
                wait_time = 2.0 / (matrix['dopamine'] + 0.5) # Plus de dopa = plus rapide
                
                # 2. Simulation d'une micro-activité interne (bruit de fond)
                if matrix['noradrenaline'] < 0.3:
                    print(f"  [Auto] aNA is calm... BPM: {self.pulse.bpm:.1f}")
                else:
                    print(f"  [Auto] aNA is on alert! BPM: {self.pulse.bpm:.1f}")
                
                await asyncio.sleep(wait_time)
        except asyncio.CancelledError:
            print("  [Thalamus] Consciousness put on standby.")
