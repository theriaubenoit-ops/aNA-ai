#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Neuromodulator implementation for aNA AI Project v5.3

Communicates with: Input: (<- Amygdala) | Output: (-> Neuron Receptors) (-> Thalamic Gain)

Description: This module implements the Neuromodulator as a centralized system for managing neuromodulatory influences across the brain. It replaces the legacy spatial diffusion model with a more biologically plausible chemical matrix that modulates the activity of the Thalamus and Cortex based on inputs from the Limbic System (notably the Amygdala). The Neuromodulator tracks key neurotransmitters (dopamine, acetylcholine, serotonin, norepinephrine, cortisol) and applies homeostatic decay to simulate natural recapture processes.

Architecture, concept and supervision: Benoit Theriault
Collaboration, research and code: Gemini
"""

import os
import sys
import numpy as np
from typing import Dict, Any
from dataclasses import dataclass

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from config import get_config
from registry import ORGANS

@dataclass
class NeuromodulatorState:
    # Valeurs de base (Homeostasie)
    dopamine: float = 0.1       # Motivation / Récompense
    acetylcholine: float = 0.1  # Attention / Habituation
    serotonin: float = 0.5      # Stabilité / Humeur
    norepinephrine: float = 0.1  # Alerte / Gravure Flash (Trauma)
    cortisol: float = 0.0       # Stress long terme

class Neuromodulator:
    def __init__(self):
        self.state = NeuromodulatorState()
        config = get_config()
        self.performance_boost = config.get("MYELIN_EFFICIENCY_COEFF", 1.0)
        self.resonance_factor = config.get("CORTICAL_RESONANCE_FACTOR", 0.5)

        self.decay_rates = {
            "dopamine": 0.95,
            "acetylcholine": 0.80,
            "serotonin": 0.99,
            "norepinephrine": 0.70, # Uniformisé
            "cortisol": 0.99       
        }

    def inject_chemicals(self, source_name: str, chemical_data: Dict[str, float]):
        """
        Entrée universelle pour l'Amygdale, le Striatum et le Cortex (v5.3.2).
        """
        # 1. Norepinephrine (Alerte / Amygdale)
        if "norepinephrine" in chemical_data:
            self.state.norepinephrine = max(self.state.norepinephrine, chemical_data["norepinephrine"])
            
        # 2. Dopamine (Récompense / Striatum ou Amygdale)
        if "dopamine" in chemical_data:
            # On peut imaginer une sommation pour la dopamine (cumul de succès)
            self.state.dopamine = min(1.0, self.state.dopamine + chemical_data["dopamine"])

        # 3. Acetylcholine (Attention / Cortex ou Thalamus)
        if "acetylcholine" in chemical_data:
            self.state.acetylcholine = min(1.0, self.state.acetylcholine + chemical_data["acetylcholine"])

    def apply_homeostasis(self):
        """Simule la recapture (Cycle du Pulse)"""
        for neurotransmitter, rate in self.decay_rates.items():
            current_val = getattr(self.state, neurotransmitter)
            setattr(self.state, neurotransmitter, current_val * rate)

    def get_matrix(self) -> Dict[str, float]:
        """Retourne les niveaux pour Neuron.py et Thalamus.py"""
        return {
            "dopamine": self.state.dopamine,
            "acetylcholine": self.state.acetylcholine,
            "serotonin": self.state.serotonin,
            "norepinephrine": self.state.norepinephrine, # Clé identique à Neuron.py
            "cortisol": self.state.cortisol,
            "no_gas": 0.1 # Base stable
        }