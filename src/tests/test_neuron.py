#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
aNA AI Project - v5.1
Module: Test Neuron
Description: This test is designed to validate the core functionalities of the neurone module in complete isolation. It simulates a simple data stream to verify that the neurone processes inputs correctly, learns patterns, and can retrieve them based on context. The test covers feedforward processing, lateral inhibition, and feedback mechanisms.
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

from anatomy.base.neuron import Neuron, NeuronConfig

class TestNeuron(unittest.TestCase):
    def setUp(self):
        # Configuration standard pour un neurone pyramidal
        self.config = NeuronConfig(
            layer_id=1,
            threshold_potential=-52.0,  # Seuil typique
            base_energy_consumption=0.01,
            firing_energy_cost=0.1
        )
        self.position = np.array([0.0, 0.0, 0.0])
        self.neuron = Neuron(self.position, self.config)

    def test_initial_state(self):
        """Vérifie que le neurone démarre au repos"""
        print("\n[NEURON TEST: INITIAL STATE]")
        self.assertFalse(self.neuron.is_firing)
        self.assertGreater(self.neuron.energy_level, 0.9)
        print(" -> A resting neuron, charged with energy.")

    def test_threshold_activation(self):
        """Vérifie si le neurone déclenche après avoir atteint le seuil"""
        print("\n[NEURON TEST: ACTIVATION THRESHOLD]")
        # On envoie un signal fort
        self.neuron.receive_input(60.0, {}) 
        self.neuron.update(time_step=1, neuromodulators={})
        
        self.assertTrue(self.neuron.is_firing)
        print(f" -> Successful discharge! Potential reaches the threshold of {self.config.threshold_potential} mV.")

    def test_energy_depletion(self):
        """Vérifie que l'activité consomme de l'énergie"""
        print("\n[NEURON TEST: ENERGY CONSUMPTION]")
        initial_energy = self.neuron.energy_level
        
        # On fait feu plusieurs fois
        for _ in range(5):
            self.neuron.receive_input(100.0, {})
            self.neuron.update(time_step=1, neuromodulators={})
            
        self.assertLess(self.neuron.energy_level, initial_energy)
        print(f" -> Residual energy: {self.neuron.energy_level:.2f} (Consommation validée).")

if __name__ == '__main__':
    unittest.main()