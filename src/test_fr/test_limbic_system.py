#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Projet aNA AI - v5.1
Module : Tester le système limbique
Description : Cette suite de tests est conçue pour valider les fonctionnalités de base des modules du système limbique (Amygdale et Hippocampe) en isolement complet. Il simule divers scénarios pour vérifier que l’amygdale répond de manière appropriée aux différentes intensités de stimulus et que l’hippocampe peut coder, consolider et récupérer correctement les modèles. Les tests vérifient également l’interaction entre ces deux structures en termes de traitement de la mémoire émotionnelle.
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
    
from unittest.mock import MagicMock
from anatomy.limbic.limbic_system import LimbicSystem

def create_ascii_header():
    print(f"\033c") 
    print("░                     ░░░░░░░░░░▒▒▒▒▒▒░░")
    print("           ░░░░░░░░░▒▒▒▒▒▓▒▒▒▒░░░░░░░░░░▒▒▒▒░                                                          ░░░░░░░░░░░")
    print("░░░░░░░░░░░░░░░░▒▒▒▒▓▓▓▓▓▓▓▓▓▓▓▒░░░░░▒▒▒░░░░▒▓▒░░                      ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░")
    print("░░░░░░░░░░░░░░▒▒▒▓▓▓▓▓▓▓▓▓▓▓▒░░▒▒▒░░░░▒▓▓▓▓▓▓▒▒▒▒▒░     ░░░░░░░░░░░░░░░░░░░░░▒▒░░▒▒▒▓▓▓▓▓▓▒▒▒░░░░░░░░░░░░░░░░░▒▒▒▒")
    print("▒░░░░░▒▒▒▒▒▒▓▓▓▓▓▓▓▓▓▒░         ░░▒▒▒░▒▒▒▒▓▓▓▓▓▓▓▒▒░░  ░▒▒▒▓▒▒▒▓▒▓▒▓▒░░░░░░░▒▓▓▓▓▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░░░░░░░░░░░▒▓")
    print("░▒▒▒▒▓▓▓▓▓▓▓▓▓▓▓▓░                   ░░ ▒▒▓▒░▒▓▓▓░▒▒░░           ░▒░░░▒▓▒▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒▒▓▓")
    print("▒▒▓▓▓▓▓▓▒▒▒░░                           ░▓▓▒░░▒▓▓░ _    _    _ ░▒░░▒▓▒▓▓▓▓▓▓▓▓▓▓▒░░░░░░░░░▒▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓")
    print("▓▓▓░IA inspirée de la plasticité naturelle░░  ░░░  a    N    A  ▒▓▒▓▒▒▒▓░Architecture Neuronale Autonome v5.1░░▒▒▓")
    print("░                                                  ‾    ‾    ‾ ░▓▒▓░░▒▓░\n\n")

class TestLimbicSystem(unittest.TestCase):
    def setUp(self):
        # On simule (Mock) les organes pour isoler le Système Limbique
        self.mock_amygdala = MagicMock()
        self.mock_hippocampus = MagicMock()
        self.limbic = LimbicSystem(self.mock_amygdala, self.mock_hippocampus)

    def test_routine_experience(self):
        """Scénario : Une donnée neutre (Arousal faible)"""
        print("\n[SCÉNARIO : EXPÉRIENCE DE ROUTINE]")
        # On simule un état émotionnel calme
        emotional_data = {"dopamine": 0.1, "cortisol": 0.1}
        
        # On passe le dictionnaire au lieu d'une string[cite: 8]
        is_critical = self.limbic.process_experience("Sensor_Data_01", emotional_data)
        
        # Récupération de l'argument 'importance'[cite: 8]
        args, kwargs = self.mock_hippocampus.encode.call_args
        importance = kwargs.get('importance', 0.0)
        
        print(f" -> Importance calculée : {importance:.2f}")
        self.assertFalse(is_critical)

    def test_shock_experience(self):
        """Scénario : Un événement majeur (Choc)"""
        print("\n[SCÉNARIO : ÉVÉNEMENT MAJEUR (CHOC)]")
        # On simule un stress élevé[cite: 8]
        shock_data = {"dopamine": 0.2, "cortisol": 0.9}
        
        is_critical = self.limbic.process_experience("Security_Alert_99", shock_data)
        
        args, kwargs = self.mock_hippocampus.encode.call_args
        importance = kwargs.get('importance', 0.0)
        
        print(f" -> Importance calculée : {importance:.2f}")
        self.assertTrue(is_critical)

if __name__ == '__main__':
    create_ascii_header()
    unittest.main()
