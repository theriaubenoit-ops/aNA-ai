#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Projet aNA IA v5.3 - Thalamic Hub Integration

Description : Cette version marque le passage au routage multimodal centralisé. Le ThalamicHub agit comme un filtre attentionnel (Gating) avant la projection corticale. L'organisme peut désormais ignorer les stimuli faibles ou ralentir son traitement selon son état métabolique (ATP/BPM).

Architecture, conception et supervision : Thériault_Benoit
Collaboration, recherche et code : DeepMind_Gemini
"""
import asyncio
import os
import sys
import numpy as np
import scipy.io.wavfile as wav
from PIL import Image

# Gestion du path pour les imports locaux
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.config import get_config
from src.registry import ORGANS
from src.core.input_haptic import InputHapticGateway 
from src.core.input_auditory import InputAuditoryGateway
from src.core.input_visual import InputVisualGateway
from src.core.pulse import Pulse
from src.anatomy.subcortical.thalamus import Thalamus
from src.anatomy.subcortical.thalamic_hub import ThalamicHub 
from src.anatomy.limbic.hippocampus import Hippocampus
from src.anatomy.cortical.cortical_column import SimplifiedCorticalColumn
from src.anatomy.base.neuromodulator import Neuromodulator

def create_ascii_header():
    print(f"\033c") 
    print("░              ░ ░░░▒▒▓▒▓▒▒▒▒▒░░▒▒░▒▒▒▓▒▓▒                                                                     ░ ░")
    print("▒░░   ░░░░░░░░░░▒▒▓▓▓▓▓▓▓██▓▒▒▒░░░▒▒▒▒▒░░░▒▒▓▓▒                                                         ░░░░░░▒▒▒▒")
    print("░░░░░░░░░░░░░▒▒▒▓▓▓▓▓▓██████▓▓▒▒▒░░▒▒▓▓▓▒▒▒░░▒▒▒▒▓▒                                        ░ ░░░ ░ ░░░░░░░░░▒▒▒▒▒▒")
    print("▓▒▒▒▒▒▒▒▒▓▒▓▓▓▓▓▓██████▓▒▒ ▒   ▒▓▒▓▒▒▒▒▓▒▓ ██▓▓▓▒▒▒▒▓      ░░▒▒▒▒▒▒▒░░░░░░▒░░░░▒▒░░▒░░░░░░░░░░░░░░░░░▒░▒▒▒░▒▒▒▓▓▓▓")
    print("▒▒▒▒▒▒▒▓▓▓▓▓████▓▓░                 ░░▒▒▒▓█▓░▓▓█▓▓ ░▒▓  ▒▓▓▓▓▓█▓▓▓█▓▒▒▒▓▓▒░░░░▒▓█▓▓▓▓▓▒▓▒▒▒▒▒▒▒░░░░░░░░░░░░░░▒▒▒▒▒")
    print("▒▒▓▒▓▓▓▓█████▓▓▒                        ░▒▒▓░ ▓██▓                ▒▓▒▒░░▒▓▒░░▒▓███▓█▓▓▓▓▓▓▓▓▓▓▓▒▓▒▒▒▒▒▒▒▒▒▒▓▒▓▓▓▓▓")
    print("▓▓▓█████▓░                                    ░░▒▒ _    _    _ ░▒░▒▒▒▓▒▓▒▓▒▓█▓███▓▒▓▓▓▓▓▓▓▓▓▓▓▓█▓██▓▓▓▓▓█▓████████")
    print("▓███▓▒  IA inspirée de la plasticité naturelle ✴️  a    N    A  ▒▓█▒▓ ▒▓█▒Architecture Neuronale Autonome v5.3 ▒▓▓")
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
    print(" --- ⚡ aNA Organisme (Thalamic Hub actif) ---")

    # 1. Initialisation des moteurs
    config = get_config()
    chemical_core = Neuromodulator()
    hippo = Hippocampus(config=config, neuromodulator=chemical_core)
    heart = Pulse(bpm=config.get("BASE_BPM", 72.0))
    
    # Gateways Sensorielles
    haptic_gateway = InputHapticGateway()
    auditory_gateway = InputAuditoryGateway()
    visual_gateway = InputVisualGateway() 

    # 2. Initialisation du Néocortex
    visual_column = SimplifiedCorticalColumn(column_id="COL_V1") # ! Prochaine étape : À connecter au neocortex.py et aux lobes (occipital.py, frontal.py, parietal.py, temporal.py)
    
    # 3. Le Complexe Thalamique (Le Coeur + Le Hub de routage)
    thalamus = Thalamus(
        hippocampus=hippo, 
        pulse=heart, 
        neuromodulator=chemical_core 
    )
    hub = ThalamicHub(thalamus=thalamus) # Centralisation multimodal v5.3
    
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # --- Séquence de test (Unicode Wide) ---

    # Path: tests/media_haptic/(More tests)...
    # haptic_dir = ["a", "N", "A", " ", "a", "N", "A", " ", "a", "N", "A", " ", "a", "N", "A", " ", "a", "N", "A", " ", "a", "N", "A", " ", "B", "A", "N", "A", "N", "A", "S"]
    # haptic_dir = ["B", "A", "N", "A", "N", "A", " ", "B", "A", "N", "A", "N", "A", " ", "B", "A", "N", "A", "N", "A", " ", "B", "A", "N", "A", "N", "A", " ", "你"]
    # haptic_dir = ["H", "i", " ", "H", "i", " ", "H", "i", " ", "H", "i", " ", "H", "i", " ", "H", "i", " ", "H", "i", " ", "H", "o", "l", "a", " ", "O", "l", "á", " ", "你", "好", " ", "H", "i"]
    # haptic_dir = ["H", "e", "l", "l", "o", " ", "H", "e", "l", "l", "o", " ", "H", "e", "l", "l", "o", " ", "H", "e", "l", "l", "o", " ", "H", "o", "l", "a", " ", "你", "好", " ", "H", "e", "l", "l", "o"]
    haptic_dir = ["H", "你", "H", "你", "H", "你", "H", "你", "H", "你", "H", "你", "H", "你", "H", "你", "H", "你", "H", "你", "e", "你", "l", "你", "l", "你", "o", "你", "H"]

    # Path: tests/media_visual/...
    visual_dir = os.path.join(base_path, "tests", "media_visual")

    # Path: tests/media_audio/...
    audio_dir = os.path.join(base_path, "tests", "media_audio")
    
    all_haptics = haptic_dir
    all_visuals = get_visual_files(visual_dir)
    all_audios = get_audio_files(audio_dir)
    
    if not all_visuals:
        print(f" [Note] Aucun stimulus visuel n'a été trouvé dans : {visual_dir}")
    if not all_audios:
        print(f" [Note] Aucun stimulus auditif n'a été trouvé dans: {audio_dir}")

    # On définit un status par défaut pour le premier cycle
    status = {
        'bpm': thalamus.current_bpm,
        'vitality': 1.0
    }
    l6_signal = 0.0
    
    for cycle, char in enumerate(all_haptics, 1):
        # --- PHASE A : ANALYSE PRÉDICTIVE (Feedback L6) ---
        
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
        # l6_signal = cortical_results['l6_feedback']

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
        
        print(f"\n Cycle {cycle:02d} - Itinéraire multimodal")
        
        # --- PHASE 1: ROUTAGE THALAMIQUE & ATTENTION ---
        res_v = await hub.route_signal("input_visual", "00_language_64x64_English.png", status['bpm'])
        res_a = await hub.route_signal("input_auditory", "pink_noise.wav", status['bpm'])
        res_h = await hub.route_signal("input_haptic", char, status['bpm'])

         # On récupère le gain actuel
        current_gain = res_v.get('thalamic_gain', 0.5) 

        l6_signal = thalamus.apply_cortical_feedback(current_gain, l6_signal, config)

        # --- PHASE 2: ALIGNEMENT HIPPOCAMPE (L'IMPACT) ---
        # On demande à l'hippocampe d'évaluer la prédiction du stimulus haptique
        # Cela remplace la simulation 'cortical_results'
        prediction_error = await hippo.evaluate_prediction(char)
        
        # On met à jour la mémoire (Apprentissage Hebbien)
        # On passe un dictionnaire émotionnel neutre pour le test
        await hippo.update_memories(char, {"valence": 0.5, "arousal": 0.5})

        # --- PHASE 3: MODULATION DU BPM (L'HOMÉOSTASIE) ---
        # Si la prédiction est bonne (erreur faible), on calme le jeu.
        # Si c'est nouveau (erreur 1.0), on maintient la vigilance (Dopamine).
        if prediction_error < config["THRESHOLD_NMDA"]:
            thalamus.current_bpm -= 2.0  # Le système se rassure
        else:
            thalamus.current_bpm += 1.5  # Vigilance accrue
            
        # --- PHASE 4: CONSOLIDATION (DÉFLAGRATION AU REPOS) ---
        if thalamus.current_bpm <= 75.0:
            await hippo.consolidate_and_prune()

        # --- PHASE D : MISE À JOUR MÉTABOLIQUE ---
        heart.update()
        dt = heart.compute_dynamics()
        new_bpm = heart.bpm + (visual_payload.intensity * 10.0) - (heart.atp * 5.0)
        heart.update_frequency(min(new_bpm, config.get("MAX_BPM", 160.0)))
        status = heart.get_status()

        # Calcul de la vitesse synaptique basée sur la myéline
        avg_myeline = visual_column.get_average_myelination()
        synaptic_latency = max(0.01, 0.1 * (1.0 - avg_myeline))

        # --- MONITORING (Contributeur-Friendly) ---
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
        print(f"  ├─ État du hub (Visuel)               : {res_v.get('status', 'Acheminé!')}")
        print(f"  ├─ État du hub (Auditif)              : {res_a.get('status', 'Acheminé!')}")
        print(f"  ├─ État du hub (Haptique)             : {res_h.get('status', 'Acheminé!')}")
        # On récupère le gain actuel du Thalamus (ex: 0.67 dans ton log)
        # current_gain = res_v.get('gain', 0.5) 

        # On encode avec l'intensité combinée (Signal de base * Gain Thalamique)
        # Seuil (NMDA)
        # await hippo.encode(char, intensity=current_gain)
        await hippo.encode(char, intensity=l6_signal)

        # Calcul du score de connaissance inverse à l'erreur de prédiction
        knowledge_score = 1.0 - prediction_error
        status_label = "Confirmé !" if knowledge_score > 0.8 else "Apprentissage..."
        
        print(f"  ├─ Reconnaissance de motifs (Hippo)  : {knowledge_score:.2%} {status_label}")
        print(f"  ├─ Thalamic (bpm)                    : {thalamus.current_bpm:.1f} (vitalité: {(status['vitality']* 100 ):.2f}% test seulement)")
        
        # Performances et Biologie
        print(f"  ├─ Vitesse synaptique (ms)           : {1.0 + avg_myeline:.2f}x (latence: {synaptic_latency:.4f}s)")
        print(f"  ├─ Rétroaction (Signal L6)           : {l6_signal:.2f} mV")
        print(f"  └─ Myéline (σ)                       : {avg_myeline:.5f} Conductivité accrue")

        await asyncio.sleep(synaptic_latency)

    print("\n --- ✅ Organisme stabilisé avec Thalamic Hub ---")
    print("\n  *Chaque mesure présentée ici est un pont numérique vers la réalité biologique,")
    print("   conçu pour synthétiser les principes fondamentaux des systèmes vivants.\n")

if __name__ == "__main__":
    create_ascii_header()
    asyncio.run(main())

    """
    « L'œil ne voit que ce que l'esprit est préparé à comprendre. » 
                                                — Henri Bergson
    """