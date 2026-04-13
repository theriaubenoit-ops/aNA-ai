#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Neuromodulator implementation for aNA AI Project v5.3b

Communicates with: Input: (<- Amygdala) | Output: (-> Neuron Receptors) (-> Thalamic Gain)

This module implements the Neuromodulator as a centralized system for managing neuromodulatory influences across the brain. It replaces the legacy spatial diffusion model with a more biologically plausible chemical matrix that modulates the activity of the Thalamus and Cortex based on inputs from the Limbic System (notably the Amygdala). The Neuromodulator tracks key neurotransmitters (dopamine, acetylcholine, serotonin, noradrenaline, cortisol) and applies homeostatic decay to simulate natural recapture processes.

Architecture, concept and supervision: Benoit Theriault
Collaboration, research and code: Gemini
"""

import os
import sys
import numpy as np
from typing import Dict, Any
from dataclasses import dataclass

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from src.config import get_config
from src.registry import ORGANS

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
        # On injecte les coefficients de performance du profil (Performant vs Saturé)
        config = get_config()
        self.performance_boost = config.get("MYELIN_EFFICIENCY_COEFF", 1.0)
        self.resonance_factor = config.get("CORTICAL_RESONANCE_FACTOR", 0.5)

        self.decay_rates = {
            "dopamine": 0.95,
            "acetylcholine": 0.80,
            "serotonin": 0.99, # Ajusté pour la stabilité
            "noradrenaline": 0.70,
            "cortisol": 0.99       
        }

    def get_signal_efficiency(self, base_myelin: float) -> float:
        """
        Calcule l'efficacité réelle du signal.
        Utilisé par le Pulse pour définir la latence.
        """
        # L'efficacité dépend de la myéline ET du boost de performance du profil
        return (1.0 + (base_myelin * self.performance_boost))

    def get_prediction_weight(self, l6_signal: float) -> float:
        """
        Calcule le poids de la rétroaction corticale (résonance).
        """
        # Plus le profil est 'Performant', plus la résonance stabilise le signal
        return l6_signal * self.resonance_factor

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
        self.state.serotonin *= self.decay_rates["serotonin"] # added
        self.state.noradrenaline *= self.decay_rates["noradrenaline"]
        self.state.cortisol *= self.decay_rates["cortisol"]

    def get_matrix(self) -> Dict[str, float]:
        """Retourne les niveaux actuels pour le Thalamus et le Cortex"""
        return {
            "dopamine": self.state.dopamine,
            "acetylcholine": self.state.acetylcholine,
            "serotonin": self.state.serotonin,
            "noradrenaline": self.state.noradrenaline,
            "cortisol": self.state.cortisol # added
        }