#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# src/core/input_gateway.py
import sys
import os
import random

# Accès au registre
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from registry import SIGNALS, INPUT_CONFIG

class InputGateway:
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
            "nucleus": INPUT_CONFIG["DEFAULT_NUCLEUS"],
            "data": char,
            "signal_label": signal_label, # Le fil conducteur pour l'Hippo
            "intensity": noisy_value,
            "raw_ord": ord(char)
        }

        self.last_char = char
        return payload

    def get_summary(self):
        return f"Dernier Input: {self.last_char} | Signaux traités: {len(self.history)}"