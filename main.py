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
    
    print("--- Système aNA en ligne ---")
    
    # 2. Lancement du cycle
    # Puisque start_orchestrator contient une boucle 'while', 
    # c'est elle qui va piloter le système.
    try:
        await rythme.start_orchestrator(input_stream="données_test")
    except KeyboardInterrupt:
        print("\nArrêt sécurisé du système.")

if __name__ == "__main__":
    # Point d'entrée unique pour la boucle asynchrone
    asyncio.run(main())