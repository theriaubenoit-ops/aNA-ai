#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Thalamus implementation for aNA AI Project v5.4 - Clean Version

Communicates with:
Input: (<- Thalamic Hub: Routed sensory payloads & Gating instructions)
Input: (<- Hippocampus: Contextual memory states)
Input: (<- Amygdala: Emotional urgency & Saliency)
Input/Output: (<-> Cortical Columns L4/L6: Direct metabolic feedback)
Output: (-> Pulse/BPM: Heart rate frequency modulation)
Output: (-> Neuromodulator: Global chemical gain & ATP management)

Description: This module implements the Thalamus as the central sensory relay and rhythmic pacemaker of aNA. It orchestrates the flow between subcortical structures and the Neocortex, specifically managing the L4 excitation and L6 feedback loops. It integrates with the ChemicalCore to modulate signal gain based on arousal and directs the Pulse (BPM) frequency, ensuring the organism maintains homeostatic stability during stimulus processing.

Key Changes:
- Removed SimplifiedCorticalColumn (No more "Fake" objects).
- Integrated get_config() for all metabolic thresholds.
- Registry-dependent: Uses ORGANS for structural awareness.
- Focused on Pulse modulation and Gating logic.

Architecture, concept and supervision: Theriault Benoit
Collaboration, research and code: Google DeepMind (Gemini)
"""

import os
import sys
import asyncio
import numpy as np
from typing import Dict, Any
from unittest import result

# Alignement du path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# from src.registry import SIGNALS, ORGANS
from src.config import get_config
from src.registry import ORGANS
from src.anatomy.limbic.hippocampus import Hippocampus
from src.core.pulse import Pulse
from src.anatomy.base.neuromodulator import Neuromodulator
from src.anatomy.limbic.limbic_system import LimbicSystem
from src.anatomy.subcortical.striatum import Striatum

class Thalamus: 
    def __init__(self, *, striatum: Striatum = None, limbicsystem: LimbicSystem = None, hippocampus: Hippocampus = None, pulse: Pulse = None, neuromodulator: Neuromodulator = None):
        """
        Initialisation de l'organe central.
        """ 
        self.config = get_config()
        self.limbic_system = limbicsystem or LimbicSystem()

        self.striatum = striatum or Striatum()
        self.last_cortical_gain = 1.0
        self.total_time_saved = 0.0

        self.synaptic_atp = 1.0  # Réservoir d'énergie (100%)
        self.is_burned_out = False # État de fatigue extrême
        
        # 1. Seuils Métaboliques (config.py)
        self.base_bpm = self.config.get("THALAMUS_BASE_BPM", 72.0)
        self.max_bpm = self.config.get("THALAMUS_MAX_BPM", 150.0)
        self.atp_critical = self.config.get("ATP_CRITICAL_THRESHOLD", 0.20)
        self.decay_factor = self.config.get("THALAMUS_DECAY_FACTOR", 0.15)

        # 2. Architecture des Noyaux (registry.py)
        self.nuclei = ORGANS["THALAMUS"]["NUCLEI"]
        self.nuclei_activity = {n: 0.0 for n in self.nuclei}

        # 3. Connexions Systémiques
        # self.hippo = hippocampus
        self.hippo = hippocampus or Hippocampus()
        # self.pulse = pulse
        self.pulse = pulse or Pulse()
        # self.neurom = neuromodulator
        self.neurom = neuromodulator or Neuromodulator()
        
        self.current_bpm = self.base_bpm
        self.system_strain = 0.0
        self.is_autonomous = False

    def get_current_bpm(self, l6_feedback: float) -> float:
        """
        Calcule le rythme cardiaque basé sur le feedback cortical (L6) 
        et la chimie actuelle.
        """
        config = get_config()
        atp = self.pulse.atp
        matrix = self.neurom.get_matrix()
        nora = matrix.get("noradrenaline", 0.1)
        
        # Calcul de l'excitation vs inhibition
        strain_multiplier = 1.0 + (1.0 - atp)
        excitation = 1.0 + (nora * 2.0 * strain_multiplier)
        
        # Le feedback L6 agit comme un frein : plus on comprend, plus on se calme.
        frein = l6_feedback * config.get("L6_GAIN", 0.8)
        target_bpm = self.base_bpm * (excitation / (1.0 + frein))
        
        # Sécurités biologiques (Bradycardie / Tachycardie)
        min_allowed = config.get("BRADYCARDIA_BPM", 45.0)
        max_allowed = config.get("MAX_VIGILANCE_BPM", 200.0)
        
        self.current_bpm = max(min_allowed, min(max_allowed, target_bpm))
        return self.current_bpm

    async def process_payload(self, stimulus: Dict[str, Any], neurom: Neuromodulator, l6_feedback: float = 0.5):
        """
        Point d'entrée principal avec modulation limbique réelle.
        """
        config = get_config()

        if self.pulse.is_refractory:
            return {"status": "REFRACTORY_REST", "gain": 0.0}
        
        # Appel au Striatum pour obtenir l'autorisation (Action Selection)
        striatal_decision = self.striatum.process_selection(
            cortical_intent=l6_feedback, 
            limbic_pulse=neurom.get_matrix(),
            atp_level=self.pulse.atp
        )
        if not striatal_decision["is_allowed"]:
            return {"status": "ACTION_BLOCKED_BY_STRIATUM", "gain": 0.0}
        
        self.rtn_inhibition = self.config.get("RTN_BASE_INHIBITION") + striatal_decision["rtn_modulator"]
        
        label = stimulus.get("signal_label", "unknown")
        intensity = stimulus.get("intensity", 0.5)
        chemistry = neurom.get_matrix()

        # 1. ÉVALUATION LIMBIQUE RÉELLE (The Real Thing)
        # Le LimbicSystem traite l'expérience via l'Amygdale et l'Hippocampe
        # On passe l'intensité comme donnée sensorielle et une valence neutre par défaut
        arousal_status = await self.limbic_system.process_experience(
            sensory_data=label, 
            emotional_input={"intensity": intensity, "atp": self.pulse.atp}
        )

        # 2. MODULATION CHIMIQUE VIA L'AMYGDALE
        # On récupère les niveaux réels d'adrénaline et de cortisol produits par les noyaux
        emotional_state = self.limbic_system.amygdala.update_activity(intensity)
        
        # Injection directe dans le Neuromodulateur
        self.neurom.inject_chemicals("amygdala", {
            "norepinephrine": emotional_state["cortisol"], # Utilise 'norepinephrine' pour la cohérence !
            "dopamine": emotional_state.get("adrenaline", 0.1) 
        })

        # 3. MISE À JOUR DU PULSE
        # Le BPM est maintenant influencé par la véritable adrénaline de l'amygdale
        new_bpm = self.calculate_bpm(arousal_status)
        self.pulse.update_frequency(new_bpm)

        result = {
            "bpm": new_bpm,
            "arousal": arousal_status,
            "atp": self.pulse.atp,
            "gain": self.system_strain, # Ou votre variable de gain actuelle
            "status": "PROJECTED_TO_CORTEX"
        }
        return result
        
    def calculate_bpm(self, arousal_status: bool) -> float:
        # 1. On récupère l'ATP actuel du Pulse
        atp = self.pulse.atp 
        
        # 2. Plus l'ATP est bas, plus le coeur doit forcer (Stress métabolique)
        metabolic_stress = 1.0 + (1.0 - atp) 
        
        # 3. Si le système limbique est en alerte, on multiplie encore
        emotional_surge = 1.4 if arousal_status else 1.0
        
        return self.base_bpm * metabolic_stress * emotional_surge
    
    def apply_cortical_feedback(self, current_gain: float, l6_signal: float, config: dict) -> float:
        inhibition_strength = config.get("CORTICAL_INHIBITION", 0.8)
        target_gain = 1.0 - (l6_signal * inhibition_strength)
        
        # --- GESTION DE LA FATIGUE (ATP) ---
        if target_gain >= 0.8:
            # Stress élevé (Nouveauté constante) : Consommation d'ATP
            self.synaptic_atp -= 0.05 
        else:
            # Habituation (Calme) : Récupération d'ATP
            self.synaptic_atp += 0.02
            
        # Plafonnement de l'ATP entre 0.0 et 1.0
        self.synaptic_atp = max(0.0, min(1.0, self.synaptic_atp))
        
        # --- DÉCLENCHEMENT DU BURNOUT ---
        if self.synaptic_atp <= 0.1:
            self.is_burned_out = True # Le système lâche prise
        elif self.synaptic_atp >= 0.7:
            self.is_burned_out = False # Récupération suffisante
            
        # --- EFFET DE LA FATIGUE SUR LE GAIN ---
        if self.is_burned_out:
            # Forçage du gain à une valeur très basse pour "ignorer" le monde
            # C'est un mécanisme de défense biologique.
            target_gain = 0.15 
            
        self.last_cortical_gain = float(np.clip(target_gain, 0.1, 1.0))
        return self.last_cortical_gain
    
    def get_synaptic_latency(self) -> float:
        base_latency = self.config.get("BASE_SYNAPTIC_LATENCY", 0.5)
        
        # --- EFFET DE LA FATIGUE SUR LA VITESSE ---
        if self.is_burned_out:
            # En Burnout, le système est dans le "brouillard mental"
            # La latence explose (ex: 1.5x la base)
            current_latency = base_latency * 1.5
            saved_this_cycle = 0.0 # Aucune économie d'énergie possible
        else:
            current_latency = base_latency * self.last_cortical_gain
            saved_this_cycle = base_latency - current_latency
            
        self.total_time_saved += saved_this_cycle
        return current_latency
    
    def apply_rest_protocol(self, cycles: int = 1):
        """
        Simule une phase de repos pour reconstituer les stocks d'ATP.
        """
        recovery_rate = self.config.get("ATP_RECOVERY_RATE", 0.15) # Remboursement rapide
        
        # On recharge l'ATP
        self.synaptic_atp += (recovery_rate * cycles)
        self.synaptic_atp = min(1.0, self.synaptic_atp)
        
        # Sortie du burnout si le crédit est suffisant
        if self.synaptic_atp >= 0.8:
            self.is_burned_out = False
            
        print(f" [MÉTABOLISME] Repos en cours... ATP: {self.synaptic_atp:.2f}")

    def is_tired(self) -> bool:
        """Évalue si le crédit ATP est passé sous un seuil critique."""
        return self.synaptic_atp < 0.3 or self.is_burned_out

    def activate_low_power_mode(self):
        """
        Force un mode d'économie d'énergie.
        Réduit le gain maximum possible pour protéger les circuits.
        """
        # On bride le gain maximum à 0.4 tant qu'on est fatigué
        self.last_cortical_gain = min(self.last_cortical_gain, 0.4)
        print(" [SYSTÈME] Mode économie synaptique : Latence augmentée. ")

    def check_circadian_cycle(self, current_hour: int):
        """
        Détermine si l'organisme doit être en Éveil ou en Repos.
        Paramètres configurables (ex: 16h/8h).
        """
        start_sleep = self.config.get("CIRCADIAN_SLEEP_START", 22) # 22h
        end_sleep = self.config.get("CIRCADIAN_SLEEP_END", 6)      # 6h
        
        # Logique simple de cycle circadien
        if current_hour >= start_sleep or current_hour < end_sleep:
            self.apply_rest_protocol(cycles=1)
            return "SLEEP"
        return "AWAKE"