#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import sys
import os

# Configuration du chemin
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'scr')))

from core.tempo import Tempo
from anatomy.thalamus import Thalamus
from core.neural_transmission import NeuralTransmission, TransmissionBridge

async def main():
    # Initialization of functional units
    rythme = Tempo()
    filtre = Thalamus()
    
    print("--- aNA System Online ---")
    
    # The orchestrator now takes the filter as a dependency
    # to maintain high-throughput processing
    try:
        # We pass the filter unit so Tempo can use it internally
        await rythme.start_orchestrator(input_stream="sensory_payload_v5", filter_unit=filtre)
    except KeyboardInterrupt:
        print("\nSafe system shutdown.")

if __name__ == "__main__":
    asyncio.run(main())
