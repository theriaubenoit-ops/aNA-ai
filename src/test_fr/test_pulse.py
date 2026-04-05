#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Projet ANA AI - v5.1
Module : Test d'impulsion
Description : Ce test est conçu pour valider les fonctionnalités de base du module Pulse en isolation complète. Il simule la réponse du cœur aux stimuli, notamment les modifications des niveaux d'ATP, la libération de dopamine et la modulation de fréquence. Le test couvre la dynamique du pouls, y compris les périodes réfractaires et l'impact des signaux chimiques sur la fréquence cardiaque.
Architecture et neuroinformatique : Thériault Benoit
"""
import unittest
import time
import sys
import os

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
    print("▓▓▓░IA inspirée de la plasticité naturelle░░  ░░░  a    N    A  ▒▓▒▓▒▒▒▓░Architecture Neuronale Autonome v5.1░░▒▒▓")
    print("░                                                  ‾    ‾    ‾ ░▓▒▓░░▒▓░\n\n")

def monitor_ana_heart():
    heart = Pulse()
    print("--- 💓 Moniteur Cardiaque aNA v5.1 ---")
    print("Appuyez sur 'Enter' pour simuler un stimulus, 'q' pour quitter.\n")
    
    try:
        while True:
            # 1. Calcul de la dynamique (dt)
            dt = heart.compute_dynamics()
            
            # 2. Récupération des constantes vitales
            hz = heart.get_current_hz()
            atp = heart.atp
            dopamine = heart.dopamine
            
            # 3. Affichage dynamique (sur une seule ligne pour voir le flux)
            status = "💤 REPOS" if heart.is_refractory else "🔥 ACTIF"
            sys.stdout.write(
                f"\r[{status}] | ATP: {atp:.3f} | Hz: {hz:4.1f} | Dopa: {dopamine:.3f} | dt: {dt:.4f}s"
            )
            sys.stdout.flush()

            # 4. Simulation d'interaction (Optionnel pour le test)
            # Dans un vrai test, on utiliserait un thread pour le clavier, 
            # mais ici on va juste laisser tourner pour voir la dissipation.
            
            time.sleep(0.1) # Petit délai technique pour ne pas saturer le CPU
            
            # Simulation d'un stimulus toutes les 5 secondes pour le test
            if int(time.time()) % 8 == 0 and dopamine < 0.1:
                heart.inject_stimulus(0.5)
                print("\n⚡ [STIMULUS] Le cœur s'accélère !")

    except KeyboardInterrupt:
        print("\n🛑 Arrêt du moniteur.")

if __name__ == "__main__":
    create_ascii_header()
    monitor_ana_heart()