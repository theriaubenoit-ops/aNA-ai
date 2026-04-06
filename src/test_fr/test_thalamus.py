#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Projet aNA AI - v5.1
Module : Test Thalamus
La description : Ce test est conçu pour valider les fonctionnalités de base du module thalamus en isolement complet. Il simule un flux de données simple pour vérifier que le thalamus traite correctement les entrées, intègre les commentaires de l'hippocampe et module les sorties en fonction des états chimiques. Le test couvre le traitement sensoriel, la modulation du gain thalamo-cortical et l'influence des neuromodulateurs sur la fonction thalamique.
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
    print("▓▓▓░IA inspirée de la plasticité naturelle░░  ░░░  a    N    A  ▒▓▒▓▒▒▒▓░Architecture Neuronale Autonome v5.1░░▒▒▓")
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
            # On retire le print ici aussi pour ne plus voir le doublon
            # print(f"  [Impulsion] Nouveau BPM: {bpm:.2f}") 
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

    print("--- 🧠 aNA v5.1 : Test d'intégration thalamo-corticale ---")
    
    stimuli = [
        {"nucleus": "MGN", "signal_label": "A", "intensity": 0.8},
        {"nucleus": "MGN", "signal_label": "N", "intensity": 0.8},
        {"nucleus": "MGN", "signal_label": "A", "intensity": 0.9}
    ]

    for i, stimulus in enumerate(stimuli):
        print(f"\nÉtape {i+1} | Entrée : {stimulus['signal_label']} via {stimulus['nucleus']}")
        
        # Simulation d'un feedback L6 (ex: 0.2 pour un signal nouveau, 0.8 pour connu)
        l6_mock = 0.2 # 0.5

        # Appel corrigé avec les deux arguments requis par la v5.1
        result = await thalamus.process_payload(stimulus, l6_feedback=l6_mock)
        
        # dt = heart.compute_dynamics()
        print(f"  [Thalamus] Résultat : {result}")
        # print(f"  [Chimie] Noradrénaline : {neuromod_core.get_matrix()['noradrenaline']:.2f}")
        print(f"  [Impulsion]  Fréquence : {result['bpm']:.2f} BPM")
        matrix = neuromod_core.get_matrix()
        print(f"  [Neuromodulateur] Dopamine : {matrix['dopamine']:.3f} | Noradrénaline : {matrix['noradrenaline']:.3f}")
        print(f"  [Gain]   Thalamic : {result['thalamic_gain']:.3f}")
        await asyncio.sleep(0.5) # On laisse le temps à la dopamine de "vivre"

    # --- 🌅 CYCLE COMPLET : DE LA PANIQUE À LA SAGESSE (v5.1) ---
    print("\n" + "="*50)
    print(" 🧠 PHASE 1 : RÉACTION SOUS FATIGUE (Stress)")
    print("="*50)
    
    # 1. On prépare un stimulus de "Danger" (ex: Signal 'D')
    stimulus_danger = {"signal_label": "D", "nucleus": "MGN", "intensity": 0.8}
    
    # On simule un ATP bas (0.3) mais pas encore critique
    heart.atp = 0.3
    l6_mock = 0.2 # Faible contrôle cortical car fatigué
    
    result_stress = await thalamus.process_payload(stimulus_danger, l6_feedback=l6_mock)
    print(f"  [Action] Réaction au danger (Fatigue): {result_stress['bpm']:.2f} BPM")
    # Ici, tu devrais voir un pic autour de 140 BPM.

    print("\n" + "="*50)
    print(" 💤 PHASE 2 : CONSOLIDATION NOCTURNE (Repos)")
    print("="*50)
    
    # 2. Effondrement et Sommeil
    heart.atp = 0.1
    heart.compute_dynamics() # Active is_refractory = True
    
    if heart.is_refractory:
        print(f"  [Pulse] Mode réfractaire activé. BPM: {heart.bpm}")
        # On simule l'appel de l'Hippocampe que nous avons codé
        await thalamus.hippo.consolidate_and_prune()

    print("\n" + "="*50)
    print(" ☀️ PHASE 3 : LE RÉVEIL ET LA SAGESSE")
    print("="*50)
    
    # 3. Restauration de l'énergie
    heart.atp = 1.0
    heart.is_refractory = False
    heart.bpm = 110.0 # Rythme de base
    print("  [Pulse] Énergie restaurée à 100%. William est frais.")

    # 4. On renvoie LE MÊME stimulus de danger
    print("  [Action] Confrontation au même danger après repos...")
    result_sagesse = await thalamus.process_payload(stimulus_danger, l6_feedback=0.5)
    
    print(f"  [Résultat] BPM après consolidation: {result_sagesse['bpm']:.2f} BPM")
    

if __name__ == "__main__":
    create_ascii_header()
    asyncio.run(test_sensory_cascade())
