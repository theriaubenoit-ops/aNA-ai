#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class LimbicSystem:
    """
    Coordinates interactions between Amygdala (emotion) and Hippocampus (memory).
    Acts as a filter to prioritize memory encoding based on emotional impact.
    """
    def __init__(self, amygdala, hippocampus):
        self.amygdala = amygdala
        self.hippocampus = hippocampus
        self.arousal_threshold = 0.6  # Seuil de choc émotionnel

    def process_experience(self, stimulus, sensory_data):
        """
        Processes a sensory event and decides how to store it.
        """
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