#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Neocortex implementation for aNA AI Project v5.3

Communicates with: 
Input: (<- Thalamus L4) (<- Hippocampus)
Input/Output: (<-> Cortical Columns) (<-> Limbic System)
Output: (-> Thalamus L6 Feedback) (-> Motor Control / Cerebellum)

This module represents the high-level cognitive engine of aNA. It manages the distribution of sensory data across specialized Cortical Columns, facilitating the L4->L2/3->L6 processing cascade. By generating downward feedback from Layer 6 to the Thalamus, the Neocortex actively modulates sensory gain and attentional focus. It integrates long-term structural plasticity and myelination logic to optimize signal conductivity based on recognition patterns.

Architecture, concept and supervision: Benoit Theriault
Collaboration, research and code: Gemini, Cline 
"""

import asyncio
import numpy as np
from typing import Dict, Any

from anatomy.cortical.occipital import OccipitalLobe
from anatomy.cortical.temporal import TemporalLobe
from anatomy.cortical.parietal import ParietalLobe
from anatomy.cortical.frontal import FrontalLobe

class Neocortex:
    def __init__(self, chemical_core):
        self.chemical_core = chemical_core
        
        # Initialisation des lobes (Chacun avec son propre σ et sa spécialité)
        self.occipital = OccipitalLobe() 
        self.temporal = TemporalLobe()   
        self.parietal = ParietalLobe()   
        self.frontal = FrontalLobe()
        
        self.l6_feedback = 0.5 

    async def process_thalamic_input(self, payload: dict) -> dict:
        """
        Distribution coordonnée et parallèle du flux sensoriel.
        """
        intensity = payload.get("intensity", 0.0)
        
        # 1. Extraction de la matrice neuromodulatrice
        current_mods = self.chemical_core.get_matrix()
        
        # 2. TRAITEMENT PARALLÈLE (Vitesse Biologique)
        # On lance l'Occipital (Quoi/Vision) et le Parietal (Où/Espace) en même temps
        tasks = [
            self.occipital.process_visual_flow(intensity, current_mods),
            self.parietal.process_spatial_flow(intensity, current_mods)
        ]
        
        visual_res, spatial_res = await asyncio.gather(*tasks)
        
        # 3. INTÉGRATION SÉMANTIQUE (Temporal)
        # Fusion des flux pour identification
        recognition_score = await self.temporal.integrate(
            visual_data=visual_res, 
            spatial_data=spatial_res, 
            chemical_matrix=current_mods
        )
        
        # 4. PLANIFICATION EXÉCUTIVE (Frontal)
        # Décision d'intention motrice basée sur le sens perçu
        motor_res = await self.frontal.plan_action(recognition_score, current_mods)
        
        # 5. SYNTHÈSE DU FEEDBACK L6
        # On récupère le feedback de V1 pour réguler le Thalamus
        self.l6_feedback = visual_res.get("feedback", 0.5)
        
        return {
            "intent": "RECOGNITION_ACTIVE",
            "recognition_score": recognition_score,
            "motor_output": motor_res.get("motor_output", 0.0),
            "l6_feedback": self.l6_feedback,
            "neuromodulation_active": current_mods,
            "is_executing": motor_res.get("is_executing", False)
        }
