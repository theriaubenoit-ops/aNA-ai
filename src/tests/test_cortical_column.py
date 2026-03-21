#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import numpy as np
import sys
import os

# Chemin vers les modules src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from anatomy.cortical.cortical_column import CorticalLobe

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
        print("\n[TEST CORTICAL : CASCADE DE SIGNAL]")
        input_signal = 100.0
        output = self.lobe.process_through_layers(input_signal, self.neuromodulators)
        
        monitoring = self.lobe.get_precision_monitoring()
        efficiency = monitoring['precision_metrics']['overall_efficiency']
        
        print(f" -> Signal Entrée : {input_signal}")
        print(f" -> Signal Sortie (L5) : {output:.2f}")
        print(f" -> Efficacité Globale : {efficiency:.2%}")
        
        # L'efficacité doit être proche de la cascade attendue (0.65) * attention boost
        self.assertGreater(output, 0)
        self.assertLess(monitoring['precision_metrics']['biological_accuracy'], 0.5)

    def test_attention_mechanism(self):
        """Vérifie que l'acétylcholine booste bien le signal en Layer I"""
        print("\n[TEST CORTICAL : MÉCANISME D'ATTENTION]")
        
        # Test sans attention (ACH = 0)
        low_ach = {'acetylcholine': 0.0, 'dopamine': 0.0}
        self.lobe.reset()
        output_base = self.lobe.process_through_layers(100.0, low_ach)
        
        # Test avec attention (ACH = 1.0)
        high_ach = {'acetylcholine': 1.0, 'dopamine': 0.0}
        self.lobe.reset()
        output_boosted = self.lobe.process_through_layers(100.0, high_ach)
        
        boost_factor = output_boosted / output_base
        print(f" -> Gain d'attention : {boost_factor:.2f}x")
        
        self.assertGreater(output_boosted, output_base)

    def test_memory_access_port(self):
        """Vérifie l'état du port de connexion vers l'Hippocampe"""
        print("\n[TEST CORTICAL : PORT MÉMOIRE]")
        status = self.lobe.get_memory_status()
        print(f" -> État Layer II/III : {status}")
        self.assertEqual(status, "READY")

if __name__ == '__main__':
    unittest.main()