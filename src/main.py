#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import numpy as np
import sys
import os

# Ajout du chemin src pour s'assurer que les imports fonctionnent partout
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.pulse import pulse
from anatomy.subcortical.thalamus import Thalamus
from anatomy.limbic.limbic_system import LimbicSystem

async def main():
    print("--- Initialisation de l'Architecture aNA v5.0 ---")
    
    # 1. Préparation des organes (L'instrumentation)
    thalamus = Thalamus()
    limbic = LimbicSystem()
    
    # 2. Simulation d'un flux d'entrée (Le "Sensory Stream")
    # Dans le futur, ceci proviendra de votre InputGateway
    mock_sensory_stream = [0.5, 0.2, 0.9] 

    try:
        # 3. Lancement du battement de cœur
        # On passe le thalamus comme unité de filtrage (filter_unit)
        await pulse.start_orchestrator(
            input_stream=mock_sensory_stream, 
            filter_unit=thalamus
        )
    except KeyboardInterrupt:
        print("\nStopping aNA gracefully... Au revoir, Chef d'orchestre.")
    except Exception as e:
        print(f"\n[CRITICAL ERROR] L'orchestre a fait une fausse note : {e}")

if __name__ == "__main__":
    asyncio.run(main())
