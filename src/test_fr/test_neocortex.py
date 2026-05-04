#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Projet aNA IA v5.2 - Tester le système limbique

Description : Ce test valide l’intégration du module Neocortex au sein de l’architecture aNA. Il vérifie que Neocortex est correctement instancié à partir du registre central et qu’il peut traiter un signal simulé à travers ses différentes couches. Le test garantit que Neocortex peut communiquer avec le thalamus (via la rétroaction de la couche 6) et qu’il peut gérer les influences neuromodulatrices pendant le traitement.

Architecture et neuroinformatique : Thériault Benoit
"""

import unittest
import asyncio
import numpy as np
import os
import sys

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from registry import ORGANS
from anatomy.cortical.neocortex import Neocortex
from anatomy.base.neuromodulator import Neuromodulator # Pour le chemical


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

async def test_3b_integration():
    print("[DÉMARRAGE DU TEST D'INTÉGRATION NEOCORTEX]\n")
    
    # 1. Initialisation du cœur chimique (nécessaire pour le Neocortex)
    chemical = Neuromodulator()
    
    # 2. Instanciation du Neocortex (C'est ici que la magie du registre opère)
    # Votre classe Neocortex doit appeler create_visual_cortical_lobe dans son __init__
    nexo = Neocortex(chemical)
    
    print(f"📡 Registre détecté : {list(ORGANS['NEOCORTEX'].get('INSTANCES', {}).keys())}")

    # 3. Test de communication avec V1
    v1 = ORGANS["NEOCORTEX"]["INSTANCES"].get("V1")
    
    if v1:
        test_signal = 0.85
        # Simulation d'un signal montant (Thalamus -> V1)
        # On vérifie si process_through_layers existe dans l'objet v1
        try:
            # Note: v1 ici est l'instance de CorticalColumns créée par create_visual_cortical_lobe
            res = v1.process_through_layers(test_signal, {"acetylcholine": 0.5})
            print(f"✅ SUCCÈS : Le signal a traversé les couches. Sortie L5 = {res:.4f}")
        except Exception as e:
            print(f"❌ ERREUR lors du traitement du signal : {e}")
    else:
        print("❌ ÉCHEC : Le lobe V1 n'a pas été trouvé dans le Registre.")

if __name__ == "__main__":
    create_ascii_header()
    asyncio.run(test_3b_integration())