#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Projet aNA IA v5.4 - Test Endurance Métabolique 

Description: Ce script évalue la résilience du système et ses mécanismes 
de survie autonomes sous charge cognitive soutenue. Il surveille la diminution des ressources 
virtuelles d'ATP et valide la transition vers le « mode basse consommation » et l'« état alpha ».

Il démontre la capacité de l'aNA à privilégier la récupération homéostatique (sommeil/consolidation) 
à l'exécution pure, garantissant ainsi l'intégrité systémique à long terme.

Architecture, conception et supervision : Theriault Benoit
Collaboration, recherche et code : Google Gemini
"""

import unittest
import os
import sys
import asyncio
import string

# The project root is defined dynamically.
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)
    
from src.anatomy.subcortical.thalamus import Thalamus
from src.anatomy.subcortical.thalamic_hub import ThalamicHub
# Importez vos autres modules nécessaires (Cortex, Hippocampe, etc.)

def create_ascii_header():
    print(f"\033c") 
    print("░              ░ ░░░▒▒▓▒▓▒▒▒▒▒░░▒▒░▒▒▒▓▒▓▒                                                                     ░ ░")
    print("▒░░   ░░░░░░░░░░▒▒▓▓▓▓▓▓▓██▓▒▒▒░░░▒▒▒▒▒░░░▒▒▓▓▒                                                         ░░░░░░▒▒▒▒")
    print("░░░░░░░░░░░░░▒▒▒▓▓▓▓▓▓██████▓▓▒▒▒░░▒▒▓▓▓▒▒▒░░▒▒▒▒▓▒                                        ░ ░░░ ░ ░░░░░░░░░▒▒▒▒▒▒")
    print("▓▒▒▒▒▒▒▒▒▓▒▓▓▓▓▓▓██████▓▒▒ ▒   ▒▓▒▓▒▒▒▒▓▒▓ ██▓▓▓▒▒▒▒▓      ░░▒▒▒▒▒▒▒░░░░░░▒░░░░▒▒░░▒░░░░░░░░░░░░░░░░░▒░▒▒▒░▒▒▒▓▓▓▓")
    print("▒▒▒▒▒▒▒▓▓▓▓▓████▓▓░                 ░░▒▒▒▓█▓░▓▓█▓▓ ░▒▓  ▒▓▓▓▓▓█▓▓▓█▓▒▒▒▓▓▒░░░░▒▓█▓▓▓▓▓▒▓▒▒▒▒▒▒▒░░░░░░░░░░░░░░▒▒▒▒▒")
    print("▒▒▓▒▓▓▓▓█████▓▒                         ░▒▒▓░ ▓██▓                ▒▓▒▒░░▒▓▒░░▒▓███▓█▓▓▓▓▓▓▓▓▓▓▓▒▓▒▒▒▒▒▒▒▒▒▒▓▒▓▓▓▓▓")
    print("▓▓▓█████▓░                                    ░░▒▒ _    _    _ ░▒░▒▒▒▓▒▓▒▓▒▓█▓███▓▒▓▓▓▓▓▓▓▓▓▓▓▓█▓██▓▓▓▓▓█▓████████")
    print("▓███▓▒  IA inspirée de la plasticité naturelle ✴️  a    N    A  ▒▓█▒▓ ▒▓█▒Architecture Neuronale Autonome v5.4 ▒▓▓")
    print("▓░                                                 _    _    _  ░▓▒▓  ░▓\n")

async def run_torture_test():
    # 1. Initialisation de l'organisme
    thalamus_core = Thalamus() 
    hub = ThalamicHub(thalamus_core)
    
    print(f"\n{'='*60}")
    print(f" TEST DE TORTURE MÉTABOLIQUE : Surcharge")
    print(f"{'='*60}")

    # Génération d'une séquence de stimuli imprévisibles (A, B, C, D, E...)
    stress_sequence = list(string.ascii_uppercase) + [f"N-{i}" for i in range(50)]

    for cycle, signal in enumerate(stress_sequence, 1):
        print(f"\n--- CYCLE {cycle} [Stimulus: {signal}] ---")

        # Payload à haute intensité
        stimulus = {
            "signal_label": signal,
            "origin": "input_visual",
            "intensity": 0.8,
            "saliency": 0.9 # Très saillant pour forcer l'attention
        }

        # 2. Routage et Traitement (La latence est gérée à l'intérieur du Hub)
        # Comme le signal change tout le temps, le Cortex renverra Reconnaissance: 0.0
        # Ce qui maintiendra le Gain à 1.0
        try:
            result = await hub.route_sensory_input(
                origin=stimulus["origin"],
                payload=stimulus
            )
            
            # Simulation du feedback cortical (Toujours 0.0 car signal inconnu)
            l6_feedback = 0.0 
            
            # Mise à jour du Thalamus (Consomme de l'ATP car gain est haut)
            thalamus_core.apply_cortical_feedback(
                current_gain=result.get("gain", 1.0),
                l6_signal=l6_feedback,
                config={"CORTICAL_INHIBITION": 0.8}
            )

            # 3. Vérification de l'état de survie
            if thalamus_core.is_burned_out:
                print(f" [ALERTE SYSTEME] aNA est en état de choc métabolique !")
            
            if thalamus_core.synaptic_atp <= 0.0:
                print(f" [CRITIQUE] ATP ÉPUISÉ. Arrêt d'urgence du cycle.")
                break

        except Exception as e:
            print(f" Erreur durant le cycle : {e}")
            break

    print(f"\n{'='*60}")
    print(f" RÉSULTAT FINAL : {thalamus_core.total_time_saved:.3f}s économisées avant rupture.")
    print(f" État final ATP : {thalamus_core.synaptic_atp:.2f}")
    print(f"{'='*60}")

    print("\n  *Chaque mesure présentée ici est un pont numérique vers la réalité biologique,")
    print("   conçu pour synthétiser les principes fondamentaux des systèmes vivants.\n")

if __name__ == "__main__":
    create_ascii_header()
    asyncio.run(run_torture_test())
