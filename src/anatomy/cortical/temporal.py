#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Temporal Lobe implementation for aNA AI Project v5.3

Communicates with: Input: (<- Thalamus) | Input/Output: (<-> Other Cortical Areas) | Output: (-> Motor / Pre-frontal)

Description: This module implements the Temporal Lobe with its key regions (IT, Wernicke) for semantic processing and memory integration. It integrates with the ChemicalCore for neuromodulatory influences, particularly acetylcholine (Attention) and serotonin (Perception Stabilization). The Temporal Lobe fuses visual and spatial information to recognize objects and provides feedback to the Frontal Lobe for action planning.

Architecture, concept and supervision: Benoit Theriault
Collaboration, research and code: Gemini, Cline 
"""

import asyncio
import numpy as np
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from typing import Dict, Any
from src.anatomy.cortical.cortical_column import CorticalColumns

class TemporalLobe(CorticalColumns):
    def __init__(self, position: np.ndarray = None):
        if position is None:
            position = np.array([20.0, 30.0, -10.0]) # Position latérale
        super().__init__(position)
        
        self.label = "Temporal (IT / Wernicke)"
        self.pattern_recognition = 0.0

    async def integrate(self, visual_data: dict, spatial_data: dict, chemical_matrix: Dict[str, float]):
        """
        Fusionne le 'Quoi' et le 'Où' pour identifier l'objet.
        """
        # 1. Modulation Chimique
        # L'Acétylcholine (ACh) augmente la sélectivité de la reconnaissance
        ach = chemical_matrix.get("acetylcholine", 0.1)
        # La Sérotonine stabilise la perception (évite les faux positifs)
        sero = chemical_matrix.get("serotonin", 0.5)
        
        # 2. Calcul du signal de fusion
        # On combine la clarté visuelle et la certitude spatiale
        fusion_signal = (visual_data.get("visual_output", 0.0) * 0.7) + \
                        (spatial_data.get("spatial_certainty", 0.0) * 0.3)
        
        # 3. Appel à la couche L2/3 (Porte de la Mémoire)
        # C'est ici que William 'compare' avec ses souvenirs (Hippocampe)
        results = await self.process_input(
            signal_data=f"sem_{fusion_signal:.2f}",
            hippo_unit=None # Sera injecté par le LimbicSystem global
        )
        
        self.pattern_recognition = results.get("recognition", 0.5)
        
        # 4. Stabilisation sémantique
        # Plus la sérotonine est haute, plus on est exigeant sur la reconnaissance
        final_score = self.pattern_recognition * (0.8 + (sero * 0.4))
        
        return min(1.0, final_score)