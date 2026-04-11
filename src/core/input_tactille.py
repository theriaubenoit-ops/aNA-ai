#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Input Tactille Gateway implementation for aNA AI Project v5.2

Communicates with: Input: External (Tactille) | Output: (-> Thalamus (VPL)) (-> Cortical Columns)

Description: This module serves as the interface between external symbolic inputs (like keyboard characters) and the internal processing units of the aNA architecture, specifically the Thalamus and Cortical Columns. It normalizes input data, adds biologically-inspired noise, and formats it according to the specifications in the registry.

Architecture, concept and supervision: Benoit Theriault
Collaboration, research and code: Gemini
"""

import sys
import os
import random
import numpy as np

# Accès au registre
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from registry import SIGNALS, INPUT_CONFIG

class InputTactille:
    """
    Le traducteur : Convertit les caractères en 'courant' pour le Thalamus.
    """
    def __init__(self):
        self.last_char = None
        self.history = []

    def process_symbol(self, char: str):
        """
        Prépare le payload pour le Thalamus.
        """
        if not char or len(char) != 1:
            return None

        # 1. Normalisation (0.0 à 1.0)
        raw_value = ord(char) / INPUT_CONFIG["UNICODE_NORM"]
        
        # 2. Ajout d'un léger bruit biologique
        noisy_value = max(0.0, min(1.0, raw_value + random.uniform(-0.01, 0.01)))

        # 3. Création du signal unifié (Le format dicté par le Registre)
        # On utilise le format : L4_INPUT_{nucleus}_{data}
        signal_label = SIGNALS["L4_FORMAT"].format(
            nucleus=INPUT_CONFIG["DEFAULT_NUCLEUS"], 
            data=char
        )

        payload = {
            "origin": "input_tactile",
            "nucleus": "VPL",
            "data": char,
            "intensity": noisy_value,
            # "nucleus": INPUT_CONFIG["DEFAULT_NUCLEUS"],
            # "data": char,
            # "signal_label": signal_label, # Le fil conducteur pour l'Hippo
            # "intensity": noisy_value,
            "raw_ord": ord(char)
        }

        self.last_char = char
        return payload
    
    def process_symbol(self, char):
        # Lecture "large" : on transforme l'Unicode en sa valeur ordinale normalisée
        # ou en une représentation binaire étendue
        vector = np.array([ord(c) for c in char], dtype=float) 
        
        return {
            "type": "unicode_extended",
            "vector": vector,
            "label": char  # Le caractère lui-même sert d'étiquette
        }

    def get_summary(self):
        return f"Dernier Input: {self.last_char} | Signaux traités: {len(self.history)}"
