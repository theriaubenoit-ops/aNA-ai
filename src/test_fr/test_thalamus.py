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
    

async def test_sensory_cascade():
    # 1. Création des Mocks (Simulacres)
    # On crée des objets simples qui imitent le comportement attendu
    class MockHippo:
        async def evaluate_prediction(self, label): return 0.2
    # class MockHippo:
    #    async def evaluate_prediction(self, label): return 0.9  # 90% d'erreur
        
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
        pulse=mock_pulse, 
        neuromodulator_core=neuromod_core
    )

    print("--- 🧠 aNA v5.1 : Test d'intégration thalamo-corticale ---")
    
    stimuli = [
        {"nucleus": "MGN", "signal_label": "A", "intensity": 0.8},
        {"nucleus": "MGN", "signal_label": "N", "intensity": 0.8},
        {"nucleus": "MGN", "signal_label": "A", "intensity": 0.9}
    ]

    for i, stimulus in enumerate(stimuli):
        print(f"\nCycle {i+1} | Entrée : {stimulus['signal_label']} via {stimulus['nucleus']}")
        
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

    # Test du mode RECEPTIVE (épuisement volontaire)
    print("\n--- 💤 Simulation d'épuisement métabolique (v5.1) ---")
    # On simule l'épuisement via le Neuromodulator si vous avez une clé 'atp' 
    # ou on baisse simplement la dopamine/adrénaline
    neuromod_core.update_from_limbic({"dopamine": -0.3, "noradrenaline": -0.05})
    
    matrix = neuromod_core.get_matrix()
    print(f"  [Statut] Énergie en baisse | Dopamine : {matrix['dopamine']:.3f}")
    print(f"  📡 Sortie (ATP Bas) | {result}")

if __name__ == "__main__":
    asyncio.run(test_sensory_cascade())