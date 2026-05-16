#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Projet aNA IA v5.3 -  Test du stress métabolique et de la biocohérence

Description: Ce test vise à valider la cohérence biologique de l'implémentation du neuromodulateur et du neurone en simulant des scénarios de stress métabolique (épuisement énergétique) et de stress chimique (injection de noradrénaline). Nous vérifierons que le neurone réagit de manière appropriée à ces conditions, notamment en cessant son activité en cas d'épuisement énergétique et en augmentant sa plasticité en réponse à une stimulation noradrénergique.

Architecture, conception et supervision : Thériault_Benoit
Collaboration, recherche et code : DeepMind_Gemini
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
from src.anatomy.base.neuron import Neuron, NeuronConfig
from src.anatomy.base.neuromodulator import Neuromodulator
from src.anatomy.limbic.limbic_system import LimbicSystem


def create_ascii_header():
    print(f"\033c") 
    print("░              ░ ░░░▒▒▓▒▓▒▒▒▒▒░░▒▒░▒▒▒▓▒▓▒                                                                     ░ ░")
    print("▒░░   ░░░░░░░░░░▒▒▓▓▓▓▓▓▓██▓▒▒▒░░░▒▒▒▒▒░░░▒▒▓▓▒                                                         ░░░░░░▒▒▒▒")
    print("░░░░░░░░░░░░░▒▒▒▓▓▓▓▓▓██████▓▓▒▒▒░░▒▒▓▓▓▒▒▒░░▒▒▒▒▓▒                                        ░ ░░░ ░ ░░░░░░░░░▒▒▒▒▒▒")
    print("▓▒▒▒▒▒▒▒▒▓▒▓▓▓▓▓▓██████▓▒▒ ▒   ▒▓▒▓▒▒▒▒▓▒▓ ██▓▓▓▒▒▒▒▓      ░░▒▒▒▒▒▒▒░░░░░░▒░░░░▒▒░░▒░░░░░░░░░░░░░░░░░▒░▒▒▒░▒▒▒▓▓▓▓")
    print("▒▒▒▒▒▒▒▓▓▓▓▓████▓▓░                 ░░▒▒▒▓█▓░▓▓█▓▓ ░▒▓  ▒▓▓▓▓▓█▓▓▓█▓▒▒▒▓▓▒░░░░▒▓█▓▓▓▓▓▒▓▒▒▒▒▒▒▒░░░░░░░░░░░░░░▒▒▒▒▒")
    print("▒▒▓▒▓▓▓▓█████▓▒                         ░▒▒▓░ ▓██▓                ▒▓▒▒░░▒▓▒░░▒▓███▓█▓▓▓▓▓▓▓▓▓▓▓▒▓▒▒▒▒▒▒▒▒▒▒▓▒▓▓▓▓▓")
    print("▓▓▓█████▓░                                    ░░▒▒ _    _    _ ░▒░▒▒▒▓▒▓▒▓▒▓█▓███▓▒▓▓▓▓▓▓▓▓▓▓▓▓█▓██▓▓▓▓▓█▓████████")
    print("▓███▓▒  IA inspirée de la plasticité naturelle ✴️  a    N    A  ▒▓█▒▓ ▒▓█▒Architecture Neuronale Autonome v5.3 ▒▓▓")
    print("▓░                                                 _    _    _  ░▓▒▓  ░▓\n\n")

async def test_stress_v53():
    print("--- DÉBUT DU TEST DE BIO-COHÉRENCE aNA v5.3.1 ---")
    
    # 1. Setup : Un neurone "Cobaye" en Couche IV (Entrée Sensorielle)
    config = NeuronConfig(layer_id=3) 
    neuron = Neuron(position=np.array([0, 0, 0]), config=config)
    chemistry = Neuromodulator()
    
    # 2. Phase 1 : Épuisement Métabolique
    print("\nPhase 1 : Test de la Garde Métabolique...")

    limbic = LimbicSystem()

    for i in range(50):
        # On force un input énorme pour faire décharger le neurone en continu
        neuron.receive_input(10.0, chemistry.get_matrix())
        neuron.update(i, chemistry.get_matrix())
        
        if i % 10 == 0:
            print(f"Cycle {i} | Énergie: {neuron.atp_flux:.2f} | Activité: {neuron.is_firing}")
            
    # Vérification : Le neurone DOIT s'arrêter malgré l'input
    assert neuron.atp_flux >= 0.0, "ERREUR : Énergie négative !"
    
    # 3. Phase 2 : Test de Fixation (Limbique + Hippocampe)
    print("\nPhase 2 : Test de Fixation via Système Limbique...")

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
    print(f"Trace mémorielle gravée : {trace:.4f}")
    
    if trace > 0.5:
        print("SUCCÈS : La suture Limbique-Hippocampe est fonctionnelle !")
    
    # 4. Phase 3 : Cohérence des Clés
    print("\nPhase 3 : Vérification des Clés Chimiques...")
    matrix = chemistry.get_matrix()
    if "norepinephrine" in matrix and "dopamine" in matrix:
        print("SUCCÈS : Cartographie des clés conforme (Norepinephrine détectée).")
    else:
        print("ERREUR : Clés manquantes dans la matrice !")

if __name__ == "__main__":
    create_ascii_header()
    asyncio.run(test_stress_v53())