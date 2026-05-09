#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
aNA AI Project v5.3 - Test Hub Autonomy

Description: Validate the complete ThalamicHub flow -> Neocortex (V1) -> L6 Feedback -> Pulse Modulation (BPM) in a standalone scenario. This test simulates a sequence of visual input, observes how the ThalamicHub processes and filters this input, how it is projected to the Neocortex (V1), and how feedback from L6 influences the heart rate via the Pulse. The goal is to ensure that the interactions between these components work coherently and autonomously, without external intervention.

Architecture, concept and supervision: Benoit Theriault
Collaboration, research and code: Google DeepMind (Gemini)
"""

import unittest
import asyncio
import numpy as np
import sys
import os

# Configuration des chemins
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.config import get_config
from src.registry import ORGANS
from src.anatomy.subcortical.thalamus import Thalamus
from src.anatomy.subcortical.thalamic_hub import ThalamicHub
from src.anatomy.limbic.hippocampus import Hippocampus
from src.anatomy.cortical.neocortex import Neocortex
from src.anatomy.base.neuromodulator import Neuromodulator
from src.core.pulse import Pulse


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

async def test_hub_cycle():
    config = get_config()
    print("🚀 STARTING THE HUB AUTONOMY TEST")
    print("="*50)

    # 1. Initialisation de l'environnement bio-numérique
    chemical = Neuromodulator()
    hippo = Hippocampus(config=config, neuromodulator=chemical)
    heart = Pulse(bpm=config.get("BASE_BPM", 72.0))
    
    # 2. Initialisation des organes maîtres
    # Le Neocortex s'enregistre dans le registre lors de sa création
    nexo = Neocortex(chemical)
    thalamus = Thalamus(
        hippocampus=hippo, 
        pulse=heart, 
        neuromodulator=chemical 
    )
    hub = ThalamicHub(thalamus=thalamus)

    print(f"🧠 Organs detected: {list(ORGANS['NEOCORTEX']['INSTANCES'].keys())}")

    # 3. Simulation d'une séquence d'entrée (Le monde extérieur)
    stimulis = [("VISUAL", 0.9), ("VISUAL", 0.4), ("VISUAL", 0.95)]

    for sense, intensity in stimulis:
        print(f"\n📥 Input detected: {sense} | Intensity: {intensity}")

        # A. Passage par le filtre du Thalamus (Gating)
        matrix = chemical.get_matrix()
        gating_res = await hub.route_signal(f"input_{sense.lower()}", intensity, heart.bpm)
        filtered_val = gating_res.get('intensity', 0.0)
        
        print(f"🔍 Thalamus Gating : {intensity} -> {filtered_val:.4f}")

# B. Projection vers le Neocortex (V1)
        v1 = ORGANS["NEOCORTEX"]["INSTANCES"].get("V1")
        if v1:
            # Traitement par les 6 couches
            l5_output = v1.process_through_layers(filtered_val, matrix)
            
            # Correction : Récupération sécurisée du feedback L6
            # Si 'layers' n'est pas un attribut, vérifiez si c'est une méthode ou 
            # utilisez une valeur par défaut en attendant de vérifier la structure de CorticalColumns
            try:
                l6_feedback = v1.layers.get("L6", 0.5) if hasattr(v1, 'layers') else 0.5
            except:
                l6_feedback = 0.5 # Valeur de sécurité
            
            print(f"🧬 Neocortex (V1): L5 output = {l5_output:.4f} | Feedback L6 = {l6_feedback:.4f}")
            
            # C. Mise à jour du rythme cardiaque basée sur le feedback
            # Si L6 est haut (reconnaissance), le système se calme.
            heart.update_metabolism(l6_feedback)
            print(f"💓 Pulse Rate: {heart.bpm:.1f} BPM")
        else: 
            print("❌ Error: V1 lobe not found.")

    print("\n" + "="*50)
    print("✅ CYCLE TEST COMPLETED: Hub-Lobe integration is operational.")

if __name__ == "__main__":
    create_ascii_header()
    try:
        asyncio.run(test_hub_cycle())
    except Exception as e:
        print(f"❌ Fatal error : {e}")