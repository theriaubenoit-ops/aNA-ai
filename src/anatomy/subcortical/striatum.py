#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Striatum (Executive Gating & Metabolic Arbitration. The Action Selector), implementation for aNA AI Project v5.4

Communicates with: 
Input: (<- Cortical Inputs: L5/L6 intent & motor plans) 
Input: (<- Limbic System: Consolidated emotional valence & urgency) 
Input: (<- Chemical Matrix (Neuromodulateur))
Output: (-> Output Gateway)
Output: (-> Thalamic Hub: RTN Gating& signal clearance)

Description: This module implements the Striatum as the central action selector of aNA. It integrates cortical inputs related to potential actions and their predicted outcomes, evaluating them based on learned associations and current neuromodulatory states. The Striatum then selects the most appropriate action, sending motor commands to the output system and gating instructions to the Thalamus to facilitate or inhibit sensory processing based on the selected action.

Architecture, concept and supervision: Theriault_Benoit
Collaboration, research and code: DeepMind_Gemini
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
        
    def process_selection(self, cortical_intent: float, neurom: Any, atp_level: float): #  limbic_pulse: Dict[str, float]
        """
        Détermine si une action est autorisée selon l'équilibre Effort/Besoin.
        """
        # 1. LA NOUVELLE BARRIÈRE (Parabolique, plus douce)
        # Au lieu de l'exponentielle qui bloquait tout à 0.8 ATP
        effort_barrier = (1.0 - atp_level) ** 2
        
        # 2. LE SURVIVAL DRIVE (L'instinct de faim)
        # Plus l'ATP est bas, plus l'organisme "pousse" pour survivre
        survival_drive = (1.0 - atp_level) * 0.5
        
        # 3. Récupération de la motivation chimique
        # dopa = limbic_pulse.get("dopamine", 0.0)
        if hasattr(neurom, 'state'):
            # C'est l'objet Neuromodulator complet
            dopa = neurom.state.dopamine
        elif isinstance(neurom, dict):
            # C'est déjà la matrice chimique (dictionnaire)
            dopa = neurom.get("dopamine", 0.1)
        else:
            # Valeur de secours si rien ne correspond
            dopa = 0.1
        
        # 4. LE CALCUL DU POTENTIEL (La règle d'or d'aNA v5.4)
        # On booste l'intention par la dopamine ET l'instinct de survie
        action_potential = (cortical_intent * (1.0 + dopa + survival_drive)) - effort_barrier
        
        # 5. DÉCISION
        threshold = self.config.get("THALAMIC_THRESHOLD", 0.35)
        is_allowed = action_potential > threshold

        if not is_allowed:
            # Si l'action est refusée, on augmente l'inhibition du RTN (verrouillage)
            rtn_modulator = 0.0 if is_allowed else max(0.1, 0.5 - action_potential)
        else:
            # Si l'action est permise, on ne rajoute pas d'inhibition
            rtn_modulator = 0.0

        return {
            "is_allowed": is_allowed,
            "potential": action_potential,
            "barrier": effort_barrier,
            "drive": survival_drive,
            "rtn_modulator": rtn_modulator
        }