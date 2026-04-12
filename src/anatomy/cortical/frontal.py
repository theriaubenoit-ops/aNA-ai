#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Frontal Lobe implementation for aNA v5.1

Communicates with: Input: (<- Thalamus) | Input/Output: (<-> Other Cortical Areas) | Output: (-> Motor / Pre-frontal)

This module implements the Frontal Lobe with its key regions (M1, PFC) for motor planning and executive functions. It integrates with the ChemicalCore for neuromodulatory influences, particularly dopamine (Motivation) and noradrenaline (Trauma). The Frontal Lobe transforms recognition signals from the Temporal Lobe into motor intentions and provides feedback to the Neocortex for action execution.

Architecture, concept and supervision: Benoit Theriault
Collaboration, research and code: Gemini, Cline 
"""

import asyncio
import numpy as np
from typing import Dict, Any
from anatomy.cortical.cortical_column import CorticalColumns

class FrontalLobe(CorticalColumns):
    def __init__(self, position: np.ndarray = None):
        if position is None:
            position = np.array([30.0, 0.0, 0.0]) # Position antérieure
        super().__init__(position)
        
        self.label = "Frontal (M1 / PFC)"
        self.action_threshold = 0.4 # Seuil d'engagement moteur
        self.current_intent = 0.0

    async def plan_action(self, recognition_score: float, chemical_matrix: Dict[str, float]):
        """
        Transforme la reconnaissance sémantique en intention motrice.
        """
        # 1. Modulation Chimique
        # La Dopamine abaisse le seuil d'action (Motivation)
        dopa = chemical_matrix.get("dopamine", 0.1)
        # La Noradrénaline (Trauma) peut causer une inhibition ou une réaction réflexe
        nora = chemical_matrix.get("noradrenaline", 0.1)
        
        # Ajustement dynamique du seuil
        dynamic_threshold = self.action_threshold - (dopa * 0.2)
        
        # 2. Calcul de l'impulsion (Layer V)
        # Si on reconnaît bien l'objet, l'intention est claire
        raw_intent = recognition_score
        
        # 3. Simulation du "Tremblement" ou de la "Saisie"
        # En cas de fort stress (Nora > 0.7), l'action devient instable
        if nora > 0.7:
            raw_intent += np.random.uniform(-0.1, 0.1)
            
        # 4. Décision d'exécution
        is_firing = raw_intent > dynamic_threshold
        self.current_intent = raw_intent if is_firing else 0.0
        
        # 5. Traitement Cortical (Myélinisation de l'effort)
        await self.process_input(
            signal_data=f"act_{self.current_intent:.2f}",
            hippo_unit=None
        )
        
        return {
            "motor_output": self.current_intent,
            "is_executing": is_firing,
            "effort_level": (raw_intent * 0.8) + (nora * 0.2)
        }