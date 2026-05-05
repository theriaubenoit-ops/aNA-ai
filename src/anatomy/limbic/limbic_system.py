#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Limbic system implementation for aNA AI Project v5.3

Communicates with: 
Input: (<- Thalamus) (<- Cortical L2/3)
Input/Output: (<-> Amygdala) (<-> Hippocampus)
Output: (-> Pulse/BPM) (-> Neuromodulator Core)

Description: This module acts as the emotional and mnestic hub of aNA. It orchestrates the bidirectional flow between the Amygdala (Threat/Arousal) and the Hippocampus (Context/Memory). By integrating these signals, the Limbic System provides a value-based filter for the Thalamus and influences the global Pulse (BPM), ensuring that the organism's metabolic state is aligned with its internal emotional landscape and past experiences.

Architecture, concept and supervision: Benoit Theriault
Collaboration, research and code: Gemini
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.anatomy.limbic.amygdala import Amygdala
from src.anatomy.limbic.hippocampus import Hippocampus

class LimbicSystem:
    """
    Coordinator of the Limbic System (Amygdala & Hippocampus).
    Manages emotional valence and memory prioritization.
    """
    def __init__(self, amygdala: Amygdala = None, hippocampus: Hippocampus = None, arousal_threshold: float = 0.5):
        # Logique d'initialisation (Guard Clauses)
        self.amygdala = amygdala or Amygdala()
        self.hippocampus = hippocampus or Hippocampus()
        # C'est ici que le "Senseur de Danger" est défini :
        self.arousal_threshold = arousal_threshold 
            
    async def process_experience(self, sensory_data, emotional_input): 
        """
        Processes a sensory event and decides how to store it.
        """
        # --- SÉCURISATION DE L'INPUT ---
        # Si emotional_input est une string (ex: "Low light"), on l'encapsule
        if isinstance(emotional_input, str):
            emotional_state = {"label": emotional_input, "dopamine": 0.05, "cortisol": 0.1}
        else:
            emotional_state = emotional_input

        # 1. Extraction sécurisée (le .get() ne plantera plus)
        dopamine = emotional_state.get("dopamine", 0.0) 
        cortisol = emotional_state.get("cortisol", 0.0)
        
        # Le reste de votre logique de consolidation...
        consolidation_factor = 1.0 + (dopamine * 1.5) + (cortisol * 2.0)
        
        # 3. Envoi à l'Hippocampe (Note: vérifiez si vous utilisez 'weight' ou 'importance')
        await self.hippocampus.encode(label=sensory_data, importance=consolidation_factor, intensity=0.5)

        # 4. Calcul de l'Arousal pour le retour du test
        total_arousal = (dopamine + cortisol) / 2
        return total_arousal > self.arousal_threshold

        def trigger_flashback(self, memory_id):
            """
            Simule la ré-excitation physique de l'Amygdale par un souvenir.
            """
            # 1. Extraction de la trace depuis l'Hippocampe
            memory_trace = self.hippocampus.retrieve(memory_id)
            
            if memory_trace and "emotional_signature" in memory_trace:
                # 2. Injection directe dans la "chimie" de l'Amygdale
                signature = memory_trace["emotional_signature"]
                for neurotransmitter, intensity in signature.items():
                    self.amygdala.inject_neuromodulator(neurotransmitter, intensity)
                
                # 3. Mise à jour de l'état d'alerte global
                self.amygdala.update_internal_state()
                return True
            return False
        
        # Simulation simplifiée de l'analyse (le temps que vous codiez la suite)
        # On imagine que l'amygdale calcule un score :
        total_arousal = self.amygdala.analyze(stimulus) 

        # 1. Evaluate emotional charge (Amygdala)
        # Returns a dict of neurotransmitter impacts (cortisol, adrenaline, etc.)
        emotional_state = self.amygdala.update_activity(stimulus)
        
        # Calculate a global stress/importance score
        stress_level = emotional_state.get("cortisol", 0.0)
        excitement = emotional_state.get("adrenaline", 0.0)
        total_arousal = (stress_level + excitement) / 2

        # 2. Modulate Hippocampal Encoding
        # If arousal is high, we increase the 'weight' (importance) of the memory
        encoding_weight = 1.0 + total_arousal
        
        memory_entry = {
            "data": sensory_data,
            "emotional_stamp": emotional_state,
            "timestamp": "v5.0_cycle_now"
        }

        # The Hippocampus stores it with a priority multiplier
        self.hippocampus.encode(memory_entry, importance=encoding_weight)

        # 3. Feedback Loop
        # If arousal is too high, the Limbic System signals the Thalamus (via aNA core)
        # to focus attention only on the threat/stimulus.
        return total_arousal > self.arousal_threshold

    def trigger_recall(self, cue):
        """
        Retrieves a memory and re-activates the associated emotional state.
        """
        memory = self.hippocampus.retrieve(cue)
        if memory and "emotional_stamp" in memory:
            # Re-inject the emotion into the Amygdala for 'Empathic AI' response
            self.amygdala.apply_flashback(memory["emotional_stamp"])
        return memory