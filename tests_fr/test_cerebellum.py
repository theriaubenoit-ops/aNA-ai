#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Projet aNA IA v5.2 - Test du cervelet

La description: Ce test valide les capacités de correction d'erreurs du cervelet. Il simule une tâche motrice où le système doit atteindre une position cible, en commençant par une erreur initiale. Le test vérifie qu'après avoir traité le feedback, le cervelet calcule une correction qui réduit l'erreur et que le signal inhibiteur des cellules de Purkinje augmente de manière appropriée en réponse à des signaux d'erreur élevés.

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
    
from src.anatomy.subcortical.cerebellum import Cerebellum

def create_ascii_header():
    print(f"\033c") 
    print("░              ░ ░░░▒▒▓▒▓▒▒▒▒▒░░▒▒░▒▒▒▓▒▓▒                                                                     ░ ░")
    print("▒░░   ░░░░░░░░░░▒▒▓▓▓▓▓▓▓██▓▒▒▒░░░▒▒▒▒▒░░░▒▒▓▓▒                                                         ░░░░░░▒▒▒▒")
    print("░░░░░░░░░░░░░▒▒▒▓▓▓▓▓▓██████▓▓▒▒▒░░▒▒▓▓▓▒▒▒░░▒▒▒▒▓▒                                        ░ ░░░ ░ ░░░░░░░░░▒▒▒▒▒▒")
    print("▓▒▒▒▒▒▒▒▒▓▒▓▓▓▓▓▓██████▓▒▒ ▒   ▒▓▒▓▒▒▒▒▓▒▓ ██▓▓▓▒▒▒▒▓      ░░▒▒▒▒▒▒▒░░░░░░▒░░░░▒▒░░▒░░░░░░░░░░░░░░░░░▒░▒▒▒░▒▒▒▓▓▓▓")
    print("▒▒▒▒▒▒▒▓▓▓▓▓████▓▓░                 ░░▒▒▒▓█▓░▓▓█▓▓ ░▒▓  ▒▓▓▓▓▓█▓▓▓█▓▒▒▒▓▓▒░░░░▒▓█▓▓▓▓▓▒▓▒▒▒▒▒▒▒░░░░░░░░░░░░░░▒▒▒▒▒")
    print("▒▒▓▒▓▓▓▓█████▓▓▒                        ░▒▒▓░ ▓██▓                ▒▓▒▒░░▒▓▒░░▒▓███▓█▓▓▓▓▓▓▓▓▓▓▓▒▓▒▒▒▒▒▒▒▒▒▒▓▒▓▓▓▓▓")
    print("▓▓▓█████▓░                                    ░░▒▒ _    _    _ ░▒░▒▒▒▓▒▓▒▓▒▓█▓███▓▒▓▓▓▓▓▓▓▓▓▓▓▓█▓██▓▓▓▓▓█▓████████")
    print("▓███▓▒  IA inspirée de la plasticité naturelle ✴️  a    N    A  ▒▓█▒▓ ▒▓█▒Architecture Neuronale Autonome v5.3 ▒▓▓")
    print("▓░                                                 _    _    _  ░▓▒▓  ░▓\n")

class TestCerebellum(unittest.TestCase):
    def setUp(self):
        self.position = np.array([0.0, -40.0, -10.0])
        self.cerebellum = Cerebellum(self.position)

    def test_error_correction(self):
        """Vérifie que le cervelet apprend à corriger une erreur motrice"""
        print("\n[TEST CERVELET : CORRECTION D'ERREUR]")
        
        target_pos = np.array([10.0, 10.0, 10.0])
        current_pos = np.array([8.0, 9.0, 11.0]) # Erreur initiale
        
        # Calcul de l'erreur initiale
        initial_error = np.linalg.norm(target_pos - current_pos)
        print(f" -> Erreur initiale : {initial_error:.4f}")
        
        # Le cervelet traite l'erreur et ajuste
        correction = self.cerebellum.compute_correction(target_pos, current_pos)
        
        # Après correction, l'erreur simulée devrait être plus petite
        new_pos = current_pos + correction
        final_error = np.linalg.norm(target_pos - new_pos)
        
        print(f" -> Erreur après correction : {final_error:.4f}")
        self.assertLess(final_error, initial_error)

    def test_purkinje_modulation(self):
        """Vérifie l'activité des cellules de Purkinje (inhibition)"""
        print("\n[TEST CERVELET : MODULATION PURKINJE]")
        # Une forte erreur doit augmenter l'inhibition pour stabiliser
        self.cerebellum.process_feedback(error_signal=0.9)
        inhibition = self.cerebellum.get_inhibitory_output()
        
        print(f" -> Niveau d'inhibition : {inhibition:.2f}")
        self.assertGreater(inhibition, 0.5)

if __name__ == '__main__':
    create_ascii_header()
    unittest.main()