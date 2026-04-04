#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Parietal Lobe implementation for aNA v5.1

Communicates with: Input: (<- Thalamus) | Input/Output: (<-> Other Cortical Areas) | Output: (-> Motor / Pre-frontal)

This module implements the Parietal Lobe with its key regions (S1-S2, IPS) for somatosensory and spatial processing. It integrates with the ChemicalCore for neuromodulatory influences, particularly dopamine (Motivation) and noradrenaline (Trauma). The Parietal Lobe processes spatial information, modulates it based on the chemical state, and provides outputs to the Neocortex for synthesis with visual and semantic data.

Architecture, concept and supervision: Benoit Theriault
Collaboration, research and code: Gemini, Cline 
"""

import asyncio
import numpy as np
from typing import Dict, Any
from anatomy.cortical.cortical_column import CorticalColumns

class ParietalLobe(CorticalColumns):
    def __init__(self, position: np.ndarray = None):
        if position is None:
            position = np.array([0.0, 20.0, 20.0]) # Position dorsale dans aNA
        super().__init__(position)
        
        self.label = "Parietal (S1-S2 / IPS)"
        self.spatial_map = {"x": 0.5, "y": 0.5, "z": 0.5}

    async def process_spatial_flow(self, intensity: float, chemical_matrix: Dict[str, float]):
        """
        Calcule la position du signal et l'attention spatiale.
        """
        # 1. Influence chimique
        # La Dopamine booste la précision du tracking spatial
        dopa = chemical_matrix.get("dopamine", 0.1)
        # La Noradrénaline (Trauma) provoque une hyper-vigilance périphérique
        nora = chemical_matrix.get("noradrenaline", 0.1)
        
        # 2. Simulation de l'intégration (IPS - Intraparietal Sulcus)
        # En v5.1, on transforme l'intensité en une "pression" sensorielle
        spatial_pressure = intensity * (1.2 if dopa > 0.7 else 1.0)
        
        # 3. Traitement via les couches corticales
        # On passe le signal pour simuler la reconnaissance de la "forme" spatiale
        results = await self.process_input(
            signal_data=f"pos_{intensity}", 
            hippo_unit=None 
        )
        
        # 4. Mise à jour de la carte spatiale interne
        # On simule un léger drift si William est stressé (Cortisol/Nora)
        drift = 0.05 * nora
        self.spatial_map["x"] = max(0, min(1, intensity + drift))
        
        return {
            "coordinates": self.spatial_map,
            "spatial_certainty": results.get("recognition", 0.5),
            "focus_level": dopa
        }

    def get_spatial_outputs(self) -> Dict[str, Any]:
        """Utilisé par le Neocortex pour la synthèse"""
        return self.spatial_map
