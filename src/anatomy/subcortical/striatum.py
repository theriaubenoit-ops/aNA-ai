#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Striatum implementation for aNA AI Project v5.4 - The Action Selector

Communicates with: 
Input: (<- Cortical Inputs - L5/L6 intent & motor plans) 
Input: (<- Limbic System - consolidated emotional valence & urgency) 
Input: (<- Chemical Matrix (Neuromodulateur))
Output: (-> Output Gateway)
Output: (-> Thalamic Hub - RTN Gating& signal clearance)

Description: This module implements the Striatum as the central action selector of aNA. It integrates cortical inputs related to potential actions and their predicted outcomes, evaluating them based on learned associations and current neuromodulatory states. The Striatum then selects the most appropriate action, sending motor commands to the output system and gating instructions to the Thalamus to facilitate or inhibit sensory processing based on the selected action.

Architecture, concept and supervision: Theriault Benoit
Collaboration, research and code: Google DeepMind (Gemini)
"""
import numpy as np
from typing import Dict, Any
from dataclasses import dataclass
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.config import get_config
from src.registry import ORGANS

class Striatum:
    """
    The Action Selector for aNA v5.3.
    Gathers Cortical intent and Limbic value to release Thalamic inhibition.
    """
    def __init__(self):
        self.config = get_config()
        self.action_history = []
        
    def process_selection(self, cortical_intent: float, limbic_pulse: Dict[str, float], atp_level: float):
        """
        Détermine si une action est autorisée.
        Input: Layer V output, Neuromodulator Matrix, Current ATP.
        """
        # 1. Calcul du coût de l'effort (Innovation bio-rythmique)
        effort_barrier = np.exp(2.0 * (1.0 - atp_level)) - 1.0
        
        # 2. Pondération par la Dopamine (Motivation)
        dopa = limbic_pulse.get("dopamine", 0.0)
        
        # 3. La règle d'or d'aNA : (Intention * Motivation) - Fatigue
        action_potential = (cortical_intent * (1.0 + dopa)) - effort_barrier
        
        # 4. Décision de Gating (Seuil Thalamique)
        threshold = self.config.get("THALAMIC_THRESHOLD", 0.35)
        is_allowed = action_potential > threshold
        
        return {
            "is_allowed": is_allowed,
            "rtn_modulator": -0.2 if is_allowed else 0.0, # Libération du Thalamus
            "potential": action_potential
        }
