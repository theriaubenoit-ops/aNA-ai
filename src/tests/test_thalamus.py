#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import sys
import os

# Insertion du chemin pour l'accès aux modules src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from unittest.mock import MagicMock
from anatomy.subcortical.thalamus import Thalamus

class TestThalamus(unittest.TestCase):
    def setUp(self):
        # Simulation des cibles du Thalamus (les Lobes du Cortex)
        self.mock_frontal_lobe = MagicMock()
        self.mock_parietal_lobe = MagicMock()
        self.mock_limbic_system = MagicMock()
        
        # Initialisation du Thalamus avec ses dépendances
        self.thalamus = Thalamus(
            frontal=self.mock_frontal_lobe,
            parietal=self.mock_parietal_lobe,
            limbic=self.mock_limbic_system
        )

    def test_relay_to_frontal(self):
        """Scénario : Une donnée de décision/planification doit aller au Lobe Frontal"""
        print("\n[TEST THALAMUS : ROUTAGE FRONTAL]")
        raw_data = {"type": "decision", "content": "Execute Protocol 9"}
        
        self.thalamus.relay(raw_data)
        
        # Vérification : Le signal a-t-il bien été envoyé au frontal ?
        self.mock_frontal_lobe.receive.assert_called_once_with(raw_data)
        print(" -> Signal 'decision' relayé avec succès au Lobe Frontal.")

    def test_limbic_integration(self):
        """Scénario : Le Thalamus doit consulter le système limbique pour l'importance"""
        print("\n[TEST THALAMUS : APPEL LIMBIQUE]")
        raw_data = {"type": "sensory", "content": "High Temperature"}
        
        self.thalamus.relay(raw_data)
        
        # Vérification : Le système limbique a-t-il été sollicité ?
        self.mock_limbic_system.process_experience.assert_called_once()
        print(" -> Consultation du Système Limbique effectuée pour filtrage émotionnel.")

if __name__ == '__main__':
    unittest.main()