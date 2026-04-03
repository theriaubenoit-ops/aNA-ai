#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import os
import sys
import numpy as np

# Gestion du path pour les imports locaux
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from config import get_config  # Ajoute l'import en haut du fichier
from core.pulse import Pulse
from core.input_gateway import InputGateway
from anatomy.subcortical.thalamus import Thalamus
from anatomy.limbic.hippocampus import Hippocampus
from anatomy.cortical.cortical_column import SimplifiedCorticalColumn
from anatomy.base.neuron import Neuron, NeuronConfig
from anatomy.base.neuromodulator import Neuromodulator
from registry import ORGANS 

async def main():
    print("--- ⚡ Organisme aNA v5.1 (Réunion des Organes) ---")
    
    config = get_config()
    neurom_core = Neuromodulator() 
    hippo = Hippocampus(config=config, neuromodulator_core=neurom_core)
    heart = Pulse()
    gateway = InputGateway()
    
    # 2. Initialisation du Néocortex (Colonne de traitement)
    # Chaque colonne représente une unité de calcul 6-layers
    visual_column = SimplifiedCorticalColumn(column_id="COL_V1")
    
    # 3. Le Thalamus (Pilote du flux et de la dopamine)
    thalamus = Thalamus(
        hippocampus=hippo, 
        pulse=heart, 
        neuromodulator_core=neurom_core 
    )
    
    # Séquence de test pour valider l'habituation et le feedback L6
    # test_sequence = ["a", "N", "A", " ", "a", "N", "A", " ", "a", "N", "A", " ", "a", "N", "A", " ", "a", "N", "A", " ", "B", "A", "N", "A", "N", "A", "S"]
    test_sequence = ["B", "A", "N", "A", "N", "A", " ", "B", "A", "N", "A", "N", "A", " ", "B", "A", "N", "A", "N", "A", " ", "B", "A", "N", "A", "N", "A", "😜"]
    # test_sequence = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "a"]

    for cycle, char in enumerate(test_sequence, 1):
        # --- PHASE A : TRANSDUCTION ---
        payload = gateway.process_symbol(char)
        
        # --- PHASE B & C : CASCADE CORTICALE (L4 -> L2/3 -> L6) ---
        # On interroge d'abord le cortex pour obtenir le feedback L6
        cortical_results = await visual_column.process_input(char, hippo)
        l6_signal = cortical_results['l6_feedback']

        # --- PHASE D : TRAITEMENT THALAMIQUE (Régulation du BPM) ---
        # aNA utilise maintenant le feedback L6 pour calculer le rythme
        log_thalamus = await thalamus.process_payload(payload, l6_feedback=l6_signal)
        
        # Mise à jour du monitoring
        # thalamus.apply_l6_feedback(l6_signal)
        
        # --- PHASE E : MISE À JOUR MÉTABOLIQUE ---
        heart.update()
        status = heart.get_status()

        # --- PHASE F : MYÉLINISATION DYNAMIQUE (Nouveau !) ---
        # En fonction de la reconnaissance, on ajuste la myéline pour accélérer les futurs
        avg_myeline = visual_column.get_average_myelination()
        
        # --- MONITORING ---
        print(f"\nCycle {cycle:02d} | Entrée: '{char}'")
        print(f" └─ Thalamus  : {log_thalamus}")
        print(f" └─ Cortex    : Reconnaissance {cortical_results['recognition']:.2%}")
        print(f" └─ Retour    : L6 Signal {cortical_results['l6_feedback']:.2f}")
        print(f" └─ Myéline   : {avg_myeline:.5f} (Conductivité accrue)") # Nouveau !
        print(f" └─ Impulsion : {status['bpm']:.1f} BPM | Vitalité: {status['energy']:.2%}")        
        await asyncio.sleep(0.1)

    print("\n--- ✅ Organisme stabilisé et fonctionnel ---")

if __name__ == "__main__":
    asyncio.run(main())