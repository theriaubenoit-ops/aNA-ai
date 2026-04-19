#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
aNA AI Project v5.3 - Test Autonomy 

Description: This test is designed to validate the autonomous behaviors of the aNA system in isolation. It simulates an interactive environment where the system can respond to user input without external dependencies. The test checks the system's ability to process sensory input, modulate internal states, and produce outputs based on its internal logic and chemical states. It also verifies that the system can maintain a basic level of consciousness and metabolic regulation while interacting with the environment.

Architecture and neuroinformatics: Theriault Benoit
"""
import unittest
import numpy as np
import asyncio
import termios
import tty
import select
import os
import sys

# The project root is defined dynamically.
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from anatomy.subcortical.thalamus import Thalamus
from anatomy.limbic.hippocampus import Hippocampus
from anatomy.base.neuromodulator import Neuromodulator
from core.pulse import Pulse

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
    print("▓░                                                 _    _    _  ░▓▒▓  ░▓\n\n")

def is_data():
    """Checks if a key is pressed without blocking the script."""
    return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

def get_input_non_blocking():
    """Checks if a key is pressed without stopping the program."""
    if select.select([sys.stdin], [], [], 0)[0]:
        return sys.stdin.read(1)
    return None

async def interactive_keyboard_input(thalamus):
    """Loop that listens to the keyboard in real time."""
    print("⌨️ Interactive mode active. Type your commands (e.g., MOON, MARS, etc.)")
    old_settings = termios.tcgetattr(sys.stdin)
    try:
        tty.setcbreak(sys.stdin.fileno())
        while True:
            char = get_input_non_blocking() # Never stop!
    
            # 1. Thalamic processing (if char is None, it does nothing)
            if char: # Processing only occurs if a key is pressed.
                # We create a minimal payload for the Thalamus 
                payload = {"signal_label": char, "intensity": 0.5, "nucleus": "MGN"}
                # We pass the feedback 0.0 because there is no cortical column in this isolated test

                if char: 
                    print(f"\n[Input] Key detected: {char}") 
                    payload = {"signal_label": char, "intensity": 0.5, "nucleus": "MGN"}
                    await thalamus.process_payload(payload, l6_feedback=0.0)
            
            await asyncio.sleep(0.1) # System breathing
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

async def main():
    # --- Initialisation ---
    #from anatomy.base.neuromodulator import Neuromodulator
    #from core.pulse import Pulse
    
    neuromod_core = Neuromodulator()
    heart = Pulse()
    hippo = Hippocampus(neuromodulator_core=neuromod_core)
    
    # Signature correction: not 'hippo=', but 'hippocampus='
    thalamus = Thalamus(
        hippocampus=hippo, 
        pulse=heart, 
        neuromodulator_core=neuromod_core
    )
    
    print("\n🚀 STARTING THE INTERACTIVE AUTONOMY TEST")
    print("="*50)

    # Instead of simulating thalamic vibration, we activate consciousness
    # and metabolism management
    thalamus.is_autonomous = True
    
    # Asynchronous tasks
    consciousness_task = asyncio.create_task(thalamus.internal_consciousness_loop())
    input_task = asyncio.create_task(interactive_keyboard_input(thalamus))
    
    # We rotate the whole thing
    await asyncio.gather(consciousness_task, input_task)

# --- SCRIPT ENTRY POINT ---
if __name__ == "__main__":
    create_ascii_header()
    try:
        # Launches the asyncio event loop for orchestration
        asyncio.run(main())
    except KeyboardInterrupt:
        # Allows you to exit cleanly with Ctrl+C
        print("\n🛑 Simulation interrupted by the user.")
    except Exception as e:
        print(f"\n❌ Fatal error during execution: {e}")
    print("\n  *Every measurement reflected here is a digital bridge to biological reality,")
    print("   designed to synthesize the fundamental principles of living systems.\n")