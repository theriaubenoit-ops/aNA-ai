#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hippocampus (Dynamic Buffer & Indexing System), implementation for aNA AI Project v5.3

Communicates with:
Input: (<- Cortex)
Input: (<- Amygdala: Emotional urgency & Saliency)
Output: (-> Thalamus: BPM & Metabolic modulation) 
Output: (-> Cortical Storage)

Description: This module implements the Hippocampus with its subfields (DG, CA1-CA4) for memory encoding, consolidation, and retrieval. It includes mechanisms for synaptic plasticity (LTP/LTD), emotional modulation of memory strength, and a novel "CA4" subfield for long-term trace stabilization.

Architecture, concept and supervision: Theriault_Benoit
Collaboration, research and code: DeepMind_Gemini, Cline
"""

from typing import Any, Dict
import sys
import os
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.config import get_config
from src.registry import ORGANS
from src.anatomy.base.neuromodulator import Neuromodulator

class Hippocampus:
    def __init__(self, config: get_config = None, neuromodulator: Neuromodulator = None):
        # config = get_config()
        # 1. Le Génome (Structure fixe du registre)
        self.structure = ORGANS["HIPPOCAMPUS"]
        # Si config est None, on peut mettre des valeurs par défaut
        self.config = config if config else {} # !!! Attention : config peut être None, on doit gérer ce cas pour éviter les erreurs de type.
        self.neurom = neuromodulator # neurom_core avant
        
        # Initialisation des sous-champs
        self.subfields = {field: {} for field in self.structure["SUBFIELDS"]}
        
        # On peut ensuite fusionner avec la config si nécessaire
        if "SUBFIELDS" in self.config:
            for sf in self.config["SUBFIELDS"]:
                if sf not in self.subfields:
                    self.subfields[sf] = {}

        self.last_signal = None
        self.sequence_map = {}  # Pour prédire : 'H' -> 'e'
        self.short_term_memory = {}
        # print("  [Hippocampus] v5.1 : Zones DG, CA1-CA4 initialized.")
        # print("  [Hippocampus] v5.2 : Hebbian sequences & Unicode Wide enabled.")

    def _get_hash(self, signal_data):
        """Utilitaire récursif pour rendre TOUT type de signal hachable (immulable)."""
        if isinstance(signal_data, dict):
            # Transforme le dict en tuple de tuples (clé, valeur_hachée)
            return tuple((k, self._get_hash(v)) for k, v in sorted(signal_data.items()))
        elif isinstance(signal_data, (list, np.ndarray)):
            # Transforme récursivement chaque élément de la liste/array en tuple
            return tuple(self._get_hash(i) for i in (signal_data.tolist() if hasattr(signal_data, 'tolist') else signal_data))
        return signal_data

    async def evaluate_prediction(self, signal_data, label=None, sensory_type: str = "haptic"):
        """
        Simule la boucle trisynaptique avec dynamique AMPA/NMDA.
        Modulation du seuil d'entrée selon le poids sensoriel du Génome.
        """
        config = get_config()
        # 1. TRADUCTION : On rend le signal (même un dict) immuable et hachable
        current_signal = self._get_hash(signal_data)

        # --- LOGIQUE HEBBIENNE (Consolidation) ---
        if self.last_signal is not None:
            pair = (self.last_signal, current_signal)
            self.sequence_map[pair] = self.sequence_map.get(pair, 0) + 0.1
            
        self.last_signal = current_signal
        # CRUCIAL : On utilise la version hachée comme étiquette pour les dictionnaires DG/CA3
        signal_label = current_signal

        # 2. DG : Séparation de motifs
        is_known_dg = signal_label in self.subfields["DG"]

        # 3. CA3 : Accès à la trace
        trace_ca3 = self.subfields["CA3"].get(signal_label, config.get("MIN_LATENT_THRESHOLD", 0.001))

        # 4. MODULATION DU SEUIL NMDA (Haptique par défaut à 0.2)
        # On vérifie si c'est un dictionnaire (multimodal) pour ajuster le poids
        if isinstance(signal_data, dict):
            # Pour un signal multimodal, on peut faire une moyenne des poids ou prendre le max
            sensory_weight = 0.4 # Valeur "Intégration"
        else:
            sensory_weight = config["SENSORY_WEIGHTS"].get(sensory_type, 0.2)

        dynamic_nmda_threshold = config.get("THRESHOLD_NMDA", 0.4) * (1.0 - sensory_weight)

        # 5. CA1 : Comparateur et Plasticité
        if is_known_dg and trace_ca3 > dynamic_nmda_threshold:
            self.subfields["CA3"][signal_label] += config.get("LTP_GAIN", 0.05)
            prediction_error = 0.1 / self.subfields["CA3"][signal_label]
        else:
            prediction_error = 1.0
            self.subfields["DG"][signal_label] = True
            self.subfields["CA3"][signal_label] = config.get("INITIAL_ENGRAM_STRENGTH", 0.1)
            self.subfields["CA4"][signal_label] = 1.0

        # --- AJOUT DU PONT INVISIBLE VERS LE REGISTRE ---
        # On convertit l'erreur de prédiction (0.0 à 1.0) en score de match (0% à 100%)
        # Plus l'erreur est basse, plus le match est haut.
        pattern_score = (1.0 - prediction_error) * 100.0
        
        # On écrit dans le registre pour le Thalamus (Lien invisible mais fonctionnel)
        if hasattr(self, 'registry'):
             self.registry.set("last_hippo_match", pattern_score)
        # ------------------------------------------------

        return max(0.0, min(1.0, prediction_error))
    
    async def update_memories(self, signal_label: str, emotional_data: dict):
        """
        Gère la sédimentation mémorielle modulée par l'émotion.
        """
        impact = emotional_data.get("impact", 0.0)
        fear_level = emotional_data.get("fear_level", 0.0)
        
        # 1. INITIALISATION (NMDA Flash)
        if signal_label not in self.subfields["CA3"]:
            # Si peur intense (>0.7), on force l'encodage au maximum (1.0)
            if fear_level > 0.7:
                self.subfields["CA3"][signal_label] = 1.0
                # On grave un plancher permanent dans CA4 (la trace acide)
                self.subfields["CA4"][signal_label] = 0.2 
                print(f"  DEBUG: Trace '{signal_label}' engraved by TRAUMA (Flash NMDA).")
            else:
                self.subfields["CA3"][signal_label] = self.config.get("MIN_LATENT_THRESHOLD", 0.001)
                print(f"  DEBUG: Trace '{signal_label}' initialized NEUTRAL.")

        # 2. RENFORCEMENT (LTP)
        # On ajoute l'impact émotionnel à la force actuelle
        self.subfields["CA3"][signal_label] += (impact * self.config.get("LTP_GAIN", 0.1))
        
        # 3. ÉTANCHÉITÉ (On s'assure que le signal DG est présent)
        self.subfields["DG"][signal_label] = True

    async def apply_synaptic_decay(self, system_strain: float = 0.0):
        """
        Version 5.1 : Le CA4 devient dynamique. 
        En cas de fatigue (strain élevé), les traces négatives 'remontent' 
        pour servir d'avertissement prioritaire.
        """
        default_min = self.config.get("MIN_LATENT_THRESHOLD", 0.001)
        
        for label in list(self.subfields["CA3"].keys()):
            # 1. Érosion naturelle (LTD)
            self.subfields["CA3"][label] *= (1.0 - self.burn_rate)
            
            # 2. Récupération du plancher de survie CA4
            survival_floor = self.subfields["CA4"].get(label, default_min)
            
            # 3. INNOVATION : Effet de Fatigue (Strain)
            # Si le système est épuisé (ATP bas), on augmente artificiellement 
            # la visibilité des traces de survie.
            if system_strain > 0.6 and survival_floor > default_min:
                # La trace 'remonte' proportionnellement à la fatigue
                boost_avertissement = survival_floor * (system_strain * 0.5)
                self.subfields["CA3"][label] += boost_avertissement
                # On s'assure que ça ne dépasse pas un seuil de panique
                self.subfields["CA3"][label] = min(1.0, self.subfields["CA3"][label])
            
            # 4. Arbitrage final
            if self.subfields["CA3"][label] < survival_floor:
                self.subfields["CA3"][label] = survival_floor

    async def update_trace_with_emotion(self, signal_label: str, impact: float, valence: float, sensory_type: str = "visual"):
        """
        Ajuste la trace CA3 en fonction de l'impact fourni par l'Amygdale
        et de la priorité sensorielle définie dans le Génome (config).
        """
        config = get_config() # Récupération des SENSORY_WEIGHTS
        
        if signal_label not in self.subfields["CA3"]:
            self.subfields["CA3"][signal_label] = config.get("MIN_LATENT_THRESHOLD", 0.001)

        # 1. RÉCUPÉRATION DU POIDS SENSORIEL (Ex: Visual=0.5, Auditory=0.3)
        # On utilise le poids défini dans config.py pour moduler l'impact
        weight = config["SENSORY_WEIGHTS"].get(sensory_type, 0.1)
        
        # 2. MODULATION DE L'IMPACT (L'image marquera plus que le son)
        effective_impact = impact * weight

        # 3. LOGIQUE DE VALENCE (LTP forcée pour le danger)
        if valence < -0.5:
            # "Trace Acide" : On multiplie l'effet pour la survie
            # Le poids sensoriel détermine la profondeur de la gravure
            self.subfields["CA3"][signal_label] += (effective_impact * 2.0)
            
            # On grave aussi un plancher de survie dans CA4
            if signal_label not in self.subfields["CA4"]:
                self.subfields["CA4"][signal_label] = effective_impact * 0.5
        else:
            # Apprentissage calme / plaisir
            self.subfields["CA3"][signal_label] += (effective_impact * 0.5)

        # Plafonnement pour la stabilité numérique
        self.subfields["CA3"][signal_label] = min(5.0, self.subfields["CA3"][signal_label])

    async def consolidate_metabolism(self, atp_level: float):
        """
        Mécanique de 'Sommeil Paradoxal' :
        Nettoie le bruit et stabilise les souvenirs de survie (CA4).
        """
        print(f"  [Hippocampe] Active consolidation phase (ATP: {atp_level:.2f})")
        
        for label in list(self.subfields["CA3"].keys()):
            # 1. Élagage (Pruning) : Si la trace est trop faible, on l'efface
            # On libère de l'espace cognitif
            if self.subfields["CA3"][label] < 0.05:
                del self.subfields["CA3"][label]
                continue
                
            # 2. Refroidissement des Traces Acides :
            # Si c'est un souvenir de danger (présent dans CA4), on baisse son 
            # intensité dans CA3 pour que aNA ne soit plus en 'panique' au réveil.
            if label in self.subfields["CA4"]:
                # On rapproche la trace de son plancher de survie (Sagesse > Peur)
                target_floor = self.subfields["CA4"][label]
                self.subfields["CA3"][label] = (self.subfields["CA3"][label] + target_floor) / 2

    async def consolidate_and_prune(self):
        """
        Simule le sommeil paradoxal : 
        Nettoyage impitoyable de tout ce qui n'a pas été verrouillé par NMDA.
        """
        nmda_threshold = self.config.get("THRESHOLD_NMDA", 0.65)
        
        # On travaille sur une copie pour pouvoir supprimer pendant l'itération
        for label in list(self.subfields["CA3"].keys()):
            val = self.subfields["CA3"][label]
            
            # --- LOGIQUE DE PRUNING NMDA ---
            if val < nmda_threshold:
                # L'information n'était qu'électrique (AMPA), pas structurelle.
                # Elle s'efface avec le repos.
                del self.subfields["CA3"][label]
            else:
                # L'information a passé le verrou NMDA. 
                # On la stabilise (éventuellement légère décroissance LTD)
                self.subfields["CA3"][label] *= 0.95

    async def encode(self, label: str, intensity: float = 0.5, importance: float = 0.5, sensory_data: Any = None):
        """
        Version corrigée 5.3.2 - Gestion des seuils AMPA/NMDA
        """
        config = get_config()
        
        # --- RÉCUPÉRATION DES SEUILS (Correction du NameError) ---
        # On utilise les valeurs du fichier config.py ou des valeurs de secours
        ampa_threshold = config.get("THRESHOLD_AMPA", 0.1) 
        nmda_threshold = config.get("THRESHOLD_NMDA", 0.65)
        
        # --- CALCUL DE L'INTENSITÉ EFFECTIVE ---
        effective_intensity = min(1.0, intensity * importance) 
        
        # 1. TRANSMISSION AMPA (Signal volatil)
        if effective_intensity < ampa_threshold: 
            print(f"  ├─ Signal trop faible ou insignifiant. Ignoré.")
            return

        # 2. TRANSMISSION NMDA (Gravure Long Terme)
        current_trace = self.subfields["CA3"].get(label, 0.0)
        
        if effective_intensity >= nmda_threshold: 
            learning_rate = 0.1 * importance 
            new_value = current_trace + (effective_intensity * learning_rate)
            self.subfields["CA3"][label] = min(new_value, 1.0)
            print(f"  ├─ [NMDA OPEN] Importance: {importance:.2f} | Trace: {self.subfields['CA3'][label]:.4f}")
        else:
            # Simple passage électrique sans changement structurel permanent
            self.subfields["CA3"][label] = max(effective_intensity, current_trace)
            print(f"  ├─ [AMPA ONLY] Signal détecté mais non consolidé.")

"""
"They shall have stars at elbow and foot;
 Though they go mad they shall be sane,
 Though they sink through the sea they shall rise again;
 Though lovers be lost love shall not;
 And death shall have no dominion."
                            - Dylan Thomas' poem excerpt
"""