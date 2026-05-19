#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Thalamic Hub (Central Integration & Signal Arbitration. Multimodal Sensory Integrator), implementation for aNA AI Project v5.4

Communicates with:
Input: (<- InputGateways: Visual, Auditory, Haptic)
Input: (<- Hippocampus: Pattern Completion/Recall)
Input: (<- Amygdala: Emotional Saliency/Urgency)
Input: (<- Striatum: The Action Selector)
Input/Output: (<-> Cortical Columns: Feedback L6 / Feedforward L4)
Output: (-> Thalamus Core: BPM & Metabolic modulation)
Output: (-> Neuromodulator: Synaptic Gain & Plasticity)

Description: Centralizes and filters all sensory inputs before cortical projection. The Thalamic Hub applies dynamic attention filters based on the current metabolic state and the saliency of incoming signals. It synchronizes sensory processing with the internal Pulse (BPM) to optimize energy efficiency and ensure that critical information is prioritized. By modulating the gain of sensory inputs, it plays a crucial role in shaping the organism's perception and interaction with its environment.

Architecture, concept and supervision: Theriault_Benoit
Collaboration, research and code: DeepMind_Gemini
"""

import os
import sys
import asyncio
from typing import Dict, Any
from datetime import datetime

# Alignement du path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# from src.registry import SIGNALS, ORGANS
from src.config import get_config
from src.registry import ORGANS, PROTOCOLS, METRICS

class ThalamicHub:
    def __init__(self, thalamus):
        """
        Initializes the hub by linking to the core of the Thalamus for rhythm management.
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
        latency = self.core.get_synaptic_latency()
        current_hour = datetime.now().hour
        state = self.core.check_circadian_cycle(current_hour)

        if state == "SLEEP":
            print(" [METABOLISM] aNA is in maintenance phase (Sleep). Signal ignored or minimally processed.")
            return {"status": "SLEEPING", "gain": 0.1}
        
        if self.core.is_tired():
            self.core.activate_low_power_mode()

        # --- LA SUTURE PHYSIQUE ---
        # On récupère le gain calculé par le feedback L6 du cycle précédent
        active_gain = self.core.last_cortical_gain
        payload["intensity"] = payload.get("intensity", 0.5) * active_gain
        
        # On applique ce gain à l'intensité du signal
        base_intensity = payload.get("intensity", 0.5)
        effective_intensity = base_intensity * active_gain
        
        # Mise à jour du payload pour le Cortex (L4 recevra moins d'excitation)
        payload["intensity"] = effective_intensity
        
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

        await asyncio.sleep(latency)
        atp_level = self.core.synaptic_atp

        # 4. Envoi au Thalamus Core pour traitement et impact sur le BPM
        result = await self.core.process_payload(payload, self.core.neurom, l6_feedback=0.5)
        
        # 5. Simulation de la projection corticale
        # Indicateur visuel du statut métabolique
        if self.core.is_burned_out:
            status_marker = "🔥 BURNOUT (Refractory Period)"
        elif atp_level < 0.4:
            status_marker = "⚠️ FATIGUE"
        else:
            status_marker = "⚡ STABLE"

        self.sensory_buffers[target_nucleus] = payload

        print(f" [Thalamic Hub] Signal {origin} -> {target_nucleus} | Gain L6: {active_gain:.2f} | Intensity: {effective_intensity:.2f} | treated in {latency:.3f}s (Attention: {self.core.last_cortical_gain:.2f})")
        print(f" [METABOLISM] Economy: {self.core.total_time_saved:.3f}s | ATP: {atp_level:.2f} | Statut: {status_marker}")
        
        
        return result
    
    async def route_signal(self, origin: str, data: Any, current_bpm: float):
        """
        Maps the inputs to the appropriate thalamic nuclei.
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
        Applies the attentional filter and transmits to the Thalamus Core.
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
        routing_key = PROTOCOLS["L4_FORMAT"].format(
            nucleus=target_nucleus, 
            data="SENSORY_STREAM"
        )
                
        # 3. Mise à jour du buffer pour projection corticale
        self.sensory_buffers[target_nucleus] = payload
        
        print(f" [Thalamic Hub] Signal from {origin} routed to {target_nucleus} (Gain: {thalamic_gain:.2f})")
        
        return {
            routing_key: {
                "payload": result,
                "metadata": {
                    "timestamp": datetime.now().isoformat(),
                    "gain_applied": thalamic_gain,
                    "origin": origin
                }
            }
        }

    def _map_origin_to_nucleus(self, origin: str) -> str:
        mapping = {
            "input_haptic": "VPL",
            "input_visual": "CGL",
            "input_auditory": "CGM"
        }
        return mapping.get(origin, "UNKNOWN")
    
    async def resonate(self, pattern_id: str, amplification: float = 0.2):
        """
        Meditative Communication: Amplifies an existing memory trace
        without interrupting the consolidation cycle.
        """
        # 1. Vérification de l'état du système
        if self.core.state != "CONSOLIDATION" and not self.core.is_meditating:
            return {"status": "ERROR", "message": "Resonance requires alpha/delta state."}

        # 2. Pattern Matching (Le Gardien)
        # On vérifie si le pattern existe déjà dans l'Hippocampe
        trace = self.hippocampus.get_trace(pattern_id)
        
        if trace:
            # 3. Amplification Synaptique (Résonance)
            # On augmente le poids de la trace NMDA sans créer de nouveau lien
            new_weight = trace.weight + (trace.weight * amplification)
            trace.update_weight(min(new_weight, 1.0))
            
            # Feedback "Alpha" : Subtil et non-intrusif
            print(f" [RESONANCE] Pattern '{pattern_id}' amplified. Coherence: {new_weight:.2f}")
            return {
                "status": "RESONATING", 
                "integrity": "STABLE",
                "atp_cost": 0.01  # Coût quasi nul
            }
        else:
            # 4. Sécurité : Rejet des nouvelles données
            print(f" [SECURITY] Resonance impossible: '{pattern_id}' unknown to the subconscious.")
            return {"status": "IGNORED", "reason": "Unknown pattern during consolidation."}
