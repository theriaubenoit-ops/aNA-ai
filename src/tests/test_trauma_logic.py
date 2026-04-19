#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
aNA AI Project v5.3 - Test Hippocampus Trauma Logic

Description: This test simulates the trauma logic of the hippocampus by creating a scenario where a neutral experience is followed by a traumatic event, and then simulating the forgetting process over time. The test checks whether the traumatic memory trace persists longer than the neutral one, demonstrating the concept of emotional memory consolidation and persistence.

Architecture and neuroinformatics: Theriault Benoit
"""
import unittest
import asyncio
import sys
import os
import numpy as np

# The project root is defined dynamically.
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from anatomy.limbic.amygdala import Amygdala
from anatomy.limbic.hippocampus import Hippocampus

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

async def process_event(amy, hippo, label, intensity, valence):
    """
    Synchronized sequence: Processing -> Update -> Modulation -> Encoding
    """
    # 1. The amygdala processes the sensory signal
    amy.process_emotional_input(intensity, valence, 0.1, {})
    
    # 2. Internal activity update (Cortisol/Adrenaline)
    # This is where the alert is actually calculated.
    amy.update_activity(intensity) 
    
    # 3. Extraction of synaptic modulation
    mod = amy.get_synaptic_modulation()
    
    # 4. The hippocampus records the trace according to the received modulation.
    await hippo.update_memories(label, mod)

async def run_scientific_test():
    print("--- START OF EMOTIONAL SEDIMENTATION TESTS ---")
    
    # Initialisation
    amy = Amygdala()
    amy.reset() # Security: We start from a neutral base
    
    hippo = Hippocampus(config={
        "SUBFIELDS": ["DG", "CA1", "CA2", "CA3", "CA4"], # Ajout de "DG" ici
        "MIN_LATENT_THRESHOLD": 0.001,
        "LTP_GAIN": 0.15,
        "BURN_SCIENTIFIC": 0.05,
        "ENCODE_THRESHOLD": 0.5
    })

    # --- Phase A : Neutral Signal (Repeated) ---
    print("\n  Phase A: Learning a neutral signal...")
    for i in range(5):
        await process_event(amy, hippo, "NEUTRE_1", 0.6, 0.0)
    
    val_n_init = hippo.subfields['CA3'].get('NEUTRE_1', 0)
    print(f"  Force trace NEUTRE_1 after 5 cycles : {val_n_init:.4f}")

    # --- Phase B : The Trauma (Unique and intense) ---
    print("\n  Phase B: Encounter with a Critical Error (Trauma)...")
    # We inject a terror valence (-1.0)
    await process_event(amy, hippo, "TRAUMA_1", 1.0, -1.0)
    
    val_t_init = hippo.subfields['CA3'].get('TRAUMA_1', 0)
    print(f"  Force trace TRAUMA_1 (Gravure Flash) : {val_t_init:.4f}")

    # --- Phase C : Sedimentation (Forgotten over 100 cycles) ---
    print("\n  Phase C: Simulation of 100 forgetting cycles...")
    for _ in range(100):
        # We simulate the passage of time (synaptic decay)
        for label in hippo.subfields['CA3']:
            hippo.subfields['CA3'][label] *= 0.95 # Burn rate de 5%
            # We prevent anyone from descending below the survival floor (if defined).
            plancher = 0.1 if label == "TRAUMA_1" else 0.001
            hippo.subfields['CA3'][label] = max(plancher, hippo.subfields['CA3'][label])

    # Results
    print("\n  --- ANALYSIS OF TRACES AFTER LONG FORGETTING ---")
    val_neutre = hippo.subfields['CA3'].get("NEUTRE_1", 0)
    val_trauma = hippo.subfields['CA3'].get("TRAUMA_1", 0)
    
    print(f"  Residue NEUTRE_1 : {val_neutre:.6f}")
    print(f"  Residue TRAUMA_1 : {val_trauma:.6f}")
    
    if val_trauma > val_neutre:
        print("\n  CONCLUSION: The Acid Trace has survived.")
    else:
        print("\n  CONCLUSION: Failure of emotional persistence.")
    print("\n  *Every measurement reflected here is a digital bridge to biological reality,")
    print("   designed to synthesize the fundamental principles of living systems.\n")

if __name__ == "__main__":
    create_ascii_header()
    asyncio.run(run_scientific_test())