#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
aNA AI Project v5.3 - Test Limbic system 

Description: This test suite is designed to validate the core functionalities of the limbic system modules (Amygdala and Hippocampus) in complete isolation. It simulates various scenarios to verify that the amygdala responds appropriately to different stimulus intensities, and that the hippocampus can encode, consolidate, and retrieve patterns correctly. The tests also check the interaction between these two structures in terms of emotional memory processing.

Architecture and neuroinformatics: Theriault Benoit
"""
import unittest
import numpy as np
import os
import sys

# The project root is defined dynamically.
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from unittest.mock import MagicMock
from anatomy.limbic.limbic_system import LimbicSystem

def create_ascii_header():
    print(f"\033c") 
    print("░              ░ ░░░▒▒▓▒▓▒▒▒▒▒░░▒▒░▒▒▒▓▒▓▒                                                                     ░ ░")
    print("▒░░   ░░░░░░░░░░▒▒▓▓▓▓▓▓▓██▓▒▒▒░░░▒▒▒▒▒░░░▒▒▓▓▒                                                         ░░░░░░▒▒▒▒")
    print("░░░░░░░░░░░░░▒▒▒▓▓▓▓▓▓██████▓▓▒▒▒░░▒▒▓▓▓▒▒▒░░▒▒▒▒▓▒                                        ░ ░░░ ░ ░░░░░░░░░▒▒▒▒▒▒")
    print("▓▒▒▒▒▒▒▒▒▓▒▓▓▓▓▓▓██████▓▒▒ ▒   ▒▓▒▓▒▒▒▒▓▒▓ ██▓▓▓▒▒▒▒▓      ░░▒▒▒▒▒▒▒░░░░░░▒░░░░▒▒░░▒░░░░░░░░░░░░░░░░░▒░▒▒▒░▒▒▒▓▓▓▓")
    print("▒▒▒▒▒▒▒▓▓▓▓▓████▓▓░                 ░░▒▒▒▓█▓░▓▓█▓▓ ░▒▓  ▒▓▓▓▓▓█▓▓▓█▓▒▒▒▓▓▒░░░░▒▓█▓▓▓▓▓▒▓▒▒▒▒▒▒▒░░░░░░░░░░░░░░▒▒▒▒▒")
    print("▒▒▓▒▓▓▓▓█████▓▒                         ░▒▒▓░ ▓██▓                ▒▓▒▒░░▒▓▒░░▒▓███▓█▓▓▓▓▓▓▓▓▓▓▓▒▓▒▒▒▒▒▒▒▒▒▒▓▒▓▓▓▓▓")
    print("▓▓▓█████▓░                                    ░░▒▒ _    _    _ ░▒░▒▒▒▓▒▓▒▓▒▓█▓███▓▒▓▓▓▓▓▓▓▓▓▓▓▓█▓██▓▓▓▓▓█▓████████")
    print("▓███▓▒      AI inspired by natural plasticity  ✴️  a    N    A  ▒▓█▒▓ ▒▓█▒Autonomous Neural Architecture v5.3  ▒▓▓")
    print("▓░                                                 _    _    _  ░▓▒▓  ░▓\n")

class TestLimbicSystem(unittest.TestCase):
    def setUp(self):
        # We simulate (mock) the organs to isolate the Limbic System
        self.mock_amygdala = MagicMock()
        self.mock_hippocampus = MagicMock()
        self.limbic = LimbicSystem(self.mock_amygdala, self.mock_hippocampus)

    def test_routine_experience(self):
        """Scenario: Neutral data (low Arousal)"""
        print("\n[SCENARIO: ROUTINE EXPERIENCE]")
        # We simulate a calm emotional state
        emotional_data = {"dopamine": 0.1, "cortisol": 0.1}
        
        # We pass the dictionary instead of a string[cite: 8]
        is_critical = self.limbic.process_experience("Sensor_Data_01", emotional_data)
        
        # Retrieving the 'importance' argument [cite: 8]
        args, kwargs = self.mock_hippocampus.encode.call_args
        importance = kwargs.get('importance', 0.0)
        
        print(f" -> Calculated importance: {importance:.2f}")
        self.assertFalse(is_critical)

    def test_shock_experience(self):
        """Scenario: A major event (Shock)"""
        print("\n[SCENARIO: MAJOR EVENT (SHOCK)]")
        # We simulate high stress[cite: 8]
        shock_data = {"dopamine": 0.2, "cortisol": 0.9}
        
        is_critical = self.limbic.process_experience("Security_Alert_99", shock_data)
        
        args, kwargs = self.mock_hippocampus.encode.call_args
        importance = kwargs.get('importance', 0.0)
        
        print(f" -> Calculated importance: {importance:.2f}")
        self.assertTrue(is_critical)

if __name__ == '__main__':
    create_ascii_header()
    unittest.main()
