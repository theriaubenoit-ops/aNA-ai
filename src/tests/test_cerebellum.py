#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import numpy as np
import sys
import os

# Insertion du chemin pour l'accès aux modules src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from anatomy.subcortical.cerebellum import Cerebellum

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
    unittest.main()