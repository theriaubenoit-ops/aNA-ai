#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Thalamic Hub (Multimodal Sensory Integrator) for aNA AI Project v5.3b

Description: Centralizes and filters all sensory inputs before cortical projection.

Architecture, concept and supervision: Benoit Theriault
Collaboration, research and code: Gemini
"""

import asyncio
from typing import Dict, Any
import numpy as np

class ThalamicHub:
    def __init__(self, thalamus_core):
        """
        Initialise le hub en se liant au coeur du Thalamus pour la gestion du rythme.
        """
        self.core = thalamus_core
        self.sensory_buffers = {
            "VPL": None,  # Haptic
            "CGL": None,  # Visual
            "CGM": None   # Auditory
        }
        # Seuils d'attention (Gating)
        self.attention_filters = {
            "VPL": 0.2, 
            "CGL": 0.3, 
            "CGM": 0.25
        }

    async def route_sensory_input(self, origin: str, payload: Dict[str, Any]):
        """
        Point d'entrée multimodal.
        Filtre le signal selon l'intensité et l'état chimique du système.
        """
        # 1. Identification du noyau cible
        target_nucleus = self._map_origin_to_nucleus(origin)
        
        # 2. Thalamic Gating (Le filtre de l'attention)
        # Si l'intensité est trop faible par rapport au bruit ambiant (gain), on ignore.
        thalamic_gain = (1.0 - self.core.system_strain) 
        effective_intensity = payload.get("intensity", 0.5) * thalamic_gain

        if effective_intensity < self.attention_filters.get(target_nucleus, 0.0):
            return {"status": "FILTERED_OUT", "nucleus": target_nucleus}

        # 3. Synchronisation avec le Pulse (BPM)
        # On attend le prochain "battement" pour traiter si le système est surchargé
        if self.core.current_bpm < 60: # Mode économie d'énergie
             await asyncio.sleep(0.1)

        # 4. Envoi au Thalamus Core pour traitement et impact sur le BPM
        result = await self.core.process_payload(payload, l6_feedback=0.5)
        
        # 5. Simulation de la projection corticale
        self.sensory_buffers[target_nucleus] = payload
        print(f" [Thalamic Hub] Signal from {origin} routed to {target_nucleus} (Gain: {thalamic_gain:.2f})")
        
        return result

    def _map_origin_to_nucleus(self, origin: str) -> str:
        mapping = {
            "input_haptic": "VPL",
            "input_visual": "CGL",
            "input_auditory": "CGM"
        }
        return mapping.get(origin, "UNKNOWN")