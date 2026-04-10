#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Projet aNA - v5.2

Module : Intégration principale

Description : Ce processus central orchestre la boucle bio-numérique complète. Il synchronise le flux thalamique, les cascades corticales L4→L2/3→L6 et la myélinisation dynamique. L’objectif est de simuler un métabolisme stabilisé où la reconnaissance module le pouls (BPM) et la résistance aux neurotransmetteurs en temps réel.
Fonctionnalités : Rétroaction thalamo-corticale, homéostasie, croissance de la myéline.

Architecture et neuroinformatique : Theriault Benoit
"""
import asyncio
import os
import sys
import numpy as np

# Gestion du path pour les imports locaux
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from config import get_config  # Ajoute l'import en haut du fichier
from core.input_visual import InputVisualGateway, VisualSensoryPayload
from core.pulse import Pulse
from core.input_tactille import InputGateway
from anatomy.subcortical.thalamus import Thalamus
from anatomy.limbic.hippocampus import Hippocampus
from anatomy.cortical.cortical_column import SimplifiedCorticalColumn
from anatomy.base.neuron import Neuron, NeuronConfig
from anatomy.base.neuromodulator import Neuromodulator
from registry import ORGANS 

def create_ascii_header():
    print(f"\033c") 
    print("░                     ░░░░░░░░░░▒▒▒▒▒▒░░")
    print("           ░░░░░░░░░▒▒▒▒▒▓▒▒▒▒░░░░░░░░░░▒▒▒▒░                                                          ░░░░░░░░░░░")
    print("░░░░░░░░░░░░░░░░▒▒▒▒▓▓▓▓▓▓▓▓▓▓▓▒░░░░░▒▒▒░░░░▒▓▒░░                      ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░")
    print("░░░░░░░░░░░░░░▒▒▒▓▓▓▓▓▓▓▓▓▓▓▒░░▒▒▒░░░░▒▓▓▓▓▓▓▒▒▒▒▒░     ░░░░░░░░░░░░░░░░░░░░░▒▒░░▒▒▒▓▓▓▓▓▓▒▒▒░░░░░░░░░░░░░░░░░▒▒▒▒")
    print("▒░░░░░▒▒▒▒▒▒▓▓▓▓▓▓▓▓▓▒░         ░░▒▒▒░▒▒▒▒▓▓▓▓▓▓▓▒▒░░  ░▒▒▒▓▒▒▒▓▒▓▒▓▒░░░░░░░▒▓▓▓▓▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░░░░░░░░░░░▒▓")
    print("░▒▒▒▒▓▓▓▓▓▓▓▓▓▓▓▓░                   ░░ ▒▒▓▒░▒▓▓▓░▒▒░░           ░▒░░░▒▓▒▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒▒▓▓")
    print("▒▒▓▓▓▓▓▓▒▒▒░░                           ░▓▓▒░░▒▓▓░ _    _    _ ░▒░░▒▓▒▓▓▓▓▓▓▓▓▓▓▒░░░░░░░░░▒▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓")
    print("▓▓▓░IA inspirée de la plasticité naturelle░░  ░░░  a    N    A  ▒▓▒▓▒▒▒▓░Architecture Neuronale Autonome v5.2b ░▒▓")
    print("░                                                  ‾    ‾    ‾ ░▓▒▓░░▒▓░\n\n")

async def main():
    print("--- ⚡ Organisme aNA v5.2 (Réunion des Organes) ---")
    
    # 1. Initialisation des moteurs v5.2
    config = get_config()
    neurom_core = Neuromodulator() 
    hippo = Hippocampus(config=config, neuromodulator_core=neurom_core)
    heart = Pulse()
    gateway = InputGateway()
    # Nouvelle voie visuelle
    visual_gateway = InputVisualGateway() 

    # Simulation d'une image test (ex: 64x64)
    test_image = np.random.rand(64, 64)

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
    # test_sequence = ["B", "A", "N", "A", "N", "E", " ", "B", "A", "N", "A", "N", "E", " ", "B", "A", "N", "A", "N", "E", " ", "B", "A", "N", "A", "N", "E", "Z"]
    # test_sequence = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "a"]
    test_sequence = ["H", "e", "l", "l", "o", " ", "你", "好", " ", "H", "o", "l", "a", " ", "A", "l", "l", "ô", " ", "П", "р", "и", "в", "е", "т", " ", "H", "e", "l", "l", "o", " ", "你", "好"]

    for cycle, char in enumerate(test_sequence, 1):
        # --- PHASE A : TRANSDUCTION ---
        payload = gateway.process_symbol(char)
        
        # --- PHASE B : CASCADE CORTICALE (L4 -> L2/3 -> L6) ---
        # On interroge d'abord le cortex pour obtenir le feedback L6
        cortical_results = await visual_column.process_input(char, hippo)
        l6_signal = cortical_results['l6_feedback']

        # --- PHASE C : PRÉPARATION DES SENS ---
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        test_dir = os.path.join(base_path, "docs", "assets", "occipital_input_test_64x64")

        # 1. Récupérer la liste de toutes les images valides
        all_images = sorted([img for img in os.listdir(test_dir) if img.lower().endswith(('.png', '.jpg', '.jpeg'))])

        # Initialisation par défaut (Sécurité)
        if all_images:
            # 2. Sélectionner l'image correspondant au cycle (modulo pour boucler si moins d'images que de lettres)
            current_img_name = all_images[(cycle - 1) % len(all_images)]
            full_path = os.path.join(test_dir, current_img_name)
            
            # 3. Capture réelle par la gateway
            raw_matrix = np.random.rand(64, 64) 
            visual_payload = await visual_gateway.capture_image(raw_matrix, ratio=0.25)
            visual_payload.source = current_img_name
        else:
            visual_payload = {"type": "visuel", "source": "aucun", "data": None}

        # 2. Le Tactile (on crée un petit dictionnaire ou objet compatible)
        tactile_payload = {
            "source": "TACTILE_GATEWAY",
            "data": char,
            "signal_label": "UNICODE_WIDE"
        }

        # --- PHASE D : INTÉGRATION THALAMIQUE (Le Pulse Partagé) ---
        # Le Thalamus reçoit les deux et influence le BPM
        log_v = await thalamus.process_payload(visual_payload, l6_feedback=l6_signal)
        log_t = await thalamus.process_payload(tactile_payload, l6_feedback=l6_signal)

        # --- PHASE E : MISE À JOUR MÉTABOLIQUE ---
        heart.update() # Le cœur bat maintenant selon la tension combinée

        # --- PHASE D : TRAITEMENT THALAMIQUE (Régulation du BPM) ---
        # aNA utilise maintenant le feedback L6 pour calculer le rythme
        log_thalamus = await thalamus.process_payload(payload, l6_feedback=l6_signal)
        
        # Mise à jour du monitoring

        # --- PHASE E : MISE À JOUR MÉTABOLIQUE ---
        heart.update()
        status = heart.get_status()

        # --- PHASE F : MYÉLINISATION DYNAMIQUE (Nouveau !) ---
        # En fonction de la reconnaissance, on ajuste la myéline pour accélérer les futurs
        avg_myeline = visual_column.get_average_myelination()
        
        # --- MONITORING ---

        # --- TEST DE PERCEPTION VISUELLE ---
        print(f"\n[V1] Tentative de perception visuelle (stimulus): {visual_payload.source})...")
        print(f" └─ Thalamus visuel : {log_v}")

        # --- TEST DE PERCEPTION TACTILE ---
        print(f"\nCycle {cycle:02d} | Entrée: '{char}' (Unicode étendu)")
        print(f" └─ Thalamus  : {log_t}")
        print(f" └─ Cortex    : Reconnaissance {cortical_results['recognition']:.2%}")
        print(f" └─ Retour    : L6 Signal {cortical_results['l6_feedback']:.2f}")
        print(f" └─ Myéline   : {avg_myeline:.5f} (Conductivité accrue)") # Nouveau !
        print(f" └─ Impulsion : {status['bpm']:.1f} BPM | Vitalité: {status['energy']:.2%}")        
        await asyncio.sleep(0.1)

    print("\n--- ✅ Organisme stabilisé et fonctionnel ---")

if __name__ == "__main__":
    create_ascii_header()
    asyncio.run(main())
