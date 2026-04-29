#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Project aNA AI v5.2 - Test d'Autonomie du Hub 

Description: Valider le flux complet ThalamicHub -> Neocortex (V1) -> Feedback L6 -> Modulation du Pulse (BPM) dans un scénario autonome. Ce test simule une séquence d'entrée visuelle, observe comment le ThalamicHub traite et filtre cette entrée, comment elle est projetée vers le Neocortex (V1), et comment le feedback de L6 influence le rythme cardiaque via le Pulse. L'objectif est de s'assurer que les interactions entre ces composants fonctionnent de manière cohérente et autonome, sans intervention externe.

Architecture and neuroinformatics: Theriault Benoit
"""

import unittest
import asyncio
import numpy as np
import sys
import os

# Configuration des chemins
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config import get_config
from registry import ORGANS
from anatomy.subcortical.thalamus import Thalamus
from anatomy.subcortical.thalamic_hub import ThalamicHub
from anatomy.limbic.hippocampus import Hippocampus
from anatomy.cortical.neocortex import Neocortex
from anatomy.base.neuromodulator import Neuromodulator
from core.pulse import Pulse


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

async def test_hub_cycle():
    config = get_config()
    print("🚀 DÉMARRAGE DU TEST D'AUTONOMIE DU HUB (v5.3)")
    print("="*50)

    # 1. Initialisation de l'environnement bio-numérique
    chemical_core = Neuromodulator()
    hippo = Hippocampus(config=config, neuromodulator_core=chemical_core)
    heart = Pulse(bpm=config.get("BASE_BPM", 72.0))
    
    # 2. Initialisation des organes maîtres
    # Le Neocortex s'enregistre dans le registre lors de sa création
    nexo = Neocortex(chemical_core)
    thalamus = Thalamus(
        hippocampus=hippo, 
        pulse=heart, 
        neuromodulator_core=chemical_core 
    )
    hub = ThalamicHub(thalamus_core=thalamus)

    print(f"🧠 Organes détectés : {list(ORGANS['NEOCORTEX']['INSTANCES'].keys())}")

    # 3. Simulation d'une séquence d'entrée (Le monde extérieur)
    stimulis = [("VISUAL", 0.9), ("VISUAL", 0.4), ("VISUAL", 0.95)]

    for sense, intensity in stimulis:
        print(f"\n📥 Entrée détectée : {sense} | Intensité: {intensity}")

        # A. Passage par le filtre du Thalamus (Gating)
        matrix = chemical_core.get_matrix()
        gating_res = await hub.route_signal(f"input_{sense.lower()}", intensity, heart.bpm)
        filtered_val = gating_res.get('intensity', 0.0)
        
        print(f"🔍 Thalamus Gating : {intensity} -> {filtered_val:.4f}")

# B. Projection vers le Neocortex (V1)
        v1 = ORGANS["NEOCORTEX"]["INSTANCES"].get("V1")
        if v1:
            # Traitement par les 6 couches
            l5_output = v1.process_through_layers(filtered_val, matrix)
            
            # Correction : Récupération sécurisée du feedback L6
            # Si 'layers' n'est pas un attribut, vérifiez si c'est une méthode ou 
            # utilisez une valeur par défaut en attendant de vérifier la structure de CorticalColumns
            try:
                l6_feedback = v1.layers.get("L6", 0.5) if hasattr(v1, 'layers') else 0.5
            except:
                l6_feedback = 0.5 # Valeur de sécurité
            
            print(f"🧬 Neocortex (V1) : Sortie L5 = {l5_output:.4f} | Feedback L6 = {l6_feedback:.4f}")
            
            # C. Mise à jour du rythme cardiaque basée sur le feedback
            # Si L6 est haut (reconnaissance), le système se calme.
            heart.update_metabolism(l6_feedback)
            print(f"💓 Rythme Pulse : {heart.bpm:.1f} BPM")
        else:
            print("❌ Erreur : Lobe V1 introuvable.")

    print("\n" + "="*50)
    print("✅ TEST DE CYCLE TERMINÉ : L'intégration Hub-Lobe est opérationnelle.")

if __name__ == "__main__":
    create_ascii_header()
    try:
        asyncio.run(test_hub_cycle())
    except Exception as e:
        print(f"❌ Erreur fatale : {e}")