#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hippocampus implementation for aNA v5.1

Communicates with: Input: (<- Cortex / Amygdala) | Output: (-> Thalamus) (-> Cortical Storage)

This module implements the Hippocampus with its subfields (DG, CA1-CA4) for memory encoding, consolidation, and retrieval. It includes mechanisms for synaptic plasticity (LTP/LTD), emotional modulation of memory strength, and a novel "CA4" subfield for long-term trace stabilization.

Architecture, concept and supervision: Benoit Theriault
Collaboration, research and code: Gemini, Cline
"""

from typing import Dict
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from src.config import get_config
from src.registry import ORGANS

class Hippocampus:
    def __init__(self, config=None, neuromodulator_core=None):
        # 1. Le Génome (Structure fixe du registre)
        self.structure = ORGANS["HIPPOCAMPUS"]
        # Si config est None, on peut mettre des valeurs par défaut
        self.config = config if config else {}
        self.neurom_core = neuromodulator_core
        
        # Initialisation des sous-champs
        self.subfields = {field: {} for field in self.structure["SUBFIELDS"]}
        
        # On peut ensuite fusionner avec la config si nécessaire
        if "SUBFIELDS" in self.config:
            for sf in self.config["SUBFIELDS"]:
                if sf not in self.subfields:
                    self.subfields[sf] = {}

        self.short_term_memory = {}
        print("  [Hippocampus] v5.1 : Zones DG, CA1-CA4 initialized.")

    async def evaluate_prediction(self, signal_label: str) -> float:
        """
        Simule la boucle trisynaptique avec dynamique AMPA/NMDA.
        """
        # 1. DG : Séparation de motifs
        is_known_dg = signal_label in self.subfields["DG"]

        # 2. CA3 : Accès à la trace (Potentiel Synaptique)
        # On récupère la valeur actuelle ou le "bruit" résiduel (Seuil NMDA)
        trace_ca3 = self.subfields["CA3"].get(signal_label, self.config.get("MIN_LATENT_THRESHOLD", 0.001))

        # 3. CA1 : Comparateur et Modulation de la Plasticité
        if is_known_dg and trace_ca3 > self.config.get("MIN_LATENT_THRESHOLD", 0.001):
            # Mécanisme AMPA : Renforcement d'un chemin déjà "ouvert"
            # La croissance est logarithmique pour éviter la saturation rapide
            self.subfields["CA3"][signal_label] += self.config.get("LTP_GAIN", 0.05)
            
            # Calcul de l'erreur (plus la trace est forte, plus la prédiction est stable)
            prediction_error = 0.1 / self.subfields["CA3"][signal_label]
        else:
            # Mécanisme NMDA : "Réveil" d'une synapse silencieuse ou création
            # On passe du potentiel latent à une activation réelle
            prediction_error = 1.0
            self.subfields["DG"][signal_label] = True
            self.subfields["CA3"][signal_label] = self.config.get("INITIAL_ENGRAM_STRENGTH", 0.1)
            self.subfields["CA4"][signal_label] = 1.0 

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
                print(f"DEBUG: Trace '{signal_label}' engraved by TRAUMA (Flash NMDA).")
            else:
                self.subfields["CA3"][signal_label] = self.config.get("MIN_LATENT_THRESHOLD", 0.001)
                print(f"DEBUG: Trace '{signal_label}' initialized NEUTRAL.")

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

    async def update_trace_with_emotion(self, signal_label: str, impact: float, valence: float):
        """
        Ajuste la trace CA3 en fonction de l'impact fourni par l'Amygdale.
        """
        if signal_label not in self.subfields["CA3"]:
            self.subfields["CA3"][signal_label] = self.config.get("MIN_LATENT_THRESHOLD", 0.001)

        # La valence positive (plaisir) renforce doucement.
        # La valence négative (peur/douleur) grave la trace profondément (LTP forcée).
        if valence < -0.5:
            # "Trace Acide" : On augmente massivement la valeur pour qu'elle 
            # mette des années (cycles) à redescendre au seuil minimal.
            self.subfields["CA3"][signal_label] += (impact * 2.0)
        else:
            self.subfields["CA3"][signal_label] += (impact * 0.5)

        # Plafonnement pour éviter l'instabilité numérique
        self.subfields["CA3"][signal_label] = min(5.0, self.subfields["CA3"][signal_label])

    async def consolidate_and_prune(self):
        """
        Consolidation v5.1.1 : Utilise le tempérament pour décider 
        ce qui doit être oublié ou stabilisé.
        """
        config = get_config() # On récupère le tempérament actuel
        
        print("  [Hippocampe] 🧠 Synaptic consolidation in progress...")
        
        for label in list(self.subfields["CA3"].keys()):
            # 1. PRUNING (Élagage basé sur le bruit de fond de la config)
            # On utilise NOISE_LEVEL pour définir ce qui est insignifiant
            if self.subfields["CA3"][label] < config["NOISE_LEVEL"]:
                del self.subfields["CA3"][label]
                continue
                
            # 2. STABILISATION (Utilise le GAIN NMDA pour la force synaptique)
            if label in self.subfields["CA4"]:
                floor = self.subfields["CA4"][label]
                # On utilise THRESHOLD_NMDA pour lisser la trace vers la sagesse
                learning_factor = config["THRESHOLD_NMDA"] 
                self.subfields["CA3"][label] = (self.subfields["CA3"][label] + floor) * learning_factor

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
            # intensité dans CA3 pour que William ne soit plus en 'panique' au réveil.
            if label in self.subfields["CA4"]:
                # On rapproche la trace de son plancher de survie (Sagesse > Peur)
                target_floor = self.subfields["CA4"][label]
                self.subfields["CA3"][label] = (self.subfields["CA3"][label] + target_floor) / 2

    async def consolidate_and_prune(self):
        """
        Simule le sommeil paradoxal (REM) : 
        Élagage des bruits et stabilisation des leçons de survie.
        """
        print("  [Hippocampe] 🧠 Synaptic consolidation in progress...")
        
        for label in list(self.subfields["CA3"].keys()):
            # 1. PRUNING (Élagage)
            # Si une trace est trop faible (< 0.05), elle est considérée comme du bruit.
            # On libère de la mémoire.
            if self.subfields["CA3"][label] < 0.05:
                del self.subfields["CA3"][label]
                continue
                
            # 2. APOIDEMENT DES TRACES ACIDES (CA4)
            # Si le souvenir est marqué comme "danger" dans le CA4 :
            if label in self.subfields["CA4"]:
                # On réduit l'amplitude de la trace dans le CA3.
                # Le but : garder le souvenir du danger, mais supprimer la panique (le pic de BPM).
                floor = self.subfields["CA4"][label]
                # On lisse la valeur vers le plancher de survie
                self.subfields["CA3"][label] = (self.subfields["CA3"][label] + floor) / 2
                
        print("  [Hippocampus] ✅ Cleaning complete. aNA is ready for a new cycle.")
