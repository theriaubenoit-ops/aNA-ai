#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
aNA AI Project v5.4 - Test Neuron (In Vitro Validation)

Description: This script isolates the fundamental unit of aNA (the neuron) 
and submits it to three extreme biological stress tests:
1. Homeostasis & Myelination (Base learning)
2. Saliance Guard (Anti-Hallucination via chemical clamping)
3. Metabolic Survival (ATP preservation over processing)

Architecture, concept and supervision: Theriault Benoit
Collaboration, research and code: Google DeepMind (Gemini)
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
    print("▓███▓▒      AI inspired by natural plasticity  ✴️  a    N    A  ▒▓█▒▓ ▒▓█▒Autonomous Neural Architecture v5.4  ▒▓▓")
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
        print("\n[SCENARIO A: HOMEOSTASIS AND MYELINATION]")
        
        # Signal normal (suffisant pour atteindre le seuil)
        self.neuron.receive_input(30.0, {'no_gas': 0.1}) 
        self.neuron.update(time_step=1, neuromodulators={'no_gas': 0.1})
        
        self.assertTrue(self.neuron.is_firing)
        self.assertLess(self.neuron.energy_level, 1.0)
        self.assertGreater(self.neuron.myelination_level, 0.0)
        
        print(f" -> Discharge successful. Remaining energy: {self.neuron.energy_level:.4f}.")
        print(f" -> Reinforced structure (Myelination): {self.neuron.myelination_level:.4f}.")

    def test_02_saliance_guard(self):
        """Scénario B : La Garde de la Saliance (Protection du Pattern / Anti-Hallucination)"""
        print("\n[SCENARIO B: GUARDING SALIANCE]")
        
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
        
        print(f" -> Pure potential (without chemicals): {potentiel_pur:.2f} mV")
        print(f" -> Potential under Dopamine/Norepinephrine: {potentiel_chimique:.2f} mV")
        print(f" -> Chemical deformation contained in: +{diff:.2f} mV")
        
        # L'Architecte exige que le signal ne soit pas corrompu. 
        # Sans la garde de saliance, la différence exploserait.
        self.assertLess(diff, 10.0)
        print(" -> Guard confirmed: The neuron protects the strong signal from chemical hallucinations.")

    def test_03_metabolic_survival(self):
        """Scénario C : L'Épuisement Métabolique (La survie avant la fonction)"""
        print("\n[SCENARIO C: METABOLIC EXHAUSTION]")
        
        # On draine l'énergie sous le seuil critique de survie
        self.neuron.energy_level = 0.05 
        
        # On tente de forcer une décharge avec un stimulus massif (100.0)
        self.neuron.receive_input(100.0, {})
        self.neuron.update(time_step=2, neuromodulators={})
        
        # Le neurone DOIT REFUSER de décharger pour se protéger
        self.assertFalse(self.neuron.is_firing)
        
        # La "pompe à glucose" (récupération d'énergie) doit s'être activée
        self.assertGreater(self.neuron.energy_level, 0.05)
        
        print(" -> Action canceled: The neuron refuses to discharge below the critical threshold.")
        print(f" -> Survival mode active. Energy regeneration: {self.neuron.energy_level:.4f}.")

if __name__ == '__main__':
    create_ascii_header()
    unittest.main()