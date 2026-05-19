#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Neocortex (The "Thinking" Shell), implementation for aNA AI Project v5.3

Communicates with: 
Input: (<- Thalamus L4) 
Input: (<- Hippocampus)
Input/Output: (<-> Cortical Columns) 
Input/Output: (<-> Limbic System)
Output: (-> Thalamus L6 Feedback) 
Output: (-> Motor Control / Cerebellum)

Description: This module is responsible for the hierarchical processing of sensory information and the generation of complex internal representations. It consists of multiple lobes (Occipital, Temporal, Parietal, Frontal) each containing specialized cortical columns that process different types of information. The Neocortex receives input from the Thalamus and Hippocampus, integrates it with the internal World Model, and produces outputs that influence both perception and action. It also provides feedback to the Thalamus to regulate sensory processing based on the current state of the organism.

Architecture, concept and supervision: Theriault_Benoit
Collaboration, research and code: DeepMind_Gemini, Cline 
"""
import os
import sys
import asyncio
import numpy as np
from typing import Dict, Any

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.registry import ORGANS
from src.anatomy.cortical.occipital import OccipitalLobe
from src.anatomy.cortical.temporal import TemporalLobe
from src.anatomy.cortical.parietal import ParietalLobe
from src.anatomy.cortical.frontal import FrontalLobe
from src.anatomy.cortical.cortical_column import (
    create_visual_cortical_lobe, 
    create_motor_cortical_lobe, 
    create_associative_cortical_lobe
)

class Neocortex:
    def __init__(self, chemical):
        self.chemical = chemical
        
        # --- INITIALISATION BASÉE SUR LE REGISTRE ---
        # On s'assure que le dictionnaire d'instances existe dans le registre central
        if "INSTANCES" not in ORGANS["NEOCORTEX"]:
            ORGANS["NEOCORTEX"]["INSTANCES"] = {}

        # Création et enregistrement
        self.occipital = create_visual_cortical_lobe(np.array([0,0,0]))
        ORGANS["NEOCORTEX"]["INSTANCES"]["V1"] = self.occipital

        # 1. Création dynamique des lobes selon le "Génome" (registry.py)
        for lobe_name in ORGANS["NEOCORTEX"]["LOBES"]:
            pos = np.array([0, 0, 0]) # Position de base
            
            if lobe_name == "OCCIPITAL":
                self.occipital = create_visual_cortical_lobe(pos)
                ORGANS["NEOCORTEX"]["INSTANCES"]["V1"] = self.occipital
                
            elif lobe_name == "TEMPORAL":
                self.temporal = TemporalLobe() # Votre classe spécialisée
                ORGANS["NEOCORTEX"]["INSTANCES"]["TEMPORAL"] = self.temporal
                
            elif lobe_name == "PARIETAL":
                self.parietal = ParietalLobe()
                ORGANS["NEOCORTEX"]["INSTANCES"]["PARIETAL"] = self.parietal
                
            elif lobe_name == "FRONTAL":
                self.frontal = FrontalLobe()
                ORGANS["NEOCORTEX"]["INSTANCES"]["FRONTAL"] = self.frontal
        
        self.l6_feedback = 0.5 
        print(f"🧬 Neocortex configured via registry: {list(ORGANS['NEOCORTEX']['INSTANCES'].keys())}")

    async def process_thalamic_input(self, payload: dict) -> dict:
        """
        Distribution coordonnée et parallèle du flux sensoriel.
        """
        intensity = payload.get("intensity", 0.0)
        
        # 1. Extraction de la matrice neuromodulatrice
        current_mods = self.chemical.get_matrix()
        
        # 2. TRAITEMENT PARALLÈLE (Vitesse Biologique)
        # On lance l'Occipital (Quoi/Vision) et le Parietal (Où/Espace) en même temps
        tasks = [
            self.occipital.process_visual_flow(payload.get("char", "unknown"), intensity, current_mods),
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