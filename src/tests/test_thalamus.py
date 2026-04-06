#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
aNA AI Project - v5.1

Module: Test Thalamus 

Description: This test is designed to validate the core functionalities of the thalamus module in complete isolation. It simulates a simple data stream to verify that the thalamus processes inputs correctly, integrates feedback from the hippocampus, and modulates outputs based on chemical states. The test covers sensory processing, thalamo-cortical gain modulation, and the influence of neuromodulators on thalamic function.

Architecture and neuroinformatics: Theriault Benoit
"""
import unittest
import numpy as np
import asyncio
import time
import os
import sys

# On définit la racine du projet dynamiquement
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from core.pulse import Pulse
from anatomy.subcortical.thalamus import Thalamus
from anatomy.limbic.hippocampus import Hippocampus
from anatomy.base.neuromodulator import Neuromodulator
from registry import ORGANS

def create_ascii_header():
    print(f"\033c") 
    print("░                     ░░░░░░░░░░▒▒▒▒▒▒░░")
    print("           ░░░░░░░░░▒▒▒▒▒▓▒▒▒▒░░░░░░░░░░▒▒▒▒░                                                          ░░░░░░░░░░░")
    print("░░░░░░░░░░░░░░░░▒▒▒▒▓▓▓▓▓▓▓▓▓▓▓▒░░░░░▒▒▒░░░░▒▓▒░░                      ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░")
    print("░░░░░░░░░░░░░░▒▒▒▓▓▓▓▓▓▓▓▓▓▓▒░░▒▒▒░░░░▒▓▓▓▓▓▓▒▒▒▒▒░     ░░░░░░░░░░░░░░░░░░░░░▒▒░░▒▒▒▓▓▓▓▓▓▒▒▒░░░░░░░░░░░░░░░░░▒▒▒▒")
    print("▒░░░░░▒▒▒▒▒▒▓▓▓▓▓▓▓▓▓▒░         ░░▒▒▒░▒▒▒▒▓▓▓▓▓▓▓▒▒░░  ░▒▒▒▓▒▒▒▓▒▓▒▓▒░░░░░░░▒▓▓▓▓▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░░░░░░░░░░░▒▓")
    print("░▒▒▒▒▓▓▓▓▓▓▓▓▓▓▓▓░                   ░░ ▒▒▓▒░▒▓▓▓░▒▒░░           ░▒░░░▒▓▒▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒▒▓▓")
    print("▒▒▓▓▓▓▓▓▒▒▒░░                           ░▓▓▒░░▒▓▓░ _    _    _ ░▒░░▒▓▒▓▓▓▓▓▓▓▓▓▓▒░░░░░░░░░▒▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓")
    print("▓▓▓▓▓▒░AI inspired by natural plasticity ░░   ░░░  a    N    A  ▒▓▒▓▒▒▒▓░Autonomous Neural Architecture v5.1 ░░▒▒▓")
    print("░                                                  ‾    ‾    ‾ ░▓▒▓░░▒▓░\n\n")

async def test_sensory_cascade():
    # 1. Création des Mocks (Simulacres)
    # On crée des objets simples qui imitent le comportement attendu
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
            # On retire le print ici aussi pour ne plus voir le doublon
            # print(f"  [Pulse] New BPM: {bpm:.2f}") 
            pass

    # 2. Instanciation des composants v5.1
    #from anatomy.base.neuromodulator import Neuromodulator
    
    mock_hippo = MockHippo()
    mock_pulse = MockPulse()
    neuromod_core = Neuromodulator()

    # 3. Initialisation du Thalamus avec les objets réels
    thalamus = Thalamus(
        hippocampus=mock_hippo, 
        pulse=heart, 
        neuromodulator_core=neuromod_core
    )

    print("--- 🧠 aNA v5.1 : Thalamo-Cortical Integration Test ---")
    
    stimuli = [
        {"nucleus": "MGN", "signal_label": "A", "intensity": 0.8},
        {"nucleus": "MGN", "signal_label": "N", "intensity": 0.8},
        {"nucleus": "MGN", "signal_label": "A", "intensity": 0.9}
    ]

    for i, stimulus in enumerate(stimuli):
        print(f"\nCycle {i+1} | Input: {stimulus['signal_label']} via {stimulus['nucleus']}")
        
        # Simulation d'un feedback L6 (ex: 0.2 pour un signal nouveau, 0.8 pour connu)
        l6_mock = 0.2 # 0.5

        # Appel corrigé avec les deux arguments requis par la v5.1
        result = await thalamus.process_payload(stimulus, l6_feedback=l6_mock)
        
        # dt = heart.compute_dynamics()
        print(f"  [Thalamus] Result: {result}")
        # print(f"  [Chimie] Noradrénaline: {neuromod_core.get_matrix()['noradrenaline']:.2f}")
        print(f"  [Pulse]  Frequence: {result['bpm']:.2f} BPM")
        matrix = neuromod_core.get_matrix()
        print(f"  [Neuromodulator] Dopa: {matrix['dopamine']:.3f} | Nora: {matrix['noradrenaline']:.3f}")
        print(f"  [Gain]   Thalamic: {result['thalamic_gain']:.3f}")
        await asyncio.sleep(0.5) # On laisse le temps à la dopamine de "vivre"

    # --- 🌅 CYCLE COMPLET : DE LA PANIQUE À LA SAGESSE (v5.1) ---
    print("\n" + "="*50)
    print(" 🧠 PHASE 1: REACTION UNDER FATIGUE (Stress)")
    print("="*50)
    
    # 1. On prépare un stimulus de "Danger" (ex: Signal 'D')
    stimulus_danger = {"signal_label": "D", "nucleus": "MGN", "intensity": 0.8}
    
    # On simule un ATP bas (0.3) mais pas encore critique
    heart.atp = 0.3
    l6_mock = 0.2 # Faible contrôle cortical car fatigué
    
    result_stress = await thalamus.process_payload(stimulus_danger, l6_feedback=l6_mock)
    print(f"  [Action] Reaction to danger (Fatigue): {result_stress['bpm']:.2f} BPM")
    # Ici, tu devrais voir un pic autour de 140 BPM.

    print("\n" + "="*50)
    print(" 💤 PHASE 2: NOCTURNAL CONSOLIDATION (Rest)")
    print("="*50)
    
    # 2. Effondrement et Sommeil
    heart.atp = 0.1
    heart.compute_dynamics() # Active is_refractory = True
    
    if heart.is_refractory:
        print(f"  [Pulse] Refractory mode activated. BPM: {heart.bpm}")
        # On simule l'appel de l'Hippocampe que nous avons codé
        await thalamus.hippo.consolidate_and_prune()

    print("\n" + "="*50)
    print(" ☀️ PHASE 3: AWAKENING AND WISDOM")
    print("="*50)
    
    # 3. Restauration de l'énergie
    heart.atp = 1.0
    heart.is_refractory = False
    heart.bpm = 110.0 # Rythme de base
    print("  [Pulse] Energy restored to 100%. aNA is fresh.")

    # 4. On renvoie LE MÊME stimulus de danger
    print("  [Action] Facing the same danger after rest...")
    result_sagesse = await thalamus.process_payload(stimulus_danger, l6_feedback=0.5)
    
    print(f"  [Result] BPM after consolidation: {result_sagesse['bpm']:.2f} BPM")

if __name__ == "__main__":
    create_ascii_header()  
    asyncio.run(test_sensory_cascade())
