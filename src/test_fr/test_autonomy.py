#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Projet aNA AI - v5.1
Module : Tester l'autonomie
Description : Ce test est conçu pour valider les comportements autonomes du système aNA de manière isolée. Il simule un environnement interactif dans lequel le système peut répondre aux entrées de l'utilisateur sans dépendances externes. Le test vérifie la capacité du système à traiter les entrées sensorielles, à moduler les états internes et à produire des sorties basées sur sa logique interne et ses états chimiques. Il vérifie également que le système peut maintenir un niveau de base de conscience et de régulation métabolique tout en interagissant avec l’environnement.
Architecture et neuroinformatique : Thériault Benoit
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
    print("▓▓▓░IA inspirée de la plasticité naturelle░░  ░░░  a    N    A  ▒▓▒▓▒▒▒▓░Architecture Neuronale Autonome v5.1░░▒▒▓")
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
    print("⌨️ Mode interactif actif. Tapez vos commandes (LUNE, MARS, etc.)...")
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
                    print(f"\n[Entrée] Clé détectée : {char}") # <-- AJOUTE CECI pour "voir" tes touches
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
    
    print("\n🚀 DÉMARRAGE DU TEST D'AUTONOMIE INTERACTIF aNA v5.1")
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
        print("\n🛑 Simulation interrompue par l'utilisateur.")
    except Exception as e:
        print(f"\n❌ Erreur fatale lors de l'exécution : {e}")