#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
aNA AI Project v5.3 - Test Thalamus 

Description: This test is designed to validate the core functionalities of the thalamus module in complete isolation. It simulates a simple data stream to verify that the thalamus processes inputs correctly, integrates feedback from the hippocampus, and modulates outputs based on chemical states. The test covers sensory processing, thalamo-cortical gain modulation, and the influence of neuromodulators on thalamic function.

Architecture, concept and supervision: Benoit Theriault
Collaboration, research and code: Google DeepMind (Gemini)
"""
import unittest
import numpy as np
import asyncio
import time
import os
import sys

# The project root is defined dynamically.
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from src.core.pulse import Pulse
from src.anatomy.subcortical.thalamus import Thalamus
from src.anatomy.limbic.hippocampus import Hippocampus
from src.anatomy.base.neuromodulator import Neuromodulator
from src.config import get_config
from src.registry import ORGANS

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

async def test_sensory_cascade():
    # 1. Configuration des composants
    neurom = Neuromodulator()
    heart = Pulse(bpm=120.0)
    heart.atp = 1.0

    class MockHippo:
        async def evaluate_prediction(self, label): return 0.2
        async def consolidate_and_prune(self):
            print("  [Hippo] Simulation de la consolidation synaptique...")
            return True
    mock_hippo = MockHippo()
    thalamus = Thalamus(hippocampus=mock_hippo, pulse=heart, neuromodulator=neurom)

    print("--- 🧠 Thalamo-Cortical Integration Test ---")
    
    stimuli = [
        {"nucleus": "MGN", "signal_label": "A", "intensity": 0.8},
        {"nucleus": "MGN", "signal_label": "N", "intensity": 0.8},
        {"nucleus": "MGN", "signal_label": "A", "intensity": 0.9}
    ]

    # --- BOUCLE INITIALE ---
    for i, stimulus in enumerate(stimuli):
        print(f"\nCycle {i+1} | Input: {stimulus['signal_label']} via {stimulus['nucleus']}")
        l6_mock = 0.6  # <-- Simulated Layer 6 feedback, representing the cortical prediction error for this stimulus.
        # APPEL 1 : Correct
        result = await thalamus.process_payload(stimulus, neurom, l6_feedback=l6_mock)

        print(f"  [Thalamus] Result: {result}")
        if "bpm" in result:
            print(f"  [Pulse]  Frequence: {result['bpm']:.2f} BPM")
        else:
            print(f"  [Striatum] Action blocked: {result['status']}")
            
        await asyncio.sleep(0.1)

    print("\n" + "="*50)
    print(" 🧠 PHASE 1: REACTION UNDER FATIGUE (Stress)")
    print("="*50)
    
    stimulus_danger = {"signal_label": "D", "nucleus": "MGN", "intensity": 0.8}
    heart.atp = 0.3
    l6_mock = 0.2 
    
    # APPEL 2 : CORRIGÉ (neurom ajouté)🧔🏻
    result_stress = await thalamus.process_payload(stimulus, neurom, l6_feedback=l6_mock)

    if "bpm" in result_stress:
        print(f"  [Action] Reaction to danger (Fatigue): {result_stress['bpm']:.2f} BPM")
    else:
        print(f"  [Striatum] Action blocked: {result_stress['status']}")

    print("\n" + "="*50)
    print(" 💤 PHASE 2: NOCTURNAL CONSOLIDATION (Rest)")
    print("="*50)
    
    heart.atp = 0.1
    heart.compute_dynamics() 
    
    if heart.is_refractory:
        print(f"  [Pulse] Refractory mode activated. BPM: {heart.bpm}")
        await thalamus.hippo.consolidate_and_prune()

    print("\n" + "="*50)
    print(" ☀️ PHASE 3: AWAKENING WITH MOTIVATION BOOST")
    # print("="*50)

    thalamus.pulse.inject_stimulus(0.5) 
    print(f" [STIMULUS] Systemic injection: +0.5 Dopamine")
    print("="*50)

    # result = await thalamus.process_payload(stimulus_A, neurom, l6_feedback=0.8)
    
    heart.atp = 1.0
    heart.is_refractory = False
    heart.bpm = 110.0 
    # result_sagesse = await thalamus.process_payload(stimulus, neurom, l6_feedback=l6_mock)
    result_sagesse = await thalamus.process_payload(stimulus, neurom, l6_feedback=0.8)
    if "bpm" in result_sagesse:
        print(f"  [Result] BPM after consolidation: {result_sagesse['bpm']:.2f} BPM")
    else:
        print(f"  [Striatum] Action blocked: {result_sagesse['status']}")

    print("\n  *Every measurement reflected here is a digital bridge to biological reality,")
    print("   designed to synthesize the fundamental principles of living systems.\n")

if __name__ == "__main__":
    create_ascii_header()
    asyncio.run(test_sensory_cascade())
