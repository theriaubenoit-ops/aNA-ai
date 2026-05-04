#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Project aNA AI v5.2 - Test Thalamus

Description : Ce test est conçu pour valider les fonctionnalités de base du module thalamus en isolement complet. Il simule un flux de données simple pour vérifier que le thalamus traite correctement les entrées, intègre les commentaires de l'hippocampe et module les sorties en fonction des états chimiques. Le test couvre le traitement sensoriel, la modulation du gain thalamo-cortical et l'influence des neuromodulateurs sur la fonction thalamique.

Architecture et neuroinformatique : Thériault Benoit
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
from config import get_config
from registry import ORGANS
    
def create_ascii_header():
    print(f"\033c") 
    print("░              ░ ░░░▒▒▓▒▓▒▒▒▒▒░░▒▒░▒▒▒▓▒▓▒                                                                     ░ ░")
    print("▒░░   ░░░░░░░░░░▒▒▓▓▓▓▓▓▓██▓▒▒▒░░░▒▒▒▒▒░░░▒▒▓▓▒                                                         ░░░░░░▒▒▒▒")
    print("░░░░░░░░░░░░░▒▒▒▓▓▓▓▓▓██████▓▓▒▒▒░░▒▒▓▓▓▒▒▒░░▒▒▒▒▓▒                                        ░ ░░░ ░ ░░░░░░░░░▒▒▒▒▒▒")
    print("▓▒▒▒▒▒▒▒▒▓▒▓▓▓▓▓▓██████▓▒▒ ▒   ▒▓▒▓▒▒▒▒▓▒▓ ██▓▓▓▒▒▒▒▓      ░░▒▒▒▒▒▒▒░░░░░░▒░░░░▒▒░░▒░░░░░░░░░░░░░░░░░▒░▒▒▒░▒▒▒▓▓▓▓")
    print("▒▒▒▒▒▒▒▓▓▓▓▓████▓▓░                 ░░▒▒▒▓█▓░▓▓█▓▓ ░▒▓  ▒▓▓▓▓▓█▓▓▓█▓▒▒▒▓▓▒░░░░▒▓█▓▓▓▓▓▒▓▒▒▒▒▒▒▒░░░░░░░░░░░░░░▒▒▒▒▒")
    print("▒▒▓▒▓▓▓▓█████▓▓▒                        ░▒▒▓░ ▓██▓                ▒▓▒▒░░▒▓▒░░▒▓███▓█▓▓▓▓▓▓▓▓▓▓▓▒▓▒▒▒▒▒▒▒▒▒▒▓▒▓▓▓▓▓")
    print("▓▓▓█████▓░                                    ░░▒▒ _    _    _ ░▒░▒▒▒▓▒▓▒▓▒▓█▓███▓▒▓▓▓▓▓▓▓▓▓▓▓▓█▓██▓▓▓▓▓█▓████████")
    print("▓███▓▒  IA inspirée de la plasticité naturelle ✴️  a    N    A  ▒▓█▒▓ ▒▓█▒Architecture Neuronale Autonome v5.3 ▒▓▓")
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

    print("--- 🧠 Test d'intégration thalamo-corticale ---")
    
    stimuli = [
        {"nucleus": "MGN", "signal_label": "A", "intensity": 0.8},
        {"nucleus": "MGN", "signal_label": "N", "intensity": 0.8},
        {"nucleus": "MGN", "signal_label": "A", "intensity": 0.9}
    ]

    for i, stimulus in enumerate(stimuli):
        print(f"\nCycle {i+1} | Entrée : {stimulus['signal_label']} via {stimulus['nucleus']}")
        
        l6_mock = 0.6

        # Appel corrigé avec les deux arguments requis par la v5.1
        result = await thalamus.process_payload(stimulus, neurom, l6_feedback=l6_mock)

        print(f"  [Thalamus] Résultat : {result}")
        if "bpm" in result:
            print(f"  [Impulsion]  Fréquence : {result['bpm']:.2f} BPM")
        else:
            print(f"  [Striatum] Action bloquée : {result['status']}")

        await asyncio.sleep(0.1) # On laisse le temps à la dopamine de "vivre"

    print("\n" + "="*50)
    print(" 🧠 PHASE 1 : RÉACTION SOUS FATIGUE (Stress)")
    print("="*50)
    
    # 1. On prépare un stimulus de "Danger" (ex: Signal 'D')
    stimulus_danger = {"signal_label": "D", "nucleus": "MGN", "intensity": 0.8}
    
    # On simule un ATP bas (0.3) mais pas encore critique
    heart.atp = 0.3
    l6_mock = 0.2 # Faible contrôle cortical car fatigué
    
    result_stress = await thalamus.process_payload(stimulus, neurom, l6_feedback=l6_mock)
    if "bpm" in result_stress:
        print(f"  [Action] Réaction au danger (Fatigue): {result_stress['bpm']:.2f} BPM")
    else:
        print(f"  [Striatum] Action bloquée : {result_stress['status']}")

    print("\n" + "="*50)
    print(" 💤 PHASE 2 : CONSOLIDATION NOCTURNE (Repos)")
    print("="*50)
    
    # 2. Effondrement et Sommeil
    heart.atp = 0.1
    heart.compute_dynamics() 
    
    if heart.is_refractory:
        print(f"  [Pulse] Mode réfractaire activé. BPM: {heart.bpm}")
        # On simule l'appel de l'Hippocampe que nous avons codé
        await thalamus.hippo.consolidate_and_prune()

    print("\n" + "="*50)
    print(" ☀️ PHASE 3 : LE RÉVEIL ET LA SAGESSE")
    print("="*50)
    
    heart.atp = 1.0
    heart.is_refractory = False
    heart.bpm = 110.0
    result_sagesse = await thalamus.process_payload(stimulus, neurom, l6_feedback=l6_mock)
    if "bpm" in result_sagesse:
    
        print(f"  [Résultat] BPM après consolidation: {result_sagesse['bpm']:.2f} BPM")
    else:
        print(f"  [Striatum] Action bloquée : {result_sagesse['status']}")


    print("\n  *Chaque mesure présentée ici est un pont numérique vers la réalité biologique,")
    print("   conçu pour synthétiser les principes fondamentaux des systèmes vivants.\n")
    

if __name__ == "__main__":
    create_ascii_header()
    asyncio.run(test_sensory_cascade())
