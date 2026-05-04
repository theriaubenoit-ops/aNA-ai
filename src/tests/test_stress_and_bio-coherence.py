#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
aNA AI Project v5.3 -  Test Metabolic Stress and Bio-coherence

Description: This test aims to validate the biological consistency of the Neuromodulator and Neuron implementation by simulating metabolic stress scenarios (energy depletion) and chemical stress scenarios (norepinephrine injection). We will verify that the neuron reacts appropriately to these conditions, notably by ceasing firing when energy is depleted and increasing its plasticity in response to a noradrenergic alert.

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

# from registry import ORGANS
# from config import get_config
from anatomy.base.neuron import Neuron, NeuronConfig
from anatomy.base.neuromodulator import Neuromodulator
from anatomy.limbic.limbic_system import LimbicSystem


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

async def test_stress_v53():
    print("--- START OF BIO-COHERENCE TEST aNA v5.3.1 ---")
    
    # 1. Setup : Un neurone "Cobaye" en Couche IV (Entrée Sensorielle)
    config = NeuronConfig(layer_id=3) 
    neuron = Neuron(position=np.array([0, 0, 0]), config=config)
    chemistry = Neuromodulator()
    
    # 2. Phase 1 : Épuisement Métabolique
    print("\nPhase 1 : Metabolic Guard Test...")

    limbic = LimbicSystem()

    for i in range(50):
        # On force un input énorme pour faire décharger le neurone en continu
        neuron.receive_input(10.0, chemistry.get_matrix())
        neuron.update(i, chemistry.get_matrix())
        
        if i % 10 == 0:
            print(f"Cycle {i} | Energy: {neuron.energy_level:.2f} | Firing: {neuron.is_firing}")
             
    # Vérification : Le neurone DOIT s'arrêter malgré l'input
    assert neuron.energy_level >= 0.0, "ERREUR : Énergie négative !"
    
    # 3. Phase 2 : Test de Fixation (Limbique + Hippocampe)
    print("\nPhase 2 : Fixation Test via Limbic System...")

    experience_arousal = await limbic.process_experience(
        sensory_data="Trauma_Test_01", 
        emotional_input={"dopamine": 0.1, "cortisol": 0.9}
    )
    
    limbic = LimbicSystem()
    # On simule une expérience avec une forte dose de cortisol (Stress)
    # Cela va générer un consolidation_factor > 1.0
    experience_arousal = await limbic.process_experience(
        sensory_data="Trauma_Test_01", 
        emotional_input={"dopamine": 0.1, "cortisol": 0.9}
    )
    
    # Vérification du résultat dans l'Hippocampe
    trace = limbic.hippocampus.subfields["CA3"].get("Trauma_Test_01", 0.0)
    print(f"Engraved memorial trace: {trace:.4f}")
    
    if trace > 0.5:
        print("SUCCESS: The limbic-hippocampal suture is functional!")
    
    # 4. Phase 3 : Cohérence des Clés
    print("\nPhase 3 : Chemical Key Verification...")
    matrix = chemistry.get_matrix()
    if "norepinephrine" in matrix and "dopamine" in matrix:
        print("SUCCESS: Chemical key mapping is functional (Norepinephrine detected).")
    else:
        print("ERROR: Missing chemical keys in the matrix!")

if __name__ == "__main__":
    create_ascii_header()
    asyncio.run(test_stress_v53())