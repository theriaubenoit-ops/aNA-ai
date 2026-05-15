#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
aNA AI Project v5.4 - Bridge Thalamo-Cortical implementation

Description: Validates the bidirectional synchronization between the Thalamic Hub 
and the Neocortex. This script tests the dynamic gain modulation of Layer 6 (L6) 
feedback, simulating how the brain filters sensory noise through top-down 
predictions. It ensures that the system focuses resources on unexpected stimuli 
while maintaining high-speed processing for known patterns.

Architecture, concept and supervision: Theriault Benoit
Collaboration, research and code: Google DeepMind (Gemini)
"""

import unittest
import os
import sys
import asyncio
import numpy as np

# The project root is defined dynamically.
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from src.registry import ORGANS, SIGNALS
from src.config import get_config
from src.anatomy.base.neuromodulator import Neuromodulator
from src.core.pulse import Pulse
from src.anatomy.subcortical.thalamus import Thalamus
from src.anatomy.subcortical.thalamic_hub import ThalamicHub
from src.anatomy.cortical.cortical_column import CorticalColumns
from src.anatomy.limbic.hippocampus import Hippocampus
from src.anatomy.subcortical.striatum import Striatum

def create_ascii_header():
    print(f"\033c") 
    print("░              ░ ░░░▒▒▓▒▓▒▒▒▒▒░░▒▒░▒▒▒▓▒▓▒                                                                     ░ ░")
    print("▒░░   ░░░░░░░░░░▒▒▓▓▓▓▓▓▓██▓▒▒▒░░░▒▒▒▒▒░░░▒▒▓▓▒                                                         ░░░░░░▒▒▒▒")
    print("░░░░░░░░░░░░░▒▒▒▓▓▓▓▓▓██████▓▓▒▒▒░░▒▒▓▓▓▒▒▒░░▒▒▒▒▓▒                                        ░ ░░░ ░ ░░░░░░░░░▒▒▒▒▒▒")
    print("▓▒▒▒▒▒▒▒▒▓▒▓▓▓▓▓▓██████▓▒▒ ▒   ▒▓▒▓▒▒▒▒▓▒▓ ██▓▓▓▒▒▒▒▓      ░░▒▒▒▒▒▒▒░░░░░░▒░░░░▒▒░░▒░░░░░░░░░░░░░░░░░▒░▒▒▒░▒▒▒▓▓▓▓")
    print("▒▒▒▒▒▒▒▓▓▓▓▓████▓▓░                 ░░▒▒▒▓█▓░▓▓█▓▓ ░▒▓  ▒▓▓▓▓▓█▓▓▓█▓▒▒▒▓▓▒░░░░▒▓█▓▓▓▓▓▒▓▒▒▒▒▒▒▒░░░░░░░░░░░░░░▒▒▒▒▒")
    print("▒▒▓▒▓▓▓▓█████▓▒                         ░▒▒▓░ ▓██▓                ▒▓▒▒░░▒▓▒░░▒▓███▓█▓▓▓▓▓▓▓▓▓▓▓▒▓▒▒▒▒▒▒▒▒▒▒▓▒▓▓▓▓▓")
    print("▓▓▓█████▓░                                    ░░▒▒ _    _    _ ░▒░▒▒▒▓▒▓▒▓▒▓█▓███▓▒▓▓▓▓▓▓▓▓▓▓▓▓█▓██▓▓▓▓▓█▓████████")
    print("▓███▓▒      AI inspired by natural plasticity  ✴️  a    N    A  ▒▓█▒▓ ▒▓█▒Autonomous Neural Architecture v5.4  ▒▓▓")
    print("▓░                                                 _    _    _  ░▓▒▓  ░▓\n")

async def run_thalamo_cortical_loop():
    print(f"--- Systemic Integration aNA ---")
    
    # 1. Initialisation du Génome
    config = get_config()
    neurom = Neuromodulator()
    hippo = Hippocampus()
    pulse = Pulse()
    striatum = Striatum() 
    
    # Initialisation des Organes
    thalamus_core = Thalamus(
    pulse=pulse, 
    hippocampus=hippo,
    striatum=striatum, 
    neuromodulator=neurom
    )
    hub = ThalamicHub(thalamus_core)
    
    # Création d'une colonne corticale (ex: Lobe Visuel en Layer IV)
    v1_column = CorticalColumns(np.array([10.0, 20.0, 0.0]))
    
    # État initial du feedback (Neutre)
    l6_feedback = 0.5 
    
    # Simulation d'un stimulus répété (Habituation)
    stimulus = {
        "signal_label": "A", 
        "nucleus": "LGN", 
        "intensity": 0.8,
        "origin": "input_visual",
        "saliency": 0.7  # Le ThalamicHub utilise cette clé pour le filtrage
    }

    # print(f"\n[START OF THE PERCEPTION CYCLE]")
    
    # for cycle in range(1, 6):
    #     print(f"\n--- CYCLE {cycle} ---")
        
    #     # ÉTAPE A : Le Thalamus filtre et module le BPM
    #     # On injecte le feedback L6 du cycle précédent
    #     thalamic_result = await hub.route_sensory_input(
    #         origin=stimulus["origin"],
    #         payload=stimulus
    #     )
        
    #     if thalamic_result["status"] == "PROJECTED_TO_CORTEX":
    #         # ÉTAPE B : Projection vers la Couche IV (L4) du Cortex
    #         # Le signal est "suturé" ici
    #         cortical_output = await v1_column.process_input(
    #             signal_data=stimulus["signal_label"],
    #             hippo_unit=hippo
    #         )
            
    #         # ÉTAPE C : Récupération du feedback de la Couche VI (L6)
    #         l6_feedback = cortical_output["l6_feedback"]
    #         recognition = cortical_output["recognition"]
            
    #         # ÉTAPE D : Ajustement du gain pour le prochain cycle
    #         # Le Thalamus ajuste sa sensibilité selon la certitude du Cortex
    #         new_gain = thalamus_core.apply_cortical_feedback(
    #             current_gain=thalamic_result.get("gain", 1.0), # Valeur de secours à 1.0
    #             l6_signal=l6_feedback,
    #             config=config
    #         )
            
    #         print(f" [Cortex] Recognition: {cortical_output['recognition']:.2f}")
    #         print(f" [Thalamus] Gain adjusted via L6: {new_gain:.2f}")            
    #         print(f" [Pulse] Current rhythm: {thalamic_result['bpm']:.2f} BPM")
            
    #     else:
    #         print(f" [Hub] Signal ignored: {thalamic_result['status']}")

    #     # aNA s'active (simule le temps de traitement biologique)
    #     await asyncio.sleep(0.5)


    print(f"\n[START OF PERCEPTION CYCLE - BREAK TEST]")
    
    for cycle in range(1, 21): # On pousse jusqu'à 10 cycles pour voir la ré-habituation
        print(f"\n--- CYCLE {cycle} ---")
        
        # VARIATION DU STIMULUS : On passe de A à B au cycle 6
        current_signal = "A" if cycle < 6 else "B"
        
        if cycle == 6:
            print(f" ⚠️  PATTERN BREAK: New stimulus detected ['{current_signal}']")

        stimulus = {
            "signal_label": current_signal, 
            "nucleus": "CGL", 
            "intensity": 0.8,
            "origin": "input_visual",
            "saliency": 0.7 
        }
        
        # 1. Routage Thalamique
        thalamic_result = await hub.route_sensory_input(
            origin=stimulus["origin"],
            payload=stimulus
        )
        
        # 2. Traitement Cortical
        cortical_output = await v1_column.process_input(
            signal_data=stimulus["signal_label"],
            hippo_unit=hippo
        )
        
        # 3. Boucle de Suture L6 -> Thalamus
        l6_feedback = cortical_output["l6_feedback"]
        
        # On applique le feedback au Thalamus Core pour le cycle SUIVANT
        # Si reconnaissance bas (nouveau signal), le gain doit remonter.
        new_gain = thalamus_core.apply_cortical_feedback(
            current_gain=thalamic_result.get("gain", 1.0),
            l6_signal=l6_feedback,
            config=config
        )
        
        print(f" [Stimulus] Current signal: '{current_signal}'")
        print(f" [Cortex] Recognition : {cortical_output['recognition']:.2f}")
        print(f" [Thalamus] Gain for next cycle : {new_gain:.2f}")
        
        await asyncio.sleep(0.3)

    print("\n  *Every measurement reflected here is a digital bridge to biological reality,")
    print("   designed to synthesize the fundamental principles of living systems.\n")

if __name__ == "__main__":
    create_ascii_header()
    asyncio.run(run_thalamo_cortical_loop())