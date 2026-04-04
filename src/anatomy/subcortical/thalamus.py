#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Thalamus implementation for aNA v5.1

Communicates with: 
Input: (<- InputGateway) (<- Hippocampus) (<- Amygdala)
Input/Output: (<-> Cortical Columns L4/L6) 
Output: (-> Pulse/BPM) (-> Neuromodulator Gain)

This module implements the Thalamus as the central sensory relay and rhythmic pacemaker of aNA. It orchestrates the flow between subcortical structures and the Neocortex, specifically managing the L4 excitation and L6 feedback loops. It integrates with the ChemicalCore to modulate signal gain based on arousal and directs the Pulse (BPM) frequency, ensuring the organism maintains homeostatic stability during stimulus processing.

Architecture, concept and supervision: Benoit Theriault
Collaboration, research and code: Gemini, Cline
"""

import asyncio
from typing import Dict, Any
import sys
import os

# Alignement du path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from src.registry import SIGNALS, ORGANS

class Thalamus:
    def __init__(self, hippocampus, pulse, neuromodulator_core):
        """
        Initialisation v5.1 unifiée.
        """
        self.hippo = hippocampus
        self.pulse = pulse
        self.neurom = neuromodulator_core
        self.is_autonomous = False
        
        # Configuration extraite du registre
        config = ORGANS["THALAMUS"]
        self.l6_gain = 1.2 # Force de l'inhibition corticale
        self.base_bpm = 120.0
        self.current_bpm = 120.0
        
        # État des noyaux (MGN: Médian, LGN: Latéral, RTN: Réticulaire)
        self.nuclei_activity = {n: 0.0 for n in config["NUCLEI"]}

    def get_current_bpm(self, l6_feedback: float) -> float:
        """
        Calcule le BPM en fonction de l'excitation et de l'inhibition L6.
        C'est ici que William se calme ou s'excite.
        """
        # 1. On récupère la Noradrénaline (Alerte) du ChemicalCore
        nora = self.neurom.get_matrix().get("noradrenaline", 0.1)
        
        # 2. L'excitation brute (Nouveauté/Danger)
        excitation = 1.0 + (nora * 2.0) # Le trauma peut tripler le BPM
        
        # 3. L'inhibition corticale (Le 'Frein' de la connaissance)
        # Plus L6 est haut (reconnaissance), plus le gain est fort
        inhibition = l6_feedback * self.l6_gain
        
        # 4. Résultante : BPM = Base * (Excitation / (1 + Inhibition))
        target_bpm = self.base_bpm * (excitation / (1.0 + inhibition))
        
        # Sécurité biologique (Sommeil 110 - Panique 240)
        self.current_bpm = max(110.0, min(240.0, target_bpm))
        return self.current_bpm

    async def process_payload(self, payload: dict, l6_feedback: float):
        """
        Traite le signal et ajuste le Pulse en temps réel.
        """
        nucleus_target = payload.get("nucleus", "MGN")
        intensity = payload.get("intensity", 0.0)

        # 1. Évaluation par l'Hippocampe (Prédiction)
        # On utilise le signal_label pour vérifier si c'est déjà connu
        prediction_error = await self.hippo.evaluate_prediction(payload.get("signal_label", ""))
        
        # 2. Mise à jour du ChemicalCore via l'Amygdale (Simulée ici)
        # Si erreur forte + intensité forte = Noradrénaline boost
        if prediction_error > 0.7 and intensity > 0.6:
            self.neurom.update_from_limbic({"noradrenaline": 0.8, "dopamine_boost": 0.0})
        else:
            self.neurom.update_from_limbic({"dopamine_boost": 0.1})

        # 3. Ajustement du Pulse (Le rythme de calcul)
        new_bpm = self.get_current_bpm(l6_feedback)
        self.pulse.update_frequency(new_bpm)

        # 4. Activité des noyaux pour le Dashboard
        self.nuclei_activity[nucleus_target] = intensity
        
        return {
            "bpm": new_bpm,
            "thalamic_gain": 1.0 / (1.0 + l6_feedback)
        }
    
    async def internal_consciousness_loop(self):
        """Boucle de veille autonome de William v5.1"""
        print("  [Thalamus] Autonomous consciousness activated.")
        try:
            while self.is_autonomous:
                # 1. On vérifie l'état chimique (Dopamine = Curiosité)
                matrix = self.neurom.get_matrix()
                wait_time = 2.0 / (matrix['dopamine'] + 0.5) # Plus de dopa = plus rapide
                
                # 2. Simulation d'une micro-activité interne (bruit de fond)
                if matrix['noradrenaline'] < 0.3:
                    print(f"  [Auto] aNA is calm... BPM: {self.pulse.bpm:.1f}")
                else:
                    print(f"  [Auto] aNA is on alert! BPM: {self.pulse.bpm:.1f}")
                
                await asyncio.sleep(wait_time)
        except asyncio.CancelledError:
            print("  [Thalamus] Consciousness put on standby.")
