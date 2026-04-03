#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
aNA AI Project - v5.1
Module: Test Hippocampus Trauma Logic
Description: This test simulates the trauma logic of the hippocampus by creating a scenario where a neutral experience is followed by a traumatic event, and then simulating the forgetting process over time. The test checks whether the traumatic memory trace persists longer than the neutral one, demonstrating the concept of emotional memory consolidation and persistence.
Architecture and neuroinformatics: Theriault Benoit
"""
import unittest
import asyncio
import sys
import os
import numpy as np

# On définit la racine du projet dynamiquement
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from anatomy.limbic.amygdala import Amygdala
from anatomy.limbic.hippocampus import Hippocampus

async def process_event(amy, hippo, label, intensity, valence):
    """
    Séquence synchronisée : Traitement -> Update -> Modulation -> Encodage
    """
    # 1. L'Amygdale traite le signal sensoriel
    amy.process_emotional_input(intensity, valence, 0.1, {})
    
    # 2. Mise à jour de l'activité interne (Cortisol/Adrénaline)
    # C'est ici que l'alerte est réellement calculée
    amy.update_activity(intensity) 
    
    # 3. Extraction de la modulation synaptique
    mod = amy.get_synaptic_modulation()
    
    # 4. L'Hippocampe grave la trace en fonction de la modulation reçue
    await hippo.update_memories(label, mod)

async def run_scientific_test():
    print("--- START OF EMOTIONAL SEDIMENTATION TESTS (aNA 5.1) ---")
    
    # Initialisation
    amy = Amygdala()
    amy.reset() # Sécurité : On part d'une base neutre
    
    hippo = Hippocampus(config={
        "SUBFIELDS": ["DG", "CA1", "CA2", "CA3", "CA4"], # Ajout de "DG" ici
        "MIN_LATENT_THRESHOLD": 0.001,
        "LTP_GAIN": 0.15,
        "BURN_SCIENTIFIC": 0.05,
        "ENCODE_THRESHOLD": 0.5
    })

    # Phase A : Signal Neutre (Répété)
    print("\nPhase A: Learning a neutral signal...")
    for i in range(5):
        await process_event(amy, hippo, "NEUTRE_1", 0.6, 0.0)
    
    val_n_init = hippo.subfields['CA3'].get('NEUTRE_1', 0)
    print(f"Force trace NEUTRE_1 after 5 cycles : {val_n_init:.4f}")

    # Phase B : Le Trauma (Unique et intense)
    print("\nPhase B: Encounter with a Critical Error (Trauma)...")
    # On injecte une valence de terreur (-1.0)
    await process_event(amy, hippo, "TRAUMA_1", 1.0, -1.0)
    
    val_t_init = hippo.subfields['CA3'].get('TRAUMA_1', 0)
    print(f"Force trace TRAUMA_1 (Gravure Flash) : {val_t_init:.4f}")

    # Phase C : Sédimentation (Oubli sur 100 cycles)
    print("\nPhase C: Simulation of 100 forgetting cycles...")
    for _ in range(100):
        # On simule le passage du temps (décroissance synaptique)
        for label in hippo.subfields['CA3']:
            hippo.subfields['CA3'][label] *= 0.95 # Burn rate de 5%
            # On empêche de descendre sous le plancher de survie (si défini)
            plancher = 0.1 if label == "TRAUMA_1" else 0.001
            hippo.subfields['CA3'][label] = max(plancher, hippo.subfields['CA3'][label])

    # Résultats
    print("\n--- ANALYSIS OF TRACES AFTER LONG FORGETTING ---")
    val_neutre = hippo.subfields['CA3'].get("NEUTRE_1", 0)
    val_trauma = hippo.subfields['CA3'].get("TRAUMA_1", 0)
    
    print(f"Residue NEUTRE_1 : {val_neutre:.6f}")
    print(f"Residue TRAUMA_1 : {val_trauma:.6f}")
    
    if val_trauma > val_neutre:
        print("\nCONCLUSION: The Acid Trace has survived.")
    else:
        print("\nCONCLUSION: Failure of emotional persistence.")

if __name__ == "__main__":
    asyncio.run(run_scientific_test())
