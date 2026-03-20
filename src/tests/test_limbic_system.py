#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import sys
import os

# Ajustement du chemin pour remonter d'un niveau et trouver 'src'
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
        # Simulation d'un état calme (Cortisol/Adrénaline bas)
        self.mock_amygdala.update_activity.return_value = {"cortisol": 0.1, "adrenaline": 0.1}
        
        is_critical = self.limbic.process_experience("Low light", "Sensor_Data_01")
        
        # Vérifications
        self.assertFalse(is_critical) # Ne doit pas être critique
        # L'importance doit être proche de 1.1 ((0.1+0.1)/2 + 1.0)
        args, kwargs = self.mock_hippocampus.encode.call_args
        self.assertLess(kwargs['importance'], 1.2)

    def test_shock_experience(self):
        """Scénario : Un événement majeur (Arousal élevé)"""
        # Simulation d'un état d'alerte (Cortisol/Adrénaline hauts)
        self.mock_amygdala.update_activity.return_value = {"cortisol": 0.8, "adrenaline": 0.9}
        
        is_critical = self.limbic.process_experience("System Breach!", "Security_Alert_99")
        
        # Vérifications
        self.assertTrue(is_critical) # Doit déclencher le signal d'alerte
        # L'importance doit être élevée (~1.85)
        args, kwargs = self.mock_hippocampus.encode.call_args
        self.assertGreater(kwargs['importance'], 1.5)

if __name__ == '__main__':
    unittest.main()