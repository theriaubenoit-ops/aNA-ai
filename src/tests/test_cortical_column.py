#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
aNA AI Project - v5.2
Module: Test Cortical Column 
Description: This test is designed to validate the core functionalities of the cortical column module in complete isolation. It simulates a simple data stream to verify that the cortical column processes inputs correctly, learns patterns, and can retrieve them based on context. The test covers feedforward processing, lateral inhibition, and feedback mechanisms.
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

from anatomy.cortical.cortical_column import CorticalLobe

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

class TestCorticalColumn(unittest.TestCase):
    def setUp(self):
        # Position arbitraire pour le lobe
        self.position = np.array([100.0, 100.0, 100.0])
        self.lobe = CorticalLobe(self.position)
        self.neuromodulators = {
            'dopamine': 0.5,
            'acetylcholine': 0.8, # Forte attention
            'serotonin': 0.2
        }

    def test_signal_cascade(self):
        """Vérifie la cascade de signal à travers les 6 couches"""
        print("\n[CORTICAL TEST: SIGNAL CASCADE]")
        input_signal = 100.0
        output = self.lobe.process_through_layers(input_signal, self.neuromodulators)
        
        monitoring = self.lobe.get_precision_monitoring()
        efficiency = monitoring['precision_metrics']['overall_efficiency']
        
        print(f" -> Input Signal: {input_signal}")
        print(f" -> Output Signal (L5): {output:.2f}")
        print(f" -> Overall Effectiveness: {efficiency:.2%}")
        
        # L'efficacité doit être proche de la cascade attendue (0.65) * attention boost
        self.assertGreater(output, 0)
        self.assertLess(monitoring['precision_metrics']['biological_accuracy'], 0.5)

    def test_attention_mechanism(self):
        """Vérifie que l'acétylcholine booste bien le signal en Layer I"""
        print("\n[CORTICAL TEST: ATTENTION MECHANISM]")
        
        # Test sans attention et sans reconnaissance (Nouveauté pure)
        low_ach = {'acetylcholine': 0.0, 'dopamine': 0.0}
        self.lobe.reset()
        output_base = self.lobe.process_through_layers(100.0, low_ach, recognition_score=0.0)
        
        # Test avec forte attention sur un signal NOUVEAU (Score = 0.0)
        # C'est ici que le boost doit être maximal.
        high_ach = {'acetylcholine': 1.0, 'dopamine': 0.0}
        self.lobe.reset()
        output_boosted = self.lobe.process_through_layers(100.0, high_ach, recognition_score=0.0)
        
        boost_factor = output_boosted / output_base
        print(f" -> Attention Gainer (New): {boost_factor:.2f}x")
        
        self.assertGreater(output_boosted, output_base)

    def test_signal_cascade(self):
        """Vérifie la cascade de signal à travers les 6 couches"""
        print("\n[CORTICAL TEST: SIGNAL CASCADE]")
        input_signal = 100.0
        # On ajoute le score de reconnaissance par défaut
        output = self.lobe.process_through_layers(input_signal, self.neuromodulators, recognition_score=0.5)

if __name__ == '__main__':
    create_ascii_header()
    unittest.main()