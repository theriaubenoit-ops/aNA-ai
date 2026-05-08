#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Projet aNA IA v5.4 - Neurone de test (validation in vitro)

Description : Ce script isole l'unité fondamentale de l'aNA (le neurone)
et la soumet à trois tests de stress biologique extrêmes :
1. Homéostasie et myélinisation (apprentissage de base)
2. Protection contre les hallucinations (inhibition chimique)
3. Survie métabolique (préservation de l'ATP par rapport au traitement)

Architecture, conception et supervision : Benoit Theriault
Collaboration, recherche et code : Google Gemini
"""
import unittest
import numpy as np
import os
import sys

# The project root is defined dynamically.
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from src.anatomy.base.neuron import Neuron, NeuronConfig

def create_ascii_header():
    print(f"\033c") 
    print("░              ░ ░░░▒▒▓▒▓▒▒▒▒▒░░▒▒░▒▒▒▓▒▓▒                                                                     ░ ░")
    print("▒░░   ░░░░░░░░░░▒▒▓▓▓▓▓▓▓██▓▒▒▒░░░▒▒▒▒▒░░░▒▒▓▓▒                                                         ░░░░░░▒▒▒▒")
    print("░░░░░░░░░░░░░▒▒▒▓▓▓▓▓▓██████▓▓▒▒▒░░▒▒▓▓▓▒▒▒░░▒▒▒▒▓▒                                        ░ ░░░ ░ ░░░░░░░░░▒▒▒▒▒▒")
    print("▓▒▒▒▒▒▒▒▒▓▒▓▓▓▓▓▓██████▓▒▒ ▒   ▒▓▒▓▒▒▒▒▓▒▓ ██▓▓▓▒▒▒▒▓      ░░▒▒▒▒▒▒▒░░░░░░▒░░░░▒▒░░▒░░░░░░░░░░░░░░░░░▒░▒▒▒░▒▒▒▓▓▓▓")
    print("▒▒▒▒▒▒▒▓▓▓▓▓████▓▓░                 ░░▒▒▒▓█▓░▓▓█▓▓ ░▒▓  ▒▓▓▓▓▓█▓▓▓█▓▒▒▒▓▓▒░░░░▒▓█▓▓▓▓▓▒▓▒▒▒▒▒▒▒░░░░░░░░░░░░░░▒▒▒▒▒")
    print("▒▒▓▒▓▓▓▓█████▓▒                         ░▒▒▓░ ▓██▓                ▒▓▒▒░░▒▓▒░░▒▓███▓█▓▓▓▓▓▓▓▓▓▓▓▒▓▒▒▒▒▒▒▒▒▒▒▓▒▓▓▓▓▓")
    print("▓▓▓█████▓░                                    ░░▒▒ _    _    _ ░▒░▒▒▒▓▒▓▒▓▒▓█▓███▓▒▓▓▓▓▓▓▓▓▓▓▓▓█▓██▓▓▓▓▓█▓████████")
    print("▓███▓▒  IA inspirée de la plasticité naturelle ✴️  a    N    A  ▒▓█▒▓ ▒▓█▒Architecture Neuronale Autonome v5.4 ▒▓▓")
    print("▓░                                                 _    _    _  ░▓▒▓  ░▓\n")

class TestNeuronV54(unittest.TestCase):
    def setUp(self):
        # Configuration standard reflétant la rigueur de la v5.4
        self.config = NeuronConfig(
            layer_id=1,
            resting_potential=-70.0,
            threshold_potential=-55.0,
            base_energy_consumption=0.01,
            firing_energy_cost=0.1,
            min_energy_threshold=0.1
        )
        self.position = np.array([0.0, 0.0, 0.0])
        self.neuron = Neuron(self.position, self.config)

    def test_01_homeostasis_and_plasticity(self):
        """Scénario A : Le Rythme de Croisière (Métabolisme et Myéline)"""
        print("\n[SCÉNARIO A : HOMÉOSTASIE ET MYÉLINISATION]")
        
        # Signal normal (suffisant pour atteindre le seuil)
        self.neuron.receive_input(30.0, {'no_gas': 0.1}) 
        self.neuron.update(time_step=1, neuromodulators={'no_gas': 0.1})
        
        self.assertTrue(self.neuron.is_firing)
        self.assertLess(self.neuron.energy_level, 1.0)
        self.assertGreater(self.neuron.myelination_level, 0.0)
        
        print(f" -> Décharge réussie. Énergie restante: {self.neuron.energy_level:.4f}.")
        print(f" -> Structure renforcée (Myélinisation): {self.neuron.myelination_level:.4f}.")

    def test_02_saliance_guard(self):
        """Scénario B : La Garde de la Saliance (Protection du Pattern / Anti-Hallucination)"""
        print("\n[SCÉNARIO B : LA GARDE DE LA SALIANCE]")
        
        # Neurone 1 (Contrôle) : Signal fort, environnement chimique neutre
        neuron_control = Neuron(self.position, self.config)
        neuron_control.receive_input(20.0, {})
        potentiel_pur = neuron_control.membrane_potential
        
        # Neurone 2 (Test) : Même signal fort, mais sous cocktail chimique extrême
        neuron_chem = Neuron(self.position, self.config)
        cocktail = {'dopamine': 1.0, 'norepinephrine': 1.0} # Excitation maximale
        neuron_chem.receive_input(20.0, cocktail)
        potentiel_chimique = neuron_chem.membrane_potential
        
        # La chimie doit avoir un effet, mais il doit être contenu par la saliance
        diff = potentiel_chimique - potentiel_pur
        
        print(f" -> Potentiel pur (sans chimie): {potentiel_pur:.2f} mV")
        print(f" -> Potentiel sous Dopamine/Norepinephrine: {potentiel_chimique:.2f} mV")
        print(f" -> Déformation chimique contenue à: +{diff:.2f} mV")
        
        # L'Architecte exige que le signal ne soit pas corrompu. 
        # Sans la garde de saliance, la différence exploserait.
        self.assertLess(diff, 10.0)
        print(" -> Garde confirmée : Le neurone protège le signal fort des hallucinations chimiques.")

    def test_03_metabolic_survival(self):
        """Scénario C : L'Épuisement Métabolique (La survie avant la fonction)"""
        print("\n[SCÉNARIO C : L'ÉPUISEMENT MÉTABOLIQUE]")
        
        # On draine l'énergie sous le seuil critique de survie
        self.neuron.energy_level = 0.05 
        
        # On tente de forcer une décharge avec un stimulus massif (100.0)
        self.neuron.receive_input(100.0, {})
        self.neuron.update(time_step=2, neuromodulators={})
        
        # Le neurone DOIT REFUSER de décharger pour se protéger
        self.assertFalse(self.neuron.is_firing)
        
        # La "pompe à glucose" (récupération d'énergie) doit s'être activée
        self.assertGreater(self.neuron.energy_level, 0.05)
        
        print(" -> Action annulée : Le neurone refuse de décharger sous le seuil critique.")
        print(f" -> Mode survie actif. Énergie en récupération: {self.neuron.energy_level:.4f}.")

if __name__ == '__main__':
    create_ascii_header()
    unittest.main()
