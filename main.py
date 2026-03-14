#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import sys
import os

# Configuration du chemin
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'scr')))

from core.tempo import Tempo
from anatomy.thalamus import Thalamus
# from core.neural_transmission import NeuralTransmission, TransmissionBridge

async def main():
    # 1. Initialisation
    rythme = Tempo()
    filtre = Thalamus()
    
    print("--- aNA online system ---")
    
    # 2. Starting the cycle
    # Since start_orchestrator contains a 'while' loop,
    # it is this loop that will control the system.
    try:
        await rythme.start_orchestrator(input_stream="test_data")
    except KeyboardInterrupt:
        print("\nSafe system shutdown.")

if __name__ == "__main__":
    # Single entry point for the asynchronous loop
    asyncio.run(main())
