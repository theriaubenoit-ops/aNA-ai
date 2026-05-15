#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Input Haptic Gateway implementation for aNA AI Project v5.3

Communicates with: 
Input: External (Haptic)
Output: (-> Thalamus (VPL))
Output: (-> Cortical Columns)

Description: This module serves as the interface between external symbolic inputs (like keyboard characters) and the internal processing units of the aNA architecture, specifically the Thalamus and Cortical Columns. It normalizes input data, adds biologically-inspired noise, and formats it according to the specifications in the registry.

Architecture, concept and supervision: Theriault Benoit
Collaboration, research and code: Gemini
"""

import sys
import os
import random
import numpy as np

# Accès au registre
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.registry import SIGNALS, INPUT_CONFIG

class InputHapticGateway:
    """
    Le traducteur : Convertit les caractères en 'courant' pour le Thalamus.
    """
    def __init__(self):
        self.last_char = None
        self.history = []
        # print("  [Input Haptic] Gateway initialized")

    def process_symbol(self, char):
        # Votre version "Unicode Étendu"
        vector = np.array([ord(c) for c in char], dtype=float) 
        
        return {
            "origin": "input_haptic",
            "type": "unicode_extended",
            "vector": vector,
            "label": char,
            "intensity": 0.8  # Crucial pour éviter un crash dans le Thalamus
        }
    
    def get_summary(self):
        return f"Dernier Input: {self.last_char} | Signaux traités: {len(self.history)}"