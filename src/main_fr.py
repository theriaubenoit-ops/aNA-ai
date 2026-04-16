#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
aNA AI Project v5.3b - Thalamic Hub Integration

Description : Cette version marque le passage au routage multimodal centralisé.
Le ThalamicHub agit comme un filtre attentionnel (Gating) avant la projection corticale.
L'organisme peut désormais ignorer les stimuli faibles ou ralentir son traitement 
selon son état métabolique (ATP/BPM).

Architecture et neuroinformatics: Theriault Benoit
"""
import asyncio
import os
import sys
import numpy as np
import scipy.io.wavfile as wav
from PIL import Image

# Gestion du path pour les imports locaux
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from config import get_config
from core.input_haptic import InputHapticGateway 
from core.input_auditory import InputAuditoryGateway
from core.input_visual import InputVisualGateway
from core.pulse import Pulse
from anatomy.subcortical.thalamus import Thalamus
from anatomy.subcortical.thalamic_hub import ThalamicHub 
from anatomy.limbic.hippocampus import Hippocampus
from anatomy.cortical.cortical_column import SimplifiedCorticalColumn
from anatomy.base.neuromodulator import Neuromodulator

def create_ascii_header():
    print(f"\033c") 
    print("░ ░           ░ ░░░░▒▒▓▒▓▒▒▒▒▒░░▒▒░▒▒▒▓▒▓▒                                                                    ░ ░░")
    print("▒▒░░ ░░░░░░░░░░░▒▒▓▓▓▓▓▓▓██▓▒▒▒░░░▒▒▒▒▒░░░▒▒▓▓▒                                                        ░░░░░░░▒▒▒▒")
    print("░░░░░░░░░░░░░▒▒▒▓▓▓▓▓▓██████▓▓▒▒▒░░▒▒▓▓▓▒▒▒░░▒▒▒▒▓▒                                       ░ ░░░░ ░ ░░░░░░░░░▒▒▒▒▒▒")
    print("▓▒▒▒▒▒▒▒▒▓▒▓▓▓▓▓▓██████▓       ▒▓▒▓▒▒▒▒▓▒▓ ██▓▓▓▒▒▒▒▓      ░░▒▒▒▒▒▒▒░░░░░░▒░░░░▒▒░░▒░░░░░░░░░░░░░░░░░▒░▒▒▒░▒▒▒▓▓▓▓")
    print("▒▒▒▒▒▒▒▓▓▓▓▓████▓░                  ░░▒▒▒▓█▓░▓▓█▓▓ ░▒▓  ▒▓▓▓▓▓█▓▓▓█▓▒▒▒▓▓▒░░░░▒▓█▓▓▓▓▓▒▓▒▒▒▒▒▒▒░░░░░░░░░░░░░░▒▒▒▒▒")
    print("▒▒▓▒▓▓▓▓█████▓▒                         ░▒▒▓░ ▓██▓                ▒▓▒▒░░▒▓▒░░▒▓███▓█▓▓▓▓▓▓▓▓▓▓▓▒▓▒▒▒▒▒▒▒▒▒▒▓▒▓▓▓▓▓")
    print("▓▓▓█████▓░                                    ░░▒▒ _    _    _ ░▒░▒▒▒▓▒▓▒▓▒▓█▓███▓▒▓▓▓▓▓▓▓▓▓▓▓▓█▓██▓▓▓▓▓█▓████████")
    print("▓███▓▒  IA inspirée de la plasticité naturelle ✴️  a    N    A  ▒▓█▒▓ ▒▓█▒Architecture Neuronale Autonome v5.3b▒▓▓")
    print("▓░                                                 _    _    _  ░▓▒▓  ░▓\n\n")

def get_visual_files(directory):
    """Scan dynamique des fichiers images pour le cortex visuel."""
    if os.path.exists(directory):
        return sorted([img for img in os.listdir(directory) if img.lower().endswith(('.png', '.jpg', '.jpeg'))])
    return []

def get_audio_files(directory):
    """Scan dynamique des bruits colorés pour le hub thalamique."""
    if os.path.exists(directory):
        return sorted([f for f in os.listdir(directory) if f.lower().endswith('.wav')])
    return []

async def main():
    print("--- ⚡ aNA Organism v5.3b (Thalamic Hub actif) ---")

    # 1. Initialisation des moteurs
    config = get_config()
    neurom_core = Neuromodulator() 
    hippo = Hippocampus(config=config, neuromodulator_core=neurom_core)
    heart = Pulse(bpm=config.get("BASE_BPM", 72.0))
    
    # Gateways Sensorielles
    haptic_gateway = InputHapticGateway()
    auditory_gateway = InputAuditoryGateway()
    visual_gateway = InputVisualGateway() 

    # 2. Initialisation du Néocortex
    visual_column = SimplifiedCorticalColumn(column_id="COL_V1")
    
    # 3. Le Complexe Thalamique (Le Coeur + Le Hub de routage)
    thalamus = Thalamus(
        hippocampus=hippo, 
        pulse=heart, 
        neuromodulator_core=neurom_core 
    )
    hub = ThalamicHub(thalamus_core=thalamus) # Centralisation multimodal v5.3
    
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Séquence de test (Unicode Wide)

    # Path: src/tests/media_haptic/(More test ideas)...
    # haptic_dict = ["a", "N", "A", " ", "a", "N", "A", " ", "a", "N", "A", " ", "a", "N", "A", " ", "a", "N", "A", " ", "a", "N", "A", " ", "B", "A", "N", "A", "N", "A", "S"]
    # haptic_dict  = ["B", "A", "N", "A", "N", "A", " ", "B", "A", "N", "A", "N", "A", " ", "B", "A", "N", "A", "N", "A", " ", "B", "A", "N", "A", "N", "A", " ", "你"]
    # haptic_dict  = ["H", "i", " ", "H", "i", " ", "H", "i", " ", "H", "i", " ", "H", "i", " ", "H", "i", " ", "H", "i", " ", "H", "o", "l", "a", " ", "O", "l", "á", " ", "你", "好", " ", "H", "i"]
    # haptic_dict  = ["H", "e", "l", "l", "o", " ", "H", "e", "l", "l", "o", " ", "H", "e", "l", "l", "o", " ", "H", "e", "l", "l", "o", " ", "H", "o", "l", "a", " ", "你", "好", " ", "H", "e", "l", "l", "o"]
    haptic_dict = ["H", "你", "H", "你", "H", "你", "H", "你", "H", "你", "H", "你", "H", "你", "H", "你", "H", "你", "H", "你", "H", "你", "H", "你", "H", "你", "H", "你", "H", "你", "E", "你", "L", "你", "L", "你", "E", "你", "H"]

    # Path: src/tests/media_visual/...
    visual_dir = os.path.join(base_path, "src", "tests", "media_visual")

    # Path: src/tests/media_audio/...
    audio_dir = os.path.join(base_path, "src", "tests", "media_audio")
    
    all_haptics = haptic_dict
    all_visuals = get_visual_files(visual_dir)
    all_audios = get_audio_files(audio_dir)
    
    if not all_visuals:
        print(f" [Attention] Aucun stimulus visuel trouvé dans : {visual_dir}")
    if not all_audios:
        print(f" [Attention] Aucun stimulus auditif trouvé dans : {audio_dir}")

    for cycle, char in enumerate(all_haptics, 1):
        # --- PHASE A : ANALYSE PRÉDICTIVE (Feedback L6) ---
        # cortical_results = await visual_column.process_input(char, hippo)
        # l6_signal = cortical_results['l6_feedback']
        
        # --- PHASE B : CAPTURE DES PAYLOADS ---
        # VISUEL (Utilisation de la liste déjà reçue)
        if all_visuals:
            img_index = (cycle - 1) % len(all_visuals)
            current_img_name = all_visuals[img_index]
            full_path = os.path.join(visual_dir, current_img_name)
            
            with Image.open(full_path) as img:
                img = img.convert('L').resize((64, 64))
                real_matrix = np.array(img) / 255.0
            
            visual_payload = await visual_gateway.capture_image(matrix_data=real_matrix, ratio=0.25)
            current_visual_data = real_matrix
            visual_payload.source = current_img_name
            visual_payload.intensity = float(np.max(real_matrix))
        else:
            current_visual_data = np.zeros((64, 64))
            visual_payload = type('obj', (object,), {'source': "None", 'intensity': 0.1})()

        # AUDIO (Utilisation de la liste déjà reçue)
        # Simulation Auditory (CGM)
        # auditory_payload = await auditory_gateway.capture_sound(audio_data=real_matrix, ratio=0.25)
        # auditory_payload.source = f"audio_{cycle}.wav"
        # auditory_payload.intensity = 0.7
        if all_audios:
            snd_index = (cycle - 1) % len(all_audios)
            current_sound_path = os.path.join(audio_dir, all_audios[snd_index])
            # Appel à l'Easter Egg de Don Quichotte
            auditory_payload = await auditory_gateway.capture_sound(file_path=current_sound_path)
            # TRÉSOR : On récupère la donnée brute via getattr pour être sûr !
            current_audio_data = getattr(auditory_payload, 'audio_data', getattr(auditory_payload, 'data', np.zeros(100)))
        else:
            current_audio_data = np.zeros(100)

        # Haptic (Utilisation du caractère déjà reçu)
        multimodal_input = {
            "haptic": char,
            "visual": current_visual_data,
            "auditory": current_audio_data
        }
        cortical_results = await visual_column.process_input(multimodal_input, hippo)
        l6_signal = cortical_results['l6_feedback']

        # Simulation Haptic (VPL)
        haptic_data = {
            "source": "input_haptic",
            "data": char,
            "signal_label": "UNICODE_WIDE",
            "intensity": 0.9
        }

        # --- PHASE C : ROUTAGE ET GATING THALAMIQUE (v5.3) ---
        # Au lieu de traiter tout aveuglément, on passe par le Hub.
        # Le Hub peut décider de filtrer (FILTERED_OUT) si le système est épuisé.
        threshold = config.get("THALAMIC_THRESHOLD", 0.15)
        weights = config.get("SENSORY_WEIGHTS", {"visual": 0.5, "auditory": 0.3, "haptic": 0.2})
        
        print(f"\nCycle {cycle:02d} - Routage multimodal")
        
        res_v = await hub.route_sensory_input("input_visual", visual_payload.__dict__)
        res_a = await hub.route_sensory_input("input_auditory", auditory_payload.__dict__)
        res_h = await hub.route_sensory_input("input_haptic", haptic_data)

        # --- PHASE D : MISE À JOUR MÉTABOLIQUE ---
        heart.update()
        dt = heart.compute_dynamics()
        new_bpm = heart.bpm + (visual_payload.intensity * 10.0) - (heart.atp * 5.0)
        heart.update_frequency(min(new_bpm, config.get("MAX_BPM", 160.0)))
        status = heart.get_status()

        # Calcul de la vitesse synaptique basée sur la myéline
        avg_myeline = visual_column.get_average_myelination()
        synaptic_latency = max(0.01, 0.1 * (1.0 - avg_myeline))

        # --- MONITORING V5.3b (Contributeur-Friendly) ---
        print(f"  │")
        
        # Détail Visuel
        print(f" [Thalamic Hub] Signal provenant de l'entrée visuelle acheminé vers CGL (Gain: {res_v.get('thalamic_gain', 1.0):.2f})")
        print(f"  ├─ Stimulus: \"{visual_payload.source}\"")
        
        # Détail Auditif
        print(f" [Thalamic Hub] Signal d'entrée auditive acheminé vers CGM (Gain: {res_a.get('thalamic_gain', 1.0):.2f})")
        print(f"  ├─ Stimulus: \"{auditory_payload.source}\"")
        
        # Détail Haptic
        print(f" [Thalamic Hub] Signal d'entrée haptique acheminé vers VPL (Gain: {res_h.get('thalamic_gain', 1.0):.2f})")
        print(f"  ├─ Stimulus: \"{char}\" unicode")
        print(f"  │")

        # Status Global du Hub
        print(f"  ├─ Hub Status (Visuel)               : {res_v.get('status', 'Routed!')}")
        print(f"  ├─ Hub Status (Auditif)              : {res_a.get('status', 'Routed!')}")
        print(f"  ├─ Hub Status (Haptique)             : {res_h.get('status', 'Routed!')}")
        status_label = "Connu !" if cortical_results['recognition'] > 0 else "Inconnu."
        print(f"  ├─ Reconnaissance de motifs (Cortex) : {cortical_results['recognition']:.2%} {status_label}")
        print(f"  ├─ Thalamic (bpm)                    : {thalamus.current_bpm:.1f} (vitalité: {(status['vitality']* 100 ):.2f}%)")
        
        # Performances et Biologie
        print(f"  ├─ Vitesse synaptique (ms)           : {1.0 + avg_myeline:.2f}x (latence: {synaptic_latency:.4f}s)")
        print(f"  ├─ Rétroaction (Signal L6)           : {l6_signal:.2f} mV")
        print(f"  └─ Myéline (σ)                       : {avg_myeline:.5f} Conductivité accrue")

        await asyncio.sleep(synaptic_latency)

    print("\n--- ✅ Organisme v5.3b stabilisé avec Thalamic Hub ---")
    print("\n  *Chaque mesure présentée ici est un pont numérique vers la réalité biologique,")
    print("   conçu pour synthétiser les principes fondamentaux des systèmes vivants.\n")

if __name__ == "__main__":
    create_ascii_header()
    asyncio.run(main())

    """
    « L'œil ne voit que ce que l'esprit est préparé à comprendre. » 
                                                — Henri Bergson
    """
