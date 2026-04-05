#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
aNA AI Project - v5.1
Module: Test Autonomy 
Description: This test is designed to validate the autonomous behaviors of the aNA system in isolation. It simulates an interactive environment where the system can respond to user input without external dependencies. The test checks the system's ability to process sensory input, modulate internal states, and produce outputs based on its internal logic and chemical states. It also verifies that the system can maintain a basic level of consciousness and metabolic regulation while interacting with the environment.
Architecture and neuroinformatics: Theriault Benoit
"""
import unittest
import numpy as np
import asyncio
import termios
import tty
import select
import os
import sys

# On définit la racine du projet dynamiquement
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from anatomy.subcortical.thalamus import Thalamus
from anatomy.limbic.hippocampus import Hippocampus
from anatomy.base.neuromodulator import Neuromodulator
from core.pulse import Pulse

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

def is_data():
    """Vérifie si une touche est pressée sans bloquer le script."""
    return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

def get_input_non_blocking():
    """Vérifie si une touche est pressée sans arrêter le programme."""
    if select.select([sys.stdin], [], [], 0)[0]:
        return sys.stdin.read(1)
    return None

async def interactive_keyboard_input(thalamus):
    """Boucle qui écoute le clavier en temps réel."""
    print("⌨️ Interactive mode active. Type your commands (e.g., MOON, MARS, etc.)")
    old_settings = termios.tcgetattr(sys.stdin)
    try:
        tty.setcbreak(sys.stdin.fileno())
        while True:
            char = get_input_non_blocking() # Ne s'arrête jamais !
    
            # 1. Traitement Thalamique (si char est None, il ne fait rien)
            if char: # On ne traite que s'il y a une touche pressée
                # On crée un payload minimal pour le Thalamus v5.1
                payload = {"signal_label": char, "intensity": 0.5, "nucleus": "MGN"}
                # On passe le feedback 0.0 car il n'y a pas de colonne corticale dans ce test isolé

                if char: 
                    print(f"\n[Input] Key detected: {char}") # <-- AJOUTE CECI pour "voir" tes touches
                    payload = {"signal_label": char, "intensity": 0.5, "nucleus": "MGN"}
                    await thalamus.process_payload(payload, l6_feedback=0.0)
            
            await asyncio.sleep(0.1) # Respiration du système
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

async def main():
    # --- Initialisation v5.1 ---
    #from anatomy.base.neuromodulator import Neuromodulator
    #from core.pulse import Pulse
    
    neuromod_core = Neuromodulator()
    heart = Pulse()
    hippo = Hippocampus(neuromodulator_core=neuromod_core)
    
    # Correction de la signature : pas de 'hippo=', mais 'hippocampus='
    thalamus = Thalamus(
        hippocampus=hippo, 
        pulse=heart, 
        neuromodulator_core=neuromod_core
    )
    
    print("\n🚀 STARTING THE INTERACTIVE AUTONOMY TEST aNA v5.1")
    print("="*50)

    # Au lieu de simulate_thalamic_vibration, on lance la conscience
    # et la gestion du métabolisme
    thalamus.is_autonomous = True
    
    # Tâches asynchrones v5.1
    consciousness_task = asyncio.create_task(thalamus.internal_consciousness_loop())
    input_task = asyncio.create_task(interactive_keyboard_input(thalamus))
    
    # On fait tourner l'ensemble
    await asyncio.gather(consciousness_task, input_task)

# --- POINT D'ENTRÉE DU SCRIPT ---
if __name__ == "__main__":
    create_ascii_header()
    try:
        # Lance la boucle d'événements asyncio pour l'orchestration
        asyncio.run(main())
    except KeyboardInterrupt:
        # Permet de quitter proprement avec Ctrl+C
        print("\n🛑 Simulation interrupted by the user.")
    except Exception as e:
        print(f"\n❌ Fatal error during execution: {e}")