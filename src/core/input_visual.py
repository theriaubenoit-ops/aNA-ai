#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Input Visual Gateway implementation (Specialized in Matrix processing, Ratios and Foveal Zoom) for aNA AI Project v5.2

Communicates with: Input: External (Visual) | Output: (-> Thalamus (CGL)) (-> Occipital Lobe (V1))

Description: This module captures visual data (like images), processes it according to specified ratios (1:4 for wide view, 1:1 for normal, 2:1 for zoom), and prepares a unified payload for the Occipital Lobe. It simulates the biological process of visual perception, including foveal zoom and peripheral vision.

Features: Ratio-based processing, Foveal zoom simulation, Unified payload for the Hippocampus, Conformity with the central Registry for organ specifications.

Architecture, concept and supervision: Benoit Theriault
Collaboration, research and code: Gemini
"""

import numpy as np
import time
import sys
import os

# Accès au registre
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from registry import ORGANS # Le secret de la réussite

class InputVisualGateway:
    def __init__(self):
        # On valide la conformité avec le registre central
        self.specs = ORGANS.get("OCCIPITAL_LOBE", {})
        # print("  [Input Visual] Gateway initialized")
        
    async def capture_image(self, matrix_data, ratio=1):
        """Point d'entrée principal pour les fichiers image auto-adaptatif."""
        # L'organe calcule lui-même son intensité (Transduction)
        # Un écran noir ou uniforme = intensité faible (0.1)
        # Une image riche en détails = intensité forte (jusqu'à 1.0)
        std_dev = np.std(matrix_data)
        computed_intensity = min(1.0, max(0.1, std_dev / 128)) 

        # 2. Création du Payload avec l'intensité calculée
        return VisualSensoryPayload(
            intensity=computed_intensity, 
            raw_matrix=matrix_data, 
            ratio=ratio
        )

class VisualSensoryPayload:
    """Conteneur unifié pour le transport de données visuelles vers le lobe occipital."""
    def __init__(self, intensity, raw_matrix, ratio=1, zoom_coords=None):
        self.timestamp = time.time()
        self.source = "OCCIPITAL_LOBE"
        self.intensity = intensity # Stockage de l'intensité pour le Thalamic Hub
        self.ratio = ratio
        self.zoom_coords = zoom_coords # (x, y, w, h) si applicable
        self.signal_label = self.source # Pour la compatibilité avec le registre et l'hippocampe
        
        # Traitement du ratio (Zoom / Downsampling)
        self.processed_matrix = self._apply_sampling(raw_matrix, ratio)
        
        # Empreinte immuable pour l'Hippocampe (Tuple)
        self.fingerprint = tuple(self.processed_matrix.flatten().tolist())

    def get(self, key, default=None):
        """Assure la compatibilité avec l'ancien code du Thalamus."""
        return getattr(self, key, default)

    def _apply_sampling(self, matrix, ratio):
        """Applique la logique de ratio (1:4, 1:1, 2:1) sans casser le système."""
        if ratio == 1:
            return matrix
        elif ratio > 1: # Upsampling (Zoom) - Simulation bio-élégante
            return np.repeat(np.repeat(matrix, ratio, axis=0), ratio, axis=1)
        else: # Downsampling (Vue large)
            step = int(1/ratio)
            return matrix[::step, ::step]

