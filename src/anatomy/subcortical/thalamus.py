#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Thalamus implementation for aNA AI Project v5.3 - Clean Version

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

Architecture, concept and supervision: Benoit Theriault
Collaboration, research and code: Gemini, Cline
"""

import os
import sys
import asyncio
from typing import Dict, Any
from unittest import result

# Alignement du path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# from src.registry import SIGNALS, ORGANS
from config import get_config
from registry import ORGANS
from anatomy.limbic.hippocampus import Hippocampus
from core.pulse import Pulse
from anatomy.base.neuromodulator import Neuromodulator
from anatomy.limbic.limbic_system import LimbicSystem
from anatomy.subcortical.striatum import Striatum

class Thalamus: 
    def __init__(self, striatum: Striatum = None, limbicsystem: LimbicSystem = None, hippocampus: Hippocampus = None, pulse: Pulse = None, neuromodulator: Neuromodulator = None):
        """
        Initialisation de l'organe central.
        """ 
        self.config = get_config()
        self.limbic_system = limbicsystem or LimbicSystem()

        self.striatum = striatum or Striatum()
        
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
            "atp": self.pulse.atp, # ajout ? 
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
    
    # Pas de mock pour L6, à refaire avec cortical_column.py ! 
    def apply_cortical_feedback(self, current_gain: float, l6_signal: float, config: dict) -> float:
        """
        Simule le feedback de la couche 6 du cortex (L6) qui module l'entrée thalamique.
        """
        # On récupère le facteur d'influence depuis la config ou 0.1 par défaut
        feedback_factor = config.get("CORTICAL_FEEDBACK_STRENGTH", 0.1)
        
        # Le feedback L6 ajuste le signal : il peut l'amplifier ou le réduire
        # On simule une intégration simple : signal_actuel + (gain * influence)
        new_l6_signal = l6_signal + (current_gain * feedback_factor)
        
        return min(new_l6_signal, 1.0) # On plafonne à 1.0 pour la stabilité