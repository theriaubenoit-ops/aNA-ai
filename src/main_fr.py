#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Project aNA AI v5.2 - Intégration principale

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
from core.input_tactile import InputTactileGateway 
from core.input_auditory import InputAuditoryGateway
from core.input_visual import InputVisualGateway, VisualSensoryPayload
from core.pulse import Pulse
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
    tactile_gateway = InputTactileGateway()
    auditory_gateway = InputAuditoryGateway()
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
        payload = tactile_gateway.process_symbol(char)
        
        # --- PHASE B : CASCADE CORTICALE (L4 -> L2/3 -> L6) ---
        # On interroge d'abord le cortex pour obtenir le feedback L6
        cortical_results = await visual_column.process_input(char, hippo)
        l6_signal = cortical_results['l6_feedback']

        # --- PHASE C : PRÉPARATION DES SENS ---
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        test_dir = os.path.join(base_path, "docs", "assets", "occipital_input_test_64x64")

        # 1. Récupérer la liste de toutes les images valides
        # all_images = ["../docs/assets/occipital_input_test_64x64/occipital_input_test_64x64_01_English.png"] # test 1 seule image
        all_images = sorted([img for img in os.listdir(test_dir) if img.lower().endswith(('.png', '.jpg', '.jpeg'))])

        # Initialisation par défaut (Sécurité)
        if all_images:
            # 2. Sélectionner l'image correspondant au cycle (modulo pour boucler si moins d'images que de lettres)
            current_img_name = all_images[(cycle - 1) % len(all_images)]
            full_path = os.path.join(test_dir, current_img_name)
            
            # 3. Capture réelle par la gateway
            raw_matrix = np.random.rand(64, 64) 
            visual_payload = await visual_gateway.capture_image(matrix_data=raw_matrix, ratio=0.25)
            visual_payload.source = current_img_name
        else:
            visual_payload = {"type": "visual", "source": "None", "data": None}

        # Auditory
        current_sound_name = f"stimulus_audio_{cycle:02d}.wav"
        auditory_payload = await auditory_gateway.capture_sound(audio_data=raw_matrix, ratio=0.25)
        auditory_payload.source = current_sound_name

        # 2. Le Tactile (on crée un petit dictionnaire ou objet compatible)
        tactile_payload = {
            "source": "TACTILE_GATEWAY",
            "data": char,
            "signal_label": "UNICODE_WIDE"
        }
        tactile_signal = tactile_gateway.process_symbol(char=char)

        # --- PHASE D : INTÉGRATION THALAMIQUE (Le Pulse Partagé) ---
        # aNA utilise maintenant le feedback L6 pour calculer le rythme
        # Le Thalamus reçoit les deux et influence le BPM
        if not hasattr(visual_payload, 'intensity'):
            visual_payload.intensity = 0.8  # Valeur par défaut si non calculée
        log_v = await thalamus.process_payload(visual_payload, l6_feedback=l6_signal)
        log_a = await thalamus.process_payload(auditory_payload, l6_feedback=l6_signal)
        log_t = await thalamus.process_payload(tactile_payload, l6_feedback=l6_signal)

        # --- PHASE E : MISE À JOUR MÉTABOLIQUE ---
        final_bpm = thalamus.current_bpm 
        heart.update_frequency(final_bpm) # On synchronise le Pulse réel
        # heart.update() # Le cœur bat maintenant selon la tension combinée
        
        # Mise à jour du monitoring

        # --- PHASE E : MISE À JOUR MÉTABOLIQUE ---
        heart.update()
        status = heart.get_status()

        # --- PHASE F : MYÉLINISATION DYNAMIQUE (Nouveau !) ---
        # En fonction de la reconnaissance, on ajuste la myéline pour accélérer les futurs
        avg_myeline = visual_column.get_average_myelination()
        
        # --- PHASE G : CALCUL DE LA LATENCE SYNAPTIQUE (Nouveau) ---
                # Plus l'organisme 'apprend' (myéline), plus l'influx circule vite.
        # On passe d'un repos de 0.1s à un minimum de 0.01s pour les zones expertes.
        base_delay = 0.1
        synaptic_latency = max(0.01, base_delay * (1.0 - avg_myeline))

        # --- MONITORING FINAL v5.2 ---
        print(f"\nCycle {cycle:02d}")

        # Visuel (CGL : Corps Genouillé Latéral)
        print(f"[V1] Perception visuelle (Stimulus: {visual_payload.source})...")
        print(f" └─ Thalamus (CGL)         : BPM {log_v['bpm']:.1f} | Gain {log_v.get('thalamic_gain', 0):.2f}")

        # Auditif (CGM : Corps Genouillé Médian)
        print(f"[A1] Perception auditive (Stimulus: {auditory_payload.source})...")
        print(f" └─ Thalamus (CGM)         : BPM {log_v['bpm']:.1f} | Gain {log_v.get('thalamic_gain', 0):.2f}")

        # Tactile (VPL : Noyau Ventral Postéro-Latéral)
        print(f"[T1] Entrée somatosensorielle (Stimulus: '{char}', Unicode étendu)...")
        print(f" └─ Thalamus (VPL)         : BPM {log_t['bpm']:.1f} | Gain {log_t['thalamic_gain']:.2f}")
        print(f" └─ Cortex                 : Correspondance de motif {cortical_results['recognition']:.2%}")
        print(f" └─ Rétroaction            : Signal L6 {cortical_results['l6_feedback']:.2f}")
        print(f" └─ Myéline                : {avg_myeline:.5f} (Conductivité accrue)")
        print(f" └─ Vitesse synaptique     : {1.0 + avg_myeline:.2f}x (Latence: {synaptic_latency:.4f}s)")
        print(f" └─ Homéostasie métabolique: {status['bpm']:.1f} BPM | Vitalité: {status['energy']:.2%}")

        await asyncio.sleep(synaptic_latency)

    print("\n--- ✅ Organisme stabilisé et fonctionnel ---")

if __name__ == "__main__":
    create_ascii_header()
    asyncio.run(main())
