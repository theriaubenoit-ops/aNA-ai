#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Thalamic Hub (Multimodal Sensory Integrator) for aNA AI Project v5.3

Communicates with:
Input: (<- InputGateways: Visual, Auditory, Haptic)
Input: (<- Hippocampus: Pattern Completion/Recall)
Input: (<- Amygdala: Emotional Saliency/Urgency)
Input/Output: (<-> Cortical Columns: Feedback L6 / Feedforward L4)
Output: (-> Thalamus Core: BPM & Metabolic modulation)
Output: (-> Neuromodulator: Synaptic Gain & Plasticity)

Description: Centralizes and filters all sensory inputs before cortical projection. The Thalamic Hub applies dynamic attention filters based on the current metabolic state and the saliency of incoming signals. It synchronizes sensory processing with the internal Pulse (BPM) to optimize energy efficiency and ensure that critical information is prioritized. By modulating the gain of sensory inputs, it plays a crucial role in shaping the organism's perception and interaction with its environment.

Architecture, concept and supervision: Benoit Theriault
Collaboration, research and code: Gemini
"""

import os
import sys
import asyncio
from typing import Dict, Any

# Alignement du path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# from src.registry import SIGNALS, ORGANS
from config import get_config
from registry import ORGANS

class ThalamicHub:
    def __init__(self, thalamus):
        """
        Initialise le hub en se liant au coeur du Thalamus pour la gestion du rythme.
        """
        self.core = thalamus
        self.sensory_buffers = {
            "VPL": None,  # Haptic
            "CGL": None,  # Visual
            "CGM": None   # Auditory
        }
        # Seuils d'attention (Gating)
        self.attention_filters = {
            "VPL": 0.15, 
            "CGL": 0.05, 
            "CGM": 0.2
        }

    async def route_sensory_input(self, origin: str, payload: Dict[str, Any]):
        config = get_config()
        target_nucleus = self._map_origin_to_nucleus(origin)
        
        # Récupération du poids sensoriel (ex: visual=0.5)
        sensory_type = origin.replace("input_", "")
        weight = config.get("SENSORY_WEIGHTS", {}).get(sensory_type, 0.2)

        # INNOVATION : Plus le poids est fort, plus le filtre est bas (Seuil inverse)
        # Un poids de 0.5 donne un filtre de base de 0.1
        base_filter = 0.3 * (1.0 - weight) 
        
        thalamic_gain = (1.0 - self.core.system_strain) 
        effective_intensity = payload.get("intensity", 0.5) * thalamic_gain

        if effective_intensity < base_filter:
            return {"status": "FILTERED_OUT", "nucleus": target_nucleus}

        # 3. Synchronisation avec le Pulse (BPM)
        # On attend le prochain "battement" pour traiter si le système est surchargé
        if self.core.current_bpm < 60: # Mode économie d'énergieinput_auditory
             await asyncio.sleep(0.1)

        # 4. Envoi au Thalamus Core pour traitement et impact sur le BPM
        # result = await self.core.process_payload(payload, l6_feedback=0.5)
        # result = await self.core.process_payload(payload, self.core.neuromod, l6_feedback=0.5)
        result = await self.core.process_payload(payload, self.core.neurom, l6_feedback=0.5)
        
        # 5. Simulation de la projection corticale
        self.sensory_buffers[target_nucleus] = payload
        print(f" [Thalamic Hub] Signal from {origin} routed to {target_nucleus} (Gain: {thalamic_gain:.2f})")
        
        return result
    
    async def route_signal(self, origin: str, data: Any, current_bpm: float):
        """
        Mappe les entrées vers les noyaux thalamiques appropriés.
        """
        mapping = {
            "input_haptic": "VPL",
            "input_visual": "CGL",
            "input_auditory": "CGM"
        }
        
        target_nucleus = mapping.get(origin)
        if not target_nucleus:
            return {"status": "ERROR", "message": "Unknown origin"}

        # Création du payload pour le Thalamus Core
        payload = {
            "origin": origin,
            "data": data,
            "intensity": 0.8  # Valeur par défaut ou calculée
        }

        # Appelle la logique de filtrage (que tu as déjà dans ton fichier)
        return await self.filter_and_process(payload, target_nucleus)
    
    async def filter_and_process(self, payload: Dict[str, Any], target_nucleus: str):
        """
        Applique le filtre attentionnel et transmet au Thalamus Core.
        """
        # 1. Calcul de l'intensité effective (Gating)
        origin = payload.get("origin", "")
        sensory_type = origin.replace("input_", "")
        
        # Récupération des poids depuis la config
        config = get_config()
        weight = config.get("SENSORY_WEIGHTS", {}).get(sensory_type, 0.2)

        # Seuil d'attention : plus le poids est haut, plus le filtre est permissif
        base_filter = 0.3 * (1.0 - weight) 
        
        # Modulation par l'état du système (Strain)
        thalamic_gain = (1.0 - self.core.system_strain) 
        effective_intensity = payload.get("intensity", 0.5) * thalamic_gain

        # --- GATE ATTENTIONNEL ---
        if effective_intensity < base_filter:
            return {"status": "FILTERED_OUT", "nucleus": target_nucleus, "gain": thalamic_gain}

        # 2. Transmission au Thalamus Core pour modulation du BPM
        # Le Core va traiter le signal et ajuster le rythme cardiaque (Pulse)
        # result = await self.core.process_payload(payload, l6_feedback=0.5)
        result = await self.core.process_payload(payload, self.core.neurom, l6_feedback=0.5)
        # On injecte l'intensité calculée (filtrée) dans le résultat pour le Neocortex
        result['intensity'] = effective_intensity
        result['gain'] = thalamic_gain
        
        # 3. Mise à jour du buffer pour projection corticale
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