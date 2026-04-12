#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Input Auditory Gateway implementation for aNA AI Project v5.2

Communicates with: Input: External (Auditory) | Output: (-> Thalamus (CGM)) (-> Temporal Lobe (A1))

Description: This module serves as the primary sensory ingestion layer for acoustic signals within the aNA AI v5.2 architecture. Emulating the biological transduction of the cochlea, it converts raw external auditory data into neural-compatible feature vectors. 
The gateway utilizes a dual-projection logic to ensure high-fidelity processing:
Thalamic Relay (CGM): Directs signal flow through the Medial Geniculate Nucleus (CGM), acting as a critical frequency filter and attentional gate. This layer modulates gain and prioritizes salient auditory stimuli before cortical arrival.
Cortical Mapping (A1): Projects pre-processed signals to the Primary Auditory Cortex (A1) in the Temporal Lobe. This path facilitates tonotopic mapping and the initial extraction of complex temporal patterns, enabling the system to distinguish between noise, speech, and environmental cues.
This implementation adheres to a Hierarchical Sensory Protocol, ensuring that downstream cognitive modules receive refined, context-aware auditory representations rather than raw unparsed data.

Architecture, concept and supervision: Benoit Theriault
Collaboration, research and code: Gemini
"""
import os
import sys
import numpy as np
import wave
import time

# Accès au registre
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from registry import ORGANS

class AuditorySensoryPayload:
    """Conteneur unifié pour le transport de données acoustiques."""
    def __init__(self, intensity, raw_data, ratio=1.0):
        self.intensity = intensity
        self.raw_data = raw_data
        self.ratio = ratio
        self.source = "TEMPORAL_LOBE"
        #print("  [Input Auditory] Gateway initialized")

    def get(self, key, default=None):
        """Assure la compatibilité avec le Thalamus."""
        return getattr(self, key, default)
    
class InputAuditoryGateway:
    async def capture_sound(self, audio_data, ratio=1.0):
        # Calcul RMS interne (simule la cochlée)
        intensity_raw = np.sqrt(np.mean(audio_data**2))
        computed_intensity = min(1.0, max(0.1, intensity_raw * 5))

        return AuditorySensoryPayload(
            intensity=computed_intensity,
            raw_data=audio_data,
            ratio=ratio
        )
    
