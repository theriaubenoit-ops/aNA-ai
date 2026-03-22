#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import numpy as np
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from unittest.mock import MagicMock
from anatomy.limbic.limbic_system import LimbicSystem

class TestLimbicSystem(unittest.TestCase):
    def setUp(self):
        # On simule (Mock) les organes pour isoler le Système Limbique
        self.mock_amygdala = MagicMock()
        self.mock_hippocampus = MagicMock()
        self.limbic = LimbicSystem(self.mock_amygdala, self.mock_hippocampus)

    def test_routine_experience(self):
        """Scénario : Une donnée neutre (Arousal faible)"""
        print("\n[SCÉNARIO : EXPÉRIENCE DE ROUTINE]")
        self.mock_amygdala.update_activity.return_value = {"cortisol": 0.1, "adrenaline": 0.1}
        
        is_critical = self.limbic.process_experience("Low light", "Sensor_Data_01")
        
        importance = self.mock_hippocampus.encode.call_args[1]['importance']
        print(f" -> Donnée : 'Low light' | Importance calculée : {importance:.2f}")
        print(f" -> État Critique : {'ALERTE !' if is_critical else 'Normal'}")
        
        self.assertFalse(is_critical)
        self.assertLess(importance, 1.2)

    def test_shock_experience(self):
        """Scénario : Un événement majeur (Arousal élevé)"""
        print("\n[SCÉNARIO : ÉVÉNEMENT MAJEUR (CHOC)]")
        self.mock_amygdala.update_activity.return_value = {"cortisol": 0.8, "adrenaline": 0.9}
        
        is_critical = self.limbic.process_experience("System Breach!", "Security_Alert_99")
        
        importance = self.mock_hippocampus.encode.call_args[1]['importance']
        print(f" -> Donnée : 'System Breach!' | Importance calculée : {importance:.2f}")
        print(f" -> État Critique : {'🔴 ALERTE DÉCLENCHÉE' if is_critical else 'Normal'}")
        
        self.assertTrue(is_critical)
        self.assertGreater(importance, 1.5)

if __name__ == '__main__':
    unittest.main()
