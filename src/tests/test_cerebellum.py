#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
aNA Project - v5.2
Module: Test Cerebellum 
Description: This test validates the error correction capabilities of the cerebellum. It simulates a motor task where the system must reach a target position, starting with an initial error. The test checks that after processing feedback, the cerebellum computes a correction that reduces the error, and that the inhibitory output from Purkinje cells increases appropriately in response to high error signals.
Architecture and neuroinformatics: Theriault Benoit
"""
import unittest
import numpy as np
import os
import sys

# On définit la racine du projet dynamiquement
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from anatomy.subcortical.cerebellum import Cerebellum

def create_ascii_header():
    print(f"\033c") 
    print("░                     ░░░░░░░░░░▒▒▒▒▒▒░░")
    print("           ░░░░░░░░░▒▒▒▒▒▓▒▒▒▒░░░░░░░░░░▒▒▒▒░                                                          ░░░░░░░░░░░")
    print("░░░░░░░░░░░░░░░░▒▒▒▒▓▓▓▓▓▓▓▓▓▓▓▒░░░░░▒▒▒░░░░▒▓▒░░                      ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░")
    print("░░░░░░░░░░░░░░▒▒▒▓▓▓▓▓▓▓▓▓▓▓▒░░▒▒▒░░░░▒▓▓▓▓▓▓▒▒▒▒▒░     ░░░░░░░░░░░░░░░░░░░░░▒▒░░▒▒▒▓▓▓▓▓▓▒▒▒░░░░░░░░░░░░░░░░░▒▒▒▒")
    print("▒░░░░░▒▒▒▒▒▒▓▓▓▓▓▓▓▓▓▒░         ░░▒▒▒░▒▒▒▒▓▓▓▓▓▓▓▒▒░░  ░▒▒▒▓▒▒▒▓▒▓▒▓▒░░░░░░░▒▓▓▓▓▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░░░░░░░░░░░▒▓")
    print("░▒▒▒▒▓▓▓▓▓▓▓▓▓▓▓▓░                   ░░ ▒▒▓▒░▒▓▓▓░▒▒░░           ░▒░░░▒▓▒▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒▒▓▓")
    print("▒▒▓▓▓▓▓▓▒▒▒░░                           ░▓▓▒░░▒▓▓░ _    _    _ ░▒░░▒▓▒▓▓▓▓▓▓▓▓▓▓▒░░░░░░░░░▒▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓")
    print("▓▓▓▓▓▒░AI inspired by natural plasticity ░░   ░░░  a    N    A  ▒▓▒▓▒▒▒▓░Autonomous Neural Architecture v5.2   ░▒▓")
    print("░                                                  ‾    ‾    ‾ ░▓▒▓░░▒▓░\n")

class TestCerebellum(unittest.TestCase):
    def setUp(self):
        self.position = np.array([0.0, -40.0, -10.0])
        self.cerebellum = Cerebellum(self.position)

    def test_error_correction(self):
        """Vérifie que le cervelet apprend à corriger une erreur motrice"""
        print("\n[CEREBELLUM TEST: ERROR CORRECTION]")
        
        target_pos = np.array([10.0, 10.0, 10.0])
        current_pos = np.array([8.0, 9.0, 11.0]) # Erreur initiale
        
        # Calcul de l'erreur initiale
        initial_error = np.linalg.norm(target_pos - current_pos)
        print(f" -> Initial error: {initial_error:.4f}")
        
        # Le cervelet traite l'erreur et ajuste
        correction = self.cerebellum.compute_correction(target_pos, current_pos)
        
        # Après correction, l'erreur simulée devrait être plus petite
        new_pos = current_pos + correction
        final_error = np.linalg.norm(target_pos - new_pos)
        
        print(f" -> Error after correction: {final_error:.4f}")
        self.assertLess(final_error, initial_error)

    def test_purkinje_modulation(self):
        """Vérifie l'activité des cellules de Purkinje (inhibition)"""
        print("\n[CEREBELLUM TEST: PURKINJE MODULATION]")
        # Une forte erreur doit augmenter l'inhibition pour stabiliser
        self.cerebellum.process_feedback(error_signal=0.9)
        inhibition = self.cerebellum.get_inhibitory_output()
        
        print(f" -> Level of inhibition: {inhibition:.2f}")
        self.assertGreater(inhibition, 0.5)

if __name__ == '__main__':
    create_ascii_header()
    unittest.main()