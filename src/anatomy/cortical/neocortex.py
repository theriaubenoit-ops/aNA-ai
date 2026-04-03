#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Neocortex v5.1 - Chef d'orchestre asynchrone
Gère les flux entre les lobes et le ChemicalCore.
Supervision : Benoit Theriault
"""

import asyncio
import numpy as np
from typing import Dict, Any

# Importation des lobes migrés (ou en cours)
from anatomy.cortical.occipital import OccipitalLobe
# Les autres lobes devront hériter de CorticalColumns pour l'async
# from anatomy.cortical.temporal import TemporalLobe
# from anatomy.cortical.parietal import ParietalLobe
# from anatomy.cortical.frontal import FrontalLobe

class Neocortex:
    def __init__(self, chemical_core):
        self.chemical_core = chemical_core
        
        # Initialisation des lobes v5.1
        self.occipital = OccipitalLobe() 
        # self.temporal = TemporalLobe()   
        # self.parietal = ParietalLobe()   
        # self.frontal = FrontalLobe()
        
        self.l6_feedback = 0.5 # Valeur d'équilibre initiale

    async def process_thalamic_input(self, payload: dict) -> dict:
        """
        Distribution coordonnée du flux sensoriel.
        Plus de try/except : on assume que les lobes sont en v5.1.
        """
        intensity = payload.get("intensity", 0.0)
        
        # 1. Extraction de la matrice chimique réelle
        current_mods = self.chemical_core.get_matrix()
        
        # 2. Traitement Parallèle (Le gain de performance de l'async)
        # On lance la vision (Occipital) et l'espace (Parietal) en même temps
        visual_task = self.occipital.process_visual_flow(intensity, current_mods)
        
        # Simulation des autres lobes tant qu'ils ne sont pas migrés :
        # spatial_task = self.parietal.process_spatial_flow(intensity, current_mods)
        
        # On attend les résultats
        visual_results = await visual_task
        
        # 3. Synthèse et Feedback
        # Le score de reconnaissance (L6) calme le Thalamus
        self.l6_feedback = visual_results.get("feedback", 0.5)
        
        # 4. Retour vers le système moteur ou le Dashboard
        return {
            "intent": "RECOGNITION",
            "visual_valence": visual_results.get("visual_output", 0.0),
            "l6_feedback": self.l6_feedback,
            "neuromodulation_active": current_mods
        }