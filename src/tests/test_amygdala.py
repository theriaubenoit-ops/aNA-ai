#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
aNA Project - v5.1
Module: Test Amygdala
Description: This test checks the amygdala's responses to different levels of stimulus, simulating threat and calm scenarios. The goal is to ensure that the activation and return-to-homeostasis mechanisms are functioning correctly, by measuring adrenaline and cortisol levels. The test covers baseline arousal, high threat response, and homeostasis reset.
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

from anatomy.limbic.amygdala import Amygdala

class TestAmygdala(unittest.TestCase):
    def setUp(self):
        # Initialisation de l'Amygdale
        self.amygdala = Amygdala()

    def test_baseline_arousal(self):
        """Vérifie l'état de repos (Baseline)"""
        print("\n[TEST AMYGDALE : RESTING STATE]")
        status = self.amygdala.update_activity(stimulus_intensity=0.1)
        
        print(f" -> Low intensity (0.1) | Cortisol: {status['cortisol']:.2f}")
        self.assertLess(status['cortisol'], 0.3)

    def test_high_threat_response(self):
        """Vérifie la réaction à un stimulus intense (Menace)"""
        print("\n[TEST AMYGDALE : ALERT REACTION]")
        status = self.amygdala.update_activity(stimulus_intensity=0.9)
        
        print(f" -> High intensity (0.9) | Adrenaline: {status['adrenaline']:.2f}")
        # L'adrénaline doit être significativement élevée
        self.assertGreater(status['adrenaline'], 0.7)

    def test_homeostasis_reset(self):
        """Vérifie si le système peut revenir au calme (Homeostasie)"""
        print("\n[TEST AMYGDALE : RETURN TO CALM]")
        # On simule un pic suivi d'un calme
        self.amygdala.update_activity(stimulus_intensity=1.0)
        status_calm = self.amygdala.update_activity(stimulus_intensity=0.0)
        
        print(f" -> After peak, intensity 0.0 | Adrenaline: {status_calm['adrenaline']:.2f}")
        self.assertLess(status_calm['adrenaline'], 0.5)

if __name__ == '__main__':
    unittest.main()