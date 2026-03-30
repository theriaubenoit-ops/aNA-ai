#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# src/anatomy/cortical/neocortex.py
import numpy as np
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from src.registry import CORTEX_CONFIG

# Importation des lobes
from anatomy.cortical.occipital import OccipitalLobe
from anatomy.cortical.temporal import TemporalLobe
from anatomy.cortical.parietal import ParietalLobe
from anatomy.cortical.frontal import FrontalLobe

class Neocortex:
    def __init__(self):
        self.occipital = OccipitalLobe() 
        self.temporal = TemporalLobe()   
        self.parietal = ParietalLobe()   
        self.frontal = FrontalLobe()     
        self.l6_feedback = 0.0 

    def process_thalamic_input(self, payload: dict):
        """Distribue le flux en s'adaptant dynamiquement aux signatures v4.0"""
        intensity = payload.get("intensity", 0.0)
        current_mods = {
            "dopamine": 0.5,
            "acetylcholine": 0.5,
            "serotonin": 0.5,
            "noradrenaline": 0.5
        }
        
        # 1. Étape A : Le Pariétal (Spatial)
        # On tente l'appel avec neuromodulateurs, sinon on replie sur l'appel de base
        try:
            self.parietal.process_spatial_input(intensity, {"coord": [0.0, 0.0]}, neuromodulators=current_mods)
        except TypeError:
            self.parietal.process_spatial_input(intensity, {"coord": [0.0, 0.0]})
        
        parietal_dict = self.parietal.get_spatial_outputs()

        # 2. Étape B : L'Occipital (Visuel)
        try:
            visual_data = self.occipital.process_visual_input(np.array([[intensity]]), neuromodulators=current_mods)
        except TypeError:
            visual_data = self.occipital.process_visual_input(np.array([[intensity]]))
        
        # 3. Étape C : Le Temporal (Sémantique)
        # Le Temporal v4.0 est le plus complexe, il lui faut souvent tout le contexte
        try:
            self.temporal.process_semantic_input(
                intensity, 
                visual_data, 
                neuromodulators=current_mods,
                parietal_outputs=parietal_dict
            )
        except TypeError:
            # Repli si la signature ne correspond pas
            self.temporal.process_semantic_input(intensity, visual_data)
        
        # 4. Synthèse du Feedback L6 (La clé de la régulation Thalamique)
        # On extrait la reconnaissance sémantique pour calmer le Thalamus
        recognition = getattr(self.temporal, 'pattern_recognition', 0.0)
        self.l6_feedback = recognition * CORTEX_CONFIG["FEEDBACK_L6_GAIN"]
        
        return self.l6_feedback