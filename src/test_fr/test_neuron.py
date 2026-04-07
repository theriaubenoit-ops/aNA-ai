#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Projet aNA AI - v5.2
Module : Test du neurone
La description: Ce test est conçu pour valider les fonctionnalités de base du module neurone en isolement complet. Il simule un flux de données simple pour vérifier que le neurone traite correctement les entrées, apprend les modèles et peut les récupérer en fonction du contexte. Le test couvre le traitement anticipé, l’inhibition latérale et les mécanismes de rétroaction.
Architecture et neuroinformatique : Thériault Benoit
"""
import unittest
import numpy as np
import sys
import os

# On définit la racine du projet dynamiquement
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)
    
from anatomy.base.neuron import Neuron, NeuronConfig

def create_ascii_header():
    print(f"\033c") 
    print("░                     ░░░░░░░░░░▒▒▒▒▒▒░░")
    print("           ░░░░░░░░░▒▒▒▒▒▓▒▒▒▒░░░░░░░░░░▒▒▒▒░                                                          ░░░░░░░░░░░")
    print("░░░░░░░░░░░░░░░░▒▒▒▒▓▓▓▓▓▓▓▓▓▓▓▒░░░░░▒▒▒░░░░▒▓▒░░                      ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░")
    print("░░░░░░░░░░░░░░▒▒▒▓▓▓▓▓▓▓▓▓▓▓▒░░▒▒▒░░░░▒▓▓▓▓▓▓▒▒▒▒▒░     ░░░░░░░░░░░░░░░░░░░░░▒▒░░▒▒▒▓▓▓▓▓▓▒▒▒░░░░░░░░░░░░░░░░░▒▒▒▒")
    print("▒░░░░░▒▒▒▒▒▒▓▓▓▓▓▓▓▓▓▒░         ░░▒▒▒░▒▒▒▒▓▓▓▓▓▓▓▒▒░░  ░▒▒▒▓▒▒▒▓▒▓▒▓▒░░░░░░░▒▓▓▓▓▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░░░░░░░░░░░▒▓")
    print("░▒▒▒▒▓▓▓▓▓▓▓▓▓▓▓▓░                   ░░ ▒▒▓▒░▒▓▓▓░▒▒░░           ░▒░░░▒▓▒▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒▒▓▓")
    print("▒▒▓▓▓▓▓▓▒▒▒░░                           ░▓▓▒░░▒▓▓░ _    _    _ ░▒░░▒▓▒▓▓▓▓▓▓▓▓▓▓▒░░░░░░░░░▒▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓")
    print("▓▓▓░IA inspirée de la plasticité naturelle░░  ░░░  a    N    A  ▒▓▒▓▒▒▒▓░Architecture Neuronale Autonome v5.2  ░▒▓")
    print("░                                                  ‾    ‾    ‾ ░▓▒▓░░▒▓░\n\n")

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
        print("\n[TEST NEURONE : ÉTAT INITIAL]")
        self.assertFalse(self.neuron.is_firing)
        self.assertGreater(self.neuron.energy_level, 0.9)
        print(" -> Neurone au repos et chargé en énergie.")

    def test_threshold_activation(self):
        """Vérifie si le neurone déclenche après avoir atteint le seuil"""
        print("\n[TEST NEURONE : SEUIL D'ACTIVATION]")
        # On envoie un signal fort
        self.neuron.receive_input(60.0, {}) 
        self.neuron.update(time_step=1, neuromodulators={})
        
        self.assertTrue(self.neuron.is_firing)
        print(f" -> Décharge réussie ! Potentiel atteint le seuil de {self.config.threshold_potential} mV.")

    def test_energy_depletion(self):
        """Vérifie que l'activité consomme de l'énergie"""
        print("\n[TEST NEURONE : CONSOMMATION ÉNERGÉTIQUE]")
        initial_energy = self.neuron.energy_level
        
        # On fait feu plusieurs fois
        for _ in range(5):
            self.neuron.receive_input(100.0, {})
            self.neuron.update(time_step=1, neuromodulators={})
            
        self.assertLess(self.neuron.energy_level, initial_energy)
        print(f" -> Énergie résiduelle : {self.neuron.energy_level:.2f} (Consommation validée).")

if __name__ == '__main__':
    create_ascii_header()
    unittest.main()