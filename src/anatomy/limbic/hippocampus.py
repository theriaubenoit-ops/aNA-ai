#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hippocampus implementation for aNA v5.1 with:

This module implements the Hippocampus with its subfields (DG, CA1-CA4) for memory encoding, consolidation, and retrieval. It includes mechanisms for synaptic plasticity (LTP/LTD), emotional modulation of memory strength, and a novel "CA4" subfield for long-term trace stabilization.

Architecture, concept and supervision: Benoit Theriault
Collaboration, research and code: Gemini, Cline
"""
from typing import Dict
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from src.registry import ORGANS

class Hippocampus:
    def __init__(self, config=None, neuromodulator_core=None):
        # On s'assure d'avoir la config du registre si config est None
        #from src.registry import ORGANS
        self.config = config if config and "SUBFIELDS" in config else ORGANS["HIPPOCAMPUS"]
        self.neuromod_core = neuromodulator_core
        
        # Initialisation explicite de TOUS les sous-champs v5.1
        # Cela garantit que CA4 existe même si la config est partielle
        self.subfields = {
            "DG": {}, 
            "CA1": {}, 
            "CA2": {}, 
            "CA3": {}, 
            "CA4": {}
        }
        
        # On peut ensuite fusionner avec la config si nécessaire
        if "SUBFIELDS" in self.config:
            for sf in self.config["SUBFIELDS"]:
                if sf not in self.subfields:
                    self.subfields[sf] = {}

        self.short_term_memory = {}
        print("  [Hippocampus] v5.1 : Zones DG, CA1-CA4 initialisées.")

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
                print(f"DEBUG: Trace '{signal_label}' gravée par TRAUMA (Flash NMDA).")
            else:
                self.subfields["CA3"][signal_label] = self.config.get("MIN_LATENT_THRESHOLD", 0.001)
                print(f"DEBUG: Trace '{signal_label}' initialisée NEUTRE.")

        # 2. RENFORCEMENT (LTP)
        # On ajoute l'impact émotionnel à la force actuelle
        self.subfields["CA3"][signal_label] += (impact * self.config.get("LTP_GAIN", 0.1))
        
        # 3. ÉTANCHÉITÉ (On s'assure que le signal DG est présent)
        self.subfields["DG"][signal_label] = True

    async def apply_synaptic_decay(self):
        """
        Fonction de sédimentation : le CA4 agit comme un comparateur de survie.
        La trace s'érode (LTD) mais ne peut jamais descendre sous son plancher CA4.
        """
        # Seuil minimal par défaut pour les traces neutres
        default_min = self.config.get("MIN_LATENT_THRESHOLD", 0.001)
        
        for label in list(self.subfields["CA3"].keys()):
            # 1. Calcul de la décroissance standard (Burn Rate)
            # On simule l'érosion naturelle des liens synaptiques (LTD)
            self.subfields["CA3"][label] *= (1.0 - self.burn_rate)
            
            # 2. RÉCUPÉRATION DU PLANCHER DE SURVIE (Innovation CA4)
            # On interroge le CA4 : si une Trace Acide a été gravée (ex: 0.2), 
            # elle devient la limite infranchissable. Sinon, on utilise le seuil neutre.
            survival_floor = self.subfields["CA4"].get(label, default_min)
            
            # 3. ARBITRAGE DU COMPARATEUR
            # Si la valeur érodée descend sous le plancher de survie, on la verrouille.
            if self.subfields["CA3"][label] < survival_floor:
                self.subfields["CA3"][label] = survival_floor
                # Optionnel : log de maintenance pour le monitoring du dashboard
                # print(f"DEBUG: Trace '{label}' stabilisée par le plancher CA4 ({survival_floor}).")

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
