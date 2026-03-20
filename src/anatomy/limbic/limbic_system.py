#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from anatomy.limbic.amygdala import Amygdala
from anatomy.limbic.hippocampus import Hippocampus

class LimbicSystem:
    """
    Coordinator of the Limbic System (Amygdala & Hippocampus).
    Manages emotional valence and memory prioritization.
    """
    def __init__(self, amygdala: Amygdala = None, hippocampus: Hippocampus = None, arousal_threshold: float = 0.5):
        self.amygdala = amygdala or Amygdala()
        self.hippocampus = hippocampus or Hippocampus()
        # C'est ici que le "Senseur de Danger" est défini :
        self.arousal_threshold = arousal_threshold 
            
    def process_experience(self, stimulus, sensory_data):
        """
        Processes a sensory event and decides how to store it.
        """
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
