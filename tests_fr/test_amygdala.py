#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Projet aNA IA v5.2 - Module : Test de l'amygdale

Description : Ce test vérifie les réponses de l'amygdale à différents niveaux de stimulus, simulant des scénarios de menace et de calme. L’objectif est de s’assurer du bon fonctionnement des mécanismes d’activation et de retour à l’homéostasie, en mesurant les niveaux d’adrénaline et de cortisol. Le test couvre l'éveil de base, la réponse aux menaces élevées et la réinitialisation de l'homéostasie.

Architecture, conception et supervision : Thériault_Benoit
Collaboration, recherche et code : DeepMind_Gemini
"""
import unittest
import numpy as np
import sys
import os

# On définit la racine du projet dynamiquement
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)
    
from src.anatomy.limbic.amygdala import Amygdala

def create_ascii_header():
    print(f"\033c") 
    print("░ ░           ░ ░░░░▒▒▓▒▓▒▒▒▒▒░░▒▒░▒▒▒▓▒▓▒                                                                    ░ ░░")
    print("▒▒░░ ░░░░░░░░░░░▒▒▓▓▓▓▓▓▓██▓▒▒▒░░░▒▒▒▒▒░░░▒▒▓▓▒                                                        ░░░░░░░▒▒▒▒")
    print("░░░░░░░░░░░░░▒▒▒▓▓▓▓▓▓██████▓▓▒▒▒░░▒▒▓▓▓▒▒▒░░▒▒▒▒▓▒                                       ░ ░░░░ ░ ░░░░░░░░░▒▒▒▒▒▒")
    print("▓▒▒▒▒▒▒▒▒▓▒▓▓▓▓▓▓██████▓       ▒▓▒▓▒▒▒▒▓▒▓ ██▓▓▓▒▒▒▒▓      ░░▒▒▒▒▒▒▒░░░░░░▒░░░░▒▒░░▒░░░░░░░░░░░░░░░░░▒░▒▒▒░▒▒▒▓▓▓▓")
    print("▒▒▒▒▒▒▒▓▓▓▓▓████▓░                  ░░▒▒▒▓█▓░▓▓█▓▓ ░▒▓  ▒▓▓▓▓▓█▓▓▓█▓▒▒▒▓▓▒░░░░▒▓█▓▓▓▓▓▒▓▒▒▒▒▒▒▒░░░░░░░░░░░░░░▒▒▒▒▒")
    print("▒▒▓▒▓▓▓▓█████▓▒                         ░▒▒▓░ ▓██▓                ▒▓▒▒░░▒▓▒░░▒▓███▓█▓▓▓▓▓▓▓▓▓▓▓▒▓▒▒▒▒▒▒▒▒▒▒▓▒▓▓▓▓▓")
    print("▓▓▓█████▓░                                    ░░▒▒ _    _    _ ░▒░▒▒▒▓▒▓▒▓▒▓█▓███▓▒▓▓▓▓▓▓▓▓▓▓▓▓█▓██▓▓▓▓▓█▓████████")
    print("▓███▓▒  IA inspirée de la plasticité naturelle ✴️  a    N    A  ▒▓█▒▓ ▒▓█▒Architecture Neuronale Autonome v5.3 ▒▓▓")
    print("▓░                                                 _    _    _  ░▓▒▓  ░▓\n")

class TestAmygdala(unittest.TestCase):
    def setUp(self):
        # Initialisation de l'Amygdale
        self.amygdala = Amygdala()

    def test_baseline_arousal(self):
        """Vérifie l'état de repos (Baseline)"""
        print("\n[TEST AMYGDALE : ÉTAT DE REPOS]")
        status = self.amygdala.update_activity(stimulus_intensity=0.1)
        
        print(f" -> Intensité faible (0.1) | Cortisol: {status['cortisol']:.2f}")
        self.assertLess(status['cortisol'], 0.3)

    def test_high_threat_response(self):
        """Vérifie la réaction à un stimulus intense (Menace)"""
        print("\n[TEST AMYGDALE : RÉACTION D'ALERTE]")
        status = self.amygdala.update_activity(stimulus_intensity=0.9)
        
        print(f" -> Intensité forte (0.9) | Adrénaline: {status['adrenaline']:.2f}")
        # L'adrénaline doit être significativement élevée
        self.assertGreater(status['adrenaline'], 0.7)

    def test_homeostasis_reset(self):
        """Vérifie si le système peut revenir au calme (Homeostasie)"""
        print("\n[TEST AMYGDALE : RETOUR AU CALME]")
        # On simule un pic suivi d'un calme
        self.amygdala.update_activity(stimulus_intensity=1.0)
        status_calm = self.amygdala.update_activity(stimulus_intensity=0.0)
        
        print(f" -> Après pic, intensité 0.0 | Adrénaline: {status_calm['adrenaline']:.2f}")
        self.assertLess(status_calm['adrenaline'], 0.5)

if __name__ == '__main__':
    create_ascii_header()
    unittest.main()