#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Occipital Lobe implementation for aNA AI Project v5.3

Communicates with:
Input: (<- Thalamus)
Input/Output: (<-> Other Cortical Areas)
Output: (-> Motor / Pre-frontal)

Description: This module implements the Occipital Lobe with its key regions (V1-V3) for visual processing. It integrates with the ChemicalCore for neuromodulatory influences, particularly noradrenaline (Trauma) and acetylcholine (Attention). The Occipital Lobe processes visual inputs, modulates them based on the chemical state, and provides feedback to the Thalamus to regulate sensory gating.

Architecture, concept and supervision: Theriault Benoit
Collaboration, research and code: Gemini, Cline
"""

import asyncio
import numpy as np
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from typing import Dict, Any
from src.anatomy.cortical.cortical_column import CorticalColumns

class OccipitalLobe(CorticalColumns):
    def __init__(self, position: np.ndarray = None, hippo_unit=None):
        if position is None:
            position = np.array([0.0, 40.0, 0.0])
        super().__init__(position=position, hippo_unit=hippo_unit)
        self.label = "Occipital (V1)"

        if not hasattr(self, 'neurons'):
            self.neurons = [] # Ou initialise une NeuronPopulation si nécessaire

        self.label = "Occipital (V1-V3)"
        self.feedback_to_thalamus = 0.0
        self.layer4_gain = 1.2 
        
        # Simulation d'une mémoire visuelle (Templates)
        self.visual_memory = {"A": 0.95, "N": 0.80}

    async def process_visual_flow(self, stimulus_id: str, intensity: float, chemical_matrix: Dict[str, float]):
        """
        Traite le flux visuel : V1 (Entrée) -> V2 (Reconnaissance) -> L6 (Feedback).
        """
        # 1. Extraction des modulateurs (ChemicalCore)
        nora = chemical_matrix.get("noradrenaline", 0.1)
        ach = chemical_matrix.get("acetylcholine", 0.1)
        
        # 2. Gain de la Layer IV (V1) - Boosté par l'Attention
        gain_v1 = self.layer4_gain * (1.0 + ach)
        
        # 3. Niveau de reconnaissance (V2/V3)
        # On cherche si le cerveau connaît ce motif
        recognition_level = self.visual_memory.get(stimulus_id, 0.2) # 0.2 si inconnu
        
        # 4. Simulation de l'hyper-focalisation traumatique
        # Si aNA est en panique (Nora > 0.6), le signal "brûle" les couches
        if nora > 0.6:
            effective_impact = intensity * (1.0 + nora) * gain_v1
        else:
            effective_impact = intensity * recognition_level * gain_v1

        # 5. Appel à la cascade des 6 couches (L4 -> L2/3 -> L5)
        # On utilise le signal impacté pour activer les colonnes corticales
        results = await self.process_input(
            signal_data=str(effective_impact),
            hippo_unit=None 
        )
        
        # 6. Feedback L6 pour le Thalamus (Predictive Coding)
        # Plus on reconnaît, plus on calme le Thalamus (Inhibition latérale)
        self.feedback_to_thalamus = recognition_level
        
        return {
            "visual_output": effective_impact,
            "recognition_confidence": recognition_level,
            "arousal_contribution": nora * 0.2 if recognition_level < 0.5 else 0.0,
            "feedback": self.feedback_to_thalamus
        }

    def reset(self):
        """Remise à zéro des potentiels membranaires du lobe"""
        for layer in self.layers.values():
            if isinstance(layer, float):
                layer = 0.0
        self.feedback_to_thalamus = 0.0