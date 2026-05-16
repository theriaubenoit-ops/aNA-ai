#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
aNA AI Project v5.4 - Test Amygdala

Description: This test checks the amygdala's responses to different levels of stimulus, simulating threat and calm scenarios. The goal is to ensure that the activation and return-to-homeostasis mechanisms are functioning correctly, by measuring adrenaline and cortisol levels. The test covers baseline arousal, high threat response, and homeostasis reset.

Architecture, concept and supervision: Theriault_Benoit
Collaboration, research and code: DeepMind_Gemini
"""

import unittest
import numpy as np
import os
import sys

# The project root is defined dynamically.
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from src.anatomy.limbic.amygdala import Amygdala

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

class TestAmygdala(unittest.TestCase):
    def setUp(self):
        # Amygdala Initialization
        self.amygdala = Amygdala()

    def test_baseline_arousal(self):
        """Checks the resting state (Baseline)"""
        print("\n[TEST AMYGDALE : RESTING STATE]")
        status = self.amygdala.update_activity(stimulus_intensity=0.1)
        print(f" -> Low intensity (0.1) | Cortisol: {status['cortisol']:.2f}")
        self.assertLess(status['cortisol'], 0.3)

    def test_high_threat_response(self):
        """Checks the reaction to an intense stimulus (Threat)"""
        print("\n[TEST AMYGDALE : ALERT REACTION]")
        status = self.amygdala.update_activity(stimulus_intensity=0.9)
        print(f" -> High intensity (0.9) | Adrenaline: {status['adrenaline']:.2f}")
        # Adrenaline levels must be significantly high.
        self.assertGreater(status['adrenaline'], 0.7)

    def test_homeostasis_reset(self):
        """Check if the system can return to a calm state (Homeostasis)"""
        print("\n[TEST AMYGDALE : RETURN TO CALM]")
        # We simulate a peak followed by a calm period
        self.amygdala.update_activity(stimulus_intensity=1.0)
        status_calm = self.amygdala.update_activity(stimulus_intensity=0.0)
        print(f" -> After peak, intensity 0.0 | Adrenaline: {status_calm['adrenaline']:.2f}")
        self.assertLess(status_calm['adrenaline'], 0.5)

if __name__ == '__main__':
    create_ascii_header()
    unittest.main()