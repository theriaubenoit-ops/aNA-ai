#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Integrated System Test - The Digital Bridge
Tests the synchronization between Pulse, Thalamus, and Neural Transmission.
"""

import asyncio
import sys
import os

# Ajustement du chemin pour remonter d'un niveau et trouver 'src'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importations mises à jour selon votre structure
from core.pulse import Pulse
from anatomy.subcortical.thalamus import Thalamus
from anatomy.base.neural_transmission import NeuralTransmission, TransmissionBridge

async def main():
    # Initialisation des unités fonctionnelles
    rythme = Pulse() #
    filtre = Thalamus() #[cite: 2]
    
    print("--- ⚡ aNA System Pulse: Integration Test ---")
    
    try:
        # L'orchestrateur utilise le filtre pour le traitement à haut débit[cite: 2]
        await rythme.start_orchestrator(input_stream="sensory_payload_v5", filter_unit=filtre) #[cite: 2]
    except KeyboardInterrupt:
        print("\n🛑 Safe system shutdown.")

if __name__ == "__main__":
    asyncio.run(main())
