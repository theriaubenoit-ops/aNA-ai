#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Occipital Lobe implementation for aNA AI Project v5.3

Communicates with: Input: (<- Thalamus) | Input/Output: (<-> Other Cortical Areas) | Output: (-> Motor / Pre-frontal)

Description: This module implements the Occipital Lobe with its key regions (V1-V3) for visual processing. It integrates with the ChemicalCore for neuromodulatory influences, particularly noradrenaline (Trauma) and acetylcholine (Attention). The Occipital Lobe processes visual inputs, modulates them based on the chemical state, and provides feedback to the Thalamus to regulate sensory gating.

Architecture, concept and supervision: Benoit Theriault
Collaboration, research and code: Gemini, Cline 
"""

import asyncio
import numpy as np
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from typing import Dict, Any
from anatomy.cortical.cortical_column import CorticalColumns

class OccipitalLobe(CorticalColumns):
    def __init__(self, position: np.ndarray = None):
        if position is None:
            position = np.array([0.0, 40.0, 0.0]) # Coordonnées 3D aNA
        super().__init__(position)
        
        self.label = "Occipital (V1-V3)"
        self.feedback_to_thalamus = 0.0
        
        # Spécificité V1 : Couche IV ultra-réceptive (Entrée sensorielle)
        self.layer4_gain = 1.2 

    async def process_visual_flow(self, intensity: float, chemical_matrix: Dict[str, float]):
        """
        Traite le flux visuel entrant avec modulation noradrénergique (Trauma).
        """
        # 1. Extraction des modulateurs du ChemicalCore
        # On booste la précision si William est en alerte (Noradrénaline)
        nora = chemical_matrix.get("noradrenaline", 0.1)
        ach = chemical_matrix.get("acetylcholine", 0.1)
        
        # 2. Simulation de l'hyper-focalisation traumatique
        # Si Noradrénaline > 0.6, on augmente artificiellement l'intensité perçue
        effective_intensity = intensity * (1.0 + nora) if nora > 0.6 else intensity
        
        # 3. Passage à travers la cascade des 6 couches (L4 -> L2/3 -> L5)
        # On injecte la chimie dans la Layer I (Attention)
        results = await self.process_input(
            signal_data=str(effective_intensity), # Adapté pour tes tests actuels
            hippo_unit=None # Sera lié au LimbicSystem global plus tard
        )
        
        # 4. Calcul du Feedback L6 pour le Thalamus
        # Plus on reconnaît le signal (Habituation), plus on calme le Thalamus
        self.feedback_to_thalamus = results.get("l6_feedback", 0.5)
        
        return {
            "visual_output": effective_intensity * results.get("recognition", 0.5),
            "arousal_contribution": nora * 0.2,
            "feedback": self.feedback_to_thalamus
        }

    def reset(self):
        """Remise à zéro des potentiels membranaires du lobe"""
        for layer in self.layers.values():
            if isinstance(layer, float):
                layer = 0.0
        self.feedback_to_thalamus = 0.0