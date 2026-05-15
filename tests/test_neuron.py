#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
aNA AI Project v5.4 - Test Neuron (In Vitro Validation)

Description: Ce script isole l'unité fondamentale d'aNA (le neurone) 
et la soumet à trois tests de stress biologique alignés sur la v5.4 :
1. Homéostasie & Myélinisation (Apprentissage de base)
2. Garde de Saliance (Anti-Hallucination via clamp chimique)
3. Survie Métabolique (Priorité à l'ATP sur le traitement)

Architecture, concept and supervision: Benoit Theriault
Collaboration, research and code: Google DeepMind (Gemini)
"""
import unittest
import numpy as np
import os
import sys

# Définition dynamique du root pour l'import des modules
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
        print("\n[SCENARIO A: HOMEOSTASIS AND MYELINATION]")
        
        # On s'assure que le neurone part d'un état stable
        self.neuron.atp_flux = 1.0
        
        # Stimulation
        self.neuron.receive_input(40.0, {}) # Augmenté pour garantir le passage du seuil
        self.neuron.update(time_step=1, neuromodulators={})
        
        self.assertTrue(self.neuron.is_firing)
        
        # On vérifie que la plasticité ou la myéline a progressé
        self.assertGreater(self.neuron.myelin_level, 0.0)
        self.assertGreater(self.neuron.activity_counter, 0)
        
        print(f" -> Discharge successful. Activity counter: {self.neuron.activity_counter}")
        print(f" -> Reinforced structure (Myelination): {self.neuron.myelin_level:.4f}")

    def test_02_saliance_guard(self):
        """Scénario B : La Garde de la Saliance (Protection contre l'hallucination chimique)"""
        print("\n[SCENARIO B: GUARDING SALIANCE]")
        
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
        
        print(f" -> Pure potential (without chemistry): {potentiel_pur:.2f} mV")
        print(f" -> Potential under chemical cocktail:: {potentiel_chimique:.2f} mV")
        print(f" -> Chemical deformation contained: +{diff:.2f} mV")
        
        # Le mécanisme de Saliance doit limiter l'impact chimique pour protéger le pattern
        self.assertLess(diff, 15.0) 
        print(" -> Garde confirmée : Le neurone protège le signal fort contre la saturation chimique.")

    def test_03_metabolic_survival(self):
        """Scénario C : L'Épuisement Métabolique (La survie avant la fonction)"""
        print("\n[SCENARIO C: METABOLIC EXHAUSTION]")
        
        # On force un état d'épuisement extrême (sous le seuil de Low Power)
        self.neuron.atp_flux = 0.05 
        
        # On tente de forcer une décharge avec un stimulus massif
        self.neuron.receive_input(100.0, {})
        self.neuron.update(time_step=2, neuromodulators={})
        
        # Le neurone DOIT REFUSER de décharger pour préserver son intégrité
        self.assertFalse(self.neuron.is_firing)
        
        # La pompe de récupération doit être active malgré l'absence de décharge
        self.assertGreater(self.neuron.atp_flux, 0.05)
        
        print(" -> Action canceled: The neuron refuses the discharge as a survival measure.")
        print(f" -> Active survival mode. ATP regeneration in progress: {self.neuron.atp_flux:.4f}.")

if __name__ == '__main__':
    create_ascii_header()
    unittest.main()
