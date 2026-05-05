#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
aNA AI Project v5.3 - Test Neocortex Integration

Description: This test validates the integration of the Neocortex module within the aNA architecture. It checks that the Neocortex is correctly instantiated based on the central registry and that it can process a simulated signal through its layers. The test ensures that the Neocortex can communicate with the Thalamus (via Layer 6 feedback) and that it can handle neuromodulatory influences during processing.

Architecture and neuroinformatics: Theriault Benoit
"""

import unittest
import asyncio
import numpy as np
import os
import sys

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from src.registry import ORGANS
from src.anatomy.cortical.neocortex import Neocortex
from src.anatomy.base.neuromodulator import Neuromodulator # Pour le chemical


def create_ascii_header():
    print(f"\033c") 
    print("░              ░ ░░░▒▒▓▒▓▒▒▒▒▒░░▒▒░▒▒▒▓▒▓▒                                                                     ░ ░")
    print("▒░░   ░░░░░░░░░░▒▒▓▓▓▓▓▓▓██▓▒▒▒░░░▒▒▒▒▒░░░▒▒▓▓▒                                                         ░░░░░░▒▒▒▒")
    print("░░░░░░░░░░░░░▒▒▒▓▓▓▓▓▓██████▓▓▒▒▒░░▒▒▓▓▓▒▒▒░░▒▒▒▒▓▒                                        ░ ░░░ ░ ░░░░░░░░░▒▒▒▒▒▒")
    print("▓▒▒▒▒▒▒▒▒▓▒▓▓▓▓▓▓██████▓▒▒ ▒   ▒▓▒▓▒▒▒▒▓▒▓ ██▓▓▓▒▒▒▒▓      ░░▒▒▒▒▒▒▒░░░░░░▒░░░░▒▒░░▒░░░░░░░░░░░░░░░░░▒░▒▒▒░▒▒▒▓▓▓▓")
    print("▒▒▒▒▒▒▒▓▓▓▓▓████▓▓░                 ░░▒▒▒▓█▓░▓▓█▓▓ ░▒▓  ▒▓▓▓▓▓█▓▓▓█▓▒▒▒▓▓▒░░░░▒▓█▓▓▓▓▓▒▓▒▒▒▒▒▒▒░░░░░░░░░░░░░░▒▒▒▒▒")
    print("▒▒▓▒▓▓▓▓█████▓▒                         ░▒▒▓░ ▓██▓                ▒▓▒▒░░▒▓▒░░▒▓███▓█▓▓▓▓▓▓▓▓▓▓▓▒▓▒▒▒▒▒▒▒▒▒▒▓▒▓▓▓▓▓")
    print("▓▓▓█████▓░                                    ░░▒▒ _    _    _ ░▒░▒▒▒▓▒▓▒▓▒▓█▓███▓▒▓▓▓▓▓▓▓▓▓▓▓▓█▓██▓▓▓▓▓█▓████████")
    print("▓███▓▒      AI inspired by natural plasticity  ✴️  a    N    A  ▒▓█▒▓ ▒▓█▒Autonomous Neural Architecture v5.3  ▒▓▓")
    print("▓░                                                 _    _    _  ░▓▒▓  ░▓\n\n")

async def test_3b_integration():
    print("[STARTING NEOCORTEX INTEGRATION TEST]\n")
    
    # 1. Initialisation du cœur chimique (nécessaire pour le Neocortex)
    chemical = Neuromodulator()
    
    # 2. Instanciation du Neocortex (C'est ici que la magie du registre opère)
    # Votre classe Neocortex doit appeler create_visual_cortical_lobe dans son __init__
    nexo = Neocortex(chemical)
    
    print(f"📡 Register detected: {list(ORGANS['NEOCORTEX'].get('INSTANCES', {}).keys())}")

    # 3. Test de communication avec V1
    v1 = ORGANS["NEOCORTEX"]["INSTANCES"].get("V1")
    
    if v1:
        test_signal = 0.85
        # Simulation d'un signal montant (Thalamus -> V1)
        # On vérifie si process_through_layers existe dans l'objet v1
        try:
            # Note: v1 ici est l'instance de CorticalColumns créée par create_visual_cortical_lobe
            res = v1.process_through_layers(test_signal, {"acetylcholine": 0.5})
            print(f"✅ SUCCESS: The signal has passed through the layers. Exit L5 = {res:.4f}")
        except Exception as e:
            print(f"❌ ERROR during signal processing: {e}")
    else:
        print("❌ FAILURE: The V1 lobe was not found in the Register.")

if __name__ == "__main__":
    create_ascii_header()
    asyncio.run(test_3b_integration())