#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Neuromodulator implementation for aNA v5.1 with:

This module implements the Neuromodulator as a centralized system for managing neuromodulatory influences across the brain. It replaces the legacy spatial diffusion model with a more biologically plausible chemical matrix that modulates the activity of the Thalamus and Cortex based on inputs from the Limbic System (notably the Amygdala). The Neuromodulator tracks key neurotransmitters (dopamine, acetylcholine, serotonin, noradrenaline) and applies homeostatic decay to simulate natural recapture processes.

Architecture, concept and supervision: Benoit Theriault
Collaboration, research and code: Gemini
"""

import numpy as np
from typing import Dict, Any
from dataclasses import dataclass

@dataclass
class NeuromodulatorState:
    # Valeurs de base (Homeostasie)
    dopamine: float = 0.1       # Motivation / Récompense
    acetylcholine: float = 0.1  # Attention / Habituation
    serotonin: float = 0.5      # Stabilité / Humeur
    noradrenaline: float = 0.1  # Alerte / Gravure Flash (Trauma)
    cortisol: float = 0.0       # Stress long terme

class Neuromodulator:
    def __init__(self):
        self.state = NeuromodulatorState()
        self.decay_rates = {
            "dopamine": 0.95,
            "acetylcholine": 0.80, # Décroissance rapide pour l'attention
            "noradrenaline": 0.70, # Retour au calme après l'alerte
            "cortisol": 0.99       # Le stress persiste plus longtemps
        }

    def update_from_limbic(self, amygdala_output: Dict[str, float]):
        """
        Met à jour la matrice chimique selon les sorties de l'Amygdale.
        """
        # La noradrénaline est directement liée à l'intensité du trauma
        if "noradrenaline" in amygdala_output:
            self.state.noradrenaline = max(self.state.noradrenaline, amygdala_output["noradrenaline"])
            
        # La dopamine répond à la valence positive / succès
        if "dopamine_boost" in amygdala_output:
            self.state.dopamine = min(1.0, self.state.dopamine + amygdala_output["dopamine_boost"])

    def apply_homeostasis(self):
        """Simule la recapture des neurotransmetteurs (Cycle du Pulse)"""
        self.state.dopamine *= self.decay_rates["dopamine"]
        self.state.acetylcholine *= self.decay_rates["acetylcholine"]
        self.state.noradrenaline *= self.decay_rates["noradrenaline"]
        self.state.cortisol *= self.decay_rates["cortisol"]

    def get_matrix(self) -> Dict[str, float]:
        """Retourne les niveaux actuels pour le Thalamus et le Cortex"""
        return {
            "dopamine": self.state.dopamine,
            "acetylcholine": self.state.acetylcholine,
            "serotonin": self.state.serotonin,
            "noradrenaline": self.state.noradrenaline
        }
