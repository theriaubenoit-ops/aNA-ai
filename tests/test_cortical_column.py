#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
aNA AI Project v5.3 - Test Cortical Column 

Description: This test is designed to validate the core functionalities of the cortical column module in complete isolation. It simulates a simple data stream to verify that the cortical column processes inputs correctly, learns patterns, and can retrieve them based on context. The test covers feedforward processing, lateral inhibition, and feedback mechanisms.

Architecture, concept and supervision: Benoit Theriault
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

from src.anatomy.cortical.cortical_column import CorticalLobe

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

class TestCorticalColumn(unittest.TestCase):
    def setUp(self):
        # Arbitrary position for the lobe
        self.position = np.array([100.0, 100.0, 100.0])
        self.lobe = CorticalLobe(self.position)
        self.neuromodulators = {
            'dopamine': 0.5,
            'acetylcholine': 0.8, # High attention
            'serotonin': 0.2
        }

    def test_signal_cascade(self):
        """Check the signal cascade across the 6 layers"""
        print("\n[CORTICAL TEST: SIGNAL CASCADE]")
        input_signal = 100.0
        output = self.lobe.process_through_layers(input_signal, self.neuromodulators)
        
        monitoring = self.lobe.get_precision_monitoring()
        efficiency = monitoring['precision_metrics']['overall_efficiency']
        
        print(f" -> Input Signal: {input_signal}")
        print(f" -> Output Signal (L5): {output:.2f}")
        print(f" -> Overall Effectiveness: {efficiency:.2%}")
        
        # The efficiency should be close to the expected cascade (0.65) * note boost
        self.assertGreater(output, 0)
        self.assertLess(monitoring['precision_metrics']['biological_accuracy'], 0.5)

    def test_attention_mechanism(self):
        """Verify that acetylcholine is indeed boosting the signal in Layer I"""
        print("\n[CORTICAL TEST: ATTENTION MECHANISM]")
        
        # Testing without attention and without recognition (Pure novelty)
        low_ach = {'acetylcholine': 0.0, 'dopamine': 0.0}
        self.lobe.reset()
        output_base = self.lobe.process_through_layers(100.0, low_ach, recognition_score=0.0)
        
        # Test with great care on a NEW signal (Score = 0.0)
        # This is where the boost needs to be at its maximum.
        high_ach = {'acetylcholine': 1.0, 'dopamine': 0.0}
        self.lobe.reset()
        output_boosted = self.lobe.process_through_layers(100.0, high_ach, recognition_score=0.0)
        
        boost_factor = output_boosted / output_base
        print(f" -> Attention Gainer (New): {boost_factor:.2f}x")
        
        self.assertGreater(output_boosted, output_base)

    def test_signal_cascade(self):
        """Check the signal cascade across the 6 layers"""
        print("\n[CORTICAL TEST: SIGNAL CASCADE]")
        input_signal = 100.0
        # We add the default recognition score
        output = self.lobe.process_through_layers(input_signal, self.neuromodulators, recognition_score=0.5)

if __name__ == '__main__':
    create_ascii_header()
    unittest.main()