#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
aNA AI Project - v5.1
Module: Test Pulse 
Description: This test is designed to validate the core functionalities of the Pulse module in complete isolation. It simulates the heart's response to stimuli, including changes in ATP levels, dopamine release, and frequency modulation. The test covers the dynamics of the pulse, including refractory periods and the impact of chemical signals on heart rate.
Architecture and neuroinformatics: Theriault Benoit
"""
import unittest
import numpy as np
import time
import os
import sys
import select

# On définit la racine du projet dynamiquement
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

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

def monitor_ana_heart():
    heart = Pulse()
    print("--- 💓 Heart Monitor aNA v5.1 ---")
    print("Commandes :")
    print("  - [Enter] : Injecting a stimulus (Dopamine)")
    print("  - [q] + [Enter] : Clean exit\n")
    
    try:
        while True:
            # 1. Gestion du Clavier (Non-bloquant pour Linux/Kubuntu)
            # Vérifie si l'utilisateur a tapé quelque chose sans arrêter la boucle
            if select.select([sys.stdin], [], [], 0)[0]:
                line = sys.stdin.readline().strip()
                if line.lower() == 'q':
                    print("\n🛑 Monitor shut-off.")
                    break
                else:
                    heart.inject_stimulus(0.5)
                    # On efface la ligne précédente pour le feedback visuel
                    sys.stdout.write("\n⚡ [STIMULUS] The heart rate increases!\n")

            # 2. Calcul de la dynamique (dt)
            dt = heart.compute_dynamics()
            
            # 3. Récupération des constantes vitales
            hz = heart.get_current_hz()
            atp = heart.atp
            dopamine = heart.dopamine
            
            # 4. Affichage dynamique (Rendu propre sur une seule ligne)
            status = "💤 REPOS" if heart.is_refractory else "🔥 ACTIF"
            sys.stdout.write(
                f"\r[{status}] | ATP: {atp:.3f} | Hz: {hz:4.1f} | Dopa: {dopamine:.3f} | dt: {dt:.4f}s"
            )
            sys.stdout.flush()

            time.sleep(0.1) 

    except KeyboardInterrupt:
        print("\n🛑 Interrupt detected.")

if __name__ == "__main__":
    create_ascii_header()
    monitor_ana_heart()