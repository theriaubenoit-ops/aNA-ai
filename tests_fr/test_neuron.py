#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Projet aNA IA v5.4 - Neurone de test (validation in vitro)

Description : Ce script isole l'unité fondamentale de l'aNA (le neurone)
et la soumet à trois tests de stress biologique extrêmes :
1. Homéostasie et myélinisation (apprentissage de base)
2. Protection contre les hallucinations (inhibition chimique)
3. Survie métabolique (préservation de l'ATP par rapport au traitement)

Architecture et neuroinformatique : Thériault Benoit
Collaboration, recherche et code : Google DeepMind (Gemini)
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
        """
        Initialisation v5.4 : Le neurone récupère ses constantes 
        directement depuis le profil actif dans config.py.
        """
        self.position = np.array([0.0, 0.0, 0.0])
        # On teste ici un neurone de la couche IV (Gateway sensoriel)
        self.config = NeuronConfig(layer_id=4)
        self.neuron = Neuron(self.position, self.config)

    def test_01_homeostasis_and_plasticity(self):
        """Scénario A : Le Rythme de Croisière (Métabolisme et Myéline)"""
        print("\n[SCÉNARIO A : HOMÉOSTASIE ET MYÉLINISATION]")
        
        # On s'assure que le neurone part d'un état stable
        self.neuron.atp_flux = 1.0
        
        # Stimulation
        self.neuron.receive_input(40.0, {}) # Augmenté pour garantir le passage du seuil
        self.neuron.update(time_step=1, neuromodulators={})
        
        self.assertTrue(self.neuron.is_firing)
        
        # On vérifie que la plasticité ou la myéline a progressé
        self.assertGreater(self.neuron.myelin_level, 0.0)
        self.assertGreater(self.neuron.activity_counter, 0)
        
        print(f" -> Décharge réussie. Compteur d'activité : {self.neuron.activity_counter}")
        print(f" -> Structure renforcée (Myélinisation) : {self.neuron.myelin_level:.4f}")

    def test_02_saliance_guard(self):
        """Scénario B : La Garde de la Saliance (Protection du Pattern / Anti-Hallucination)"""
        print("\n[SCÉNARIO B : LA GARDE DE LA SALIANCE]")
        
        # Neurone de contrôle : Signal fort sans bruit chimique
        neuron_control = Neuron(self.position, self.config)
        neuron_control.receive_input(20.0, {})
        potentiel_pur = neuron_control.membrane_potential
        
        # Neurone test : Même signal, mais avec cocktail chimique extrême (Dopamine + Noradrénaline)
        neuron_chem = Neuron(self.position, self.config)
        cocktail = {'dopamine': 1.0, 'norepinephrine': 1.0}
        neuron_chem.receive_input(20.0, cocktail)
        potentiel_chimique = neuron_chem.membrane_potential
        
        # Calcul de la déformation
        diff = potentiel_chimique - potentiel_pur
        
        print(f" -> Potentiel pur (sans chimie) : {potentiel_pur:.2f} mV")
        print(f" -> Potentiel sous cocktail chimique : {potentiel_chimique:.2f} mV")
        print(f" -> Déformation chimique contenue : +{diff:.2f} mV")
        
        # Le mécanisme de Saliance doit limiter l'impact chimique pour protéger le pattern
        self.assertLess(diff, 15.0) 
        print(" -> Garde confirmée : Le neurone protège le signal fort contre la saturation chimique.")

    def test_03_metabolic_survival(self):
        """Scénario C : L'Épuisement Métabolique (La survie avant la fonction)"""
        print("\n[SCÉNARIO C : L'ÉPUISEMENT MÉTABOLIQUE]")
        
        # On force un état d'épuisement extrême (sous le seuil de Low Power)
        self.neuron.atp_flux = 0.05 
        
        # On tente de forcer une décharge avec un stimulus massif
        self.neuron.receive_input(100.0, {})
        self.neuron.update(time_step=2, neuromodulators={})
        
        # Le neurone DOIT REFUSER de décharger pour préserver son intégrité
        self.assertFalse(self.neuron.is_firing)
        
        # La pompe de récupération doit être active malgré l'absence de décharge
        self.assertGreater(self.neuron.atp_flux, 0.05)
        
        print(" -> Action annulée : Le neurone refuse la décharge par mesure de survie.")
        print(f" -> Mode survie actif. Régénération ATP en cours : {self.neuron.atp_flux:.4f}.")

if __name__ == '__main__':
    create_ascii_header()
    unittest.main()
