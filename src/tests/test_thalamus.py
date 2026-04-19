#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
aNA AI Project v5.3 - Test Thalamus 

Description: This test is designed to validate the core functionalities of the thalamus module in complete isolation. It simulates a simple data stream to verify that the thalamus processes inputs correctly, integrates feedback from the hippocampus, and modulates outputs based on chemical states. The test covers sensory processing, thalamo-cortical gain modulation, and the influence of neuromodulators on thalamic function.

Architecture and neuroinformatics: Theriault Benoit
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

from core.pulse import Pulse
from anatomy.subcortical.thalamus import Thalamus
from anatomy.limbic.hippocampus import Hippocampus
from anatomy.base.neuromodulator import Neuromodulator
# from registry import ORGANS
from config import get_config
from registry import ORGANS

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
    # 1. Creating Mocks (Simulacra)
    # We create simple objects that mimic the expected behavior
    neuromod_core = Neuromodulator()
    heart = Pulse(bpm=120.0)
    heart.atp = 1.0

    class MockHippo:
        async def evaluate_prediction(self, label): return 0.2
    #    async def evaluate_prediction(self, label): return 0.9  # 90% d'erreur

        async def consolidate_and_prune(self):
            print("  [MockHippo] Simulation de la consolidation synaptique...")
            return True
        
    class MockPulse:
        def update_frequency(self, bpm):
            self.bpm = new_bpm
            # We're removing the print here too to avoid seeing the duplicate.
            # print(f"  [Pulse] New BPM: {bpm:.2f}") 
            pass

    # 2. Component Instantiation
    #from anatomy.base.neuromodulator import Neuromodulator
    
    mock_hippo = MockHippo()
    mock_pulse = MockPulse()
    neuromod_core = Neuromodulator()

    # 3. Thalamus initialization with real objects
    thalamus = Thalamus(
        hippocampus=mock_hippo, 
        pulse=heart, 
        neuromodulator_core=neuromod_core
    )

    print("--- 🧠 Thalamo-Cortical Integration Test ---")
    
    stimuli = [
        {"nucleus": "MGN", "signal_label": "A", "intensity": 0.8},
        {"nucleus": "MGN", "signal_label": "N", "intensity": 0.8},
        {"nucleus": "MGN", "signal_label": "A", "intensity": 0.9}
    ]

    for i, stimulus in enumerate(stimuli):
        print(f"\nCycle {i+1} | Input: {stimulus['signal_label']} via {stimulus['nucleus']}")
        
        # Simulation of an L6 feedback (e.g., 0.2 for a new signal, 0.8 for a known signal)
        l6_mock = 0.2 # 0.5

        # Corrected call with the two required arguments
        result = await thalamus.process_payload(stimulus, l6_feedback=l6_mock)
        
        # dt = heart.compute_dynamics()
        print(f"  [Thalamus] Result: {result}")
        # print(f"  [Chemistry] Norepinephrine: {neuromod_core.get_matrix()['noradrenaline']:.2f}")
        print(f"  [Pulse]  Frequence: {result['bpm']:.2f} BPM")
        matrix = neuromod_core.get_matrix()
        print(f"  [Neuromodulator] Dopamine: {matrix['dopamine']:.3f} | Noradrenaline: {matrix['noradrenaline']:.3f}")
        print(f"  [Gain]   Thalamic: {result['thalamic_gain']:.3f}")
        await asyncio.sleep(0.5) # We allow time for dopamine to "live".

    # --- 🌅 COMPLETE CYCLE: FROM PANIC TO WISDOM ---
    print("\n" + "="*50)
    print(" 🧠 PHASE 1: REACTION UNDER FATIGUE (Stress)")
    print("="*50)
    
    # 1. We prepare a "Danger" stimulus (e.g., Signal 'D')
    stimulus_danger = {"signal_label": "D", "nucleus": "MGN", "intensity": 0.8}
    
    # We simulate a low ATP level (0.3) but not yet critical
    heart.atp = 0.3
    l6_mock = 0.2 # Poor cortical control due to fatigue
    
    result_stress = await thalamus.process_payload(stimulus_danger, l6_feedback=l6_mock)
    print(f"  [Action] Reaction to danger (Fatigue): {result_stress['bpm']:.2f} BPM")
    # Here, he should see a peak around 140 BPM.

    print("\n" + "="*50)
    print(" 💤 PHASE 2: NOCTURNAL CONSOLIDATION (Rest)")
    print("="*50)
    
    # 2. Collapse and Sleep
    heart.atp = 0.1
    heart.compute_dynamics() # Active is_refractory = True
    
    if heart.is_refractory:
        print(f"  [Pulse] Refractory mode activated. BPM: {heart.bpm}")
        # We simulate the Hippocampus call that we coded
        await thalamus.hippo.consolidate_and_prune()

    print("\n" + "="*50)
    print(" ☀️ PHASE 3: AWAKENING AND WISDOM")
    print("="*50)
    
    # 3. Energy restoration
    heart.atp = 1.0
    heart.is_refractory = False
    heart.bpm = 110.0 # Basic rhythm
    print("  [Pulse] Energy restored to 100%. aNA is fresh.")

    # 4. We are sending back THE SAME danger stimulus
    print("  [Action] Facing the same danger after rest...")
    result_sagesse = await thalamus.process_payload(stimulus_danger, l6_feedback=0.5)
    
    print(f"  [Result] BPM after consolidation: {result_sagesse['bpm']:.2f} BPM")
    print("\n  *Every measurement reflected here is a digital bridge to biological reality,")
    print("   designed to synthesize the fundamental principles of living systems.\n")

if __name__ == "__main__":
    create_ascii_header()  
    asyncio.run(test_sensory_cascade())
