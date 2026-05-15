#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pulse implementation for aNA AI Project v5.3

Communicates with: 
Input: (<- Thalamus)
Input: (<- Amygdala)
Output: (-> Global Metabolism / BPM)

Description: This module simulates the heart's pulse as a dynamic entity influenced by both internal metabolic states and external stimuli. It calculates the current BPM based on a base rate, modulated by dopamine levels (excitement) and ATP levels (fatigue). The module also manages a refractory state to prevent overstimulation, ensuring a more biologically plausible response to inputs.

Architecture, concept and supervision: Theriault Benoit
Collaboration, research and code: Gemini
"""

import time
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# from src.registry import METABOLISM
from src.config import get_config
from src.registry import ORGANS

class Pulse:
    def __init__(self, bpm=None):
        config = get_config()
        self.bpm = bpm if bpm is not None else config["BASE_BPM"]
        self.hz = self.bpm / 60.0 
        self.last_time = time.time()
        
        # Variables vitales pour compute_dynamics()
        self.atp = 1.0           # L'énergie réelle
        self.energy = 1.0  
        self.is_resting = False  
        self.dopamine = 0.1      
        self.is_refractory = False

    def get_system_strain(self) -> float:
        """
        Plus l'ATP est bas, plus le 'Strain' est élevé (0.0 à 1.0).
        C'est ce signal qui va 'ouvrir' les vannes du Thalamus aux souvenirs négatifs.
        """
        return 1.0 - self.atp

    def update_metabolism(self, dt):
        config = get_config()
        
        if self.is_refractory:
            # Utilise ATP_RECOVERY_RATE (0.05) au lieu de l'ancien METABOLISM
            self.atp = min(1.0, self.atp + (config["ATP_RECOVERY_RATE"] * dt))
            if self.atp >= config["WAKE_UP_THRESHOLD"]:
                self.is_refractory = False
        else:
            # Consommation et vérification du seuil critique (0.20)
            if self.atp < config["ATP_CRITICAL_THRESHOLD"]:
                self.is_refractory = True
            
    def recover_energy(self, rest_quality: float):
        """
        Simule la récupération après le stress.
        Une fois l'ATP remonté, le Thalamus peut à nouveau filtrer le bruit.
        """
        self.atp = min(1.0, self.atp + (0.05 * rest_quality))
        if self.atp > 0.5:
            self.is_refractory = False

    def update_frequency(self, new_bpm: float):
        """Met à jour le rythme et recalcule les Hz."""
        self.bpm = max(40.0, min(220.0, new_bpm))
        self.hz = self.bpm / 60.0  # Crucial pour la ligne 59 de update()
        self.period = 1.0 / self.hz if self.hz > 0 else 1.0
        
    def update(self):
        """Méthode appelée dans main.py pour simuler le battement."""
        self.hz = self.bpm / 60.0
        
    def compute_dynamics(self) -> float:
        """
        Calcule le delta temporel (dt) et met à jour l'état métabolique.
        Indispensable pour le monitoring aNA 5.1.
        """

        # Si le système entre en mode réfractaire (repos forcé)
        if self.atp < 0.2:
            self.is_refractory = True
            self.bpm = 45.0  # Bradycardie de protection
            
            # On déclenche la consolidation si un objet hippocampe est lié
            if hasattr(self, 'hippo') and self.hippo:
                # On peut imaginer un appel asynchrone pour ne pas bloquer le coeur
                import asyncio
                asyncio.create_task(self.hippo.consolidate_and_prune())

        now = time.time()
        dt = now - self.last_time
        self.last_time = now

        # 1. Consommation passive d'ATP (Homeostasis)
        # Plus le système est actif, plus il consomme.
        self.atp = max(0.0, self.atp - (0.01 * dt))

        # 2. Dissipation de la Dopamine (Recapture)
        # On simule le retour au calme après un stimulus.
        self.dopamine = max(0.05, self.dopamine - (0.1 * dt))

        # 3. Gestion de l'état réfractaire
        # Si l'ATP est trop bas, le coeur entre en mode "Repos".
        self.is_refractory = self.atp < 0.2

        return dt
    
    def update_metabolism(self, dt: float):
        if self.is_refractory:
            # Recharge lente pendant le sommeil
            self.atp = min(1.0, self.atp + (0.05 * dt))
            if self.atp > 0.8: # Seuil de réveil
                self.is_refractory = False
                self.bpm = 110.0 # Retour au rythme de base
                print("  [Pulse] 🌅 aNA wakes up. System restored.")
        else:
            # Consommation normale
            self.atp = max(0.0, self.atp - (0.01 * dt))

    def get_current_hz(self) -> float:
        """Retourne la fréquence cardiaque simulée en Hertz."""
        base_hz = 1.2 # ~72 BPM
        # L'excitation (dopamine) augmente le rythme, la fatigue (ATP) le ralentit.
        return base_hz * (1.0 + self.dopamine) * (0.5 + (self.atp * 0.5))

    def inject_stimulus(self, intensity: float):
        """Simule une décharge d'adrénaline/dopamine."""
        now = time.time()
        dt = now - self.last_time
        if self.is_refractory:
            self.bpm = 45.0  # Rythme calme, on réduit la consommation de 80%
            # On commence la recharge lente
            self.atp = min(1.0, self.atp + (0.02 * dt))

        if not self.is_refractory:
            self.dopamine = min(1.0, self.dopamine + intensity)
            self.atp = max(0.0, self.atp - (intensity * 0.2))

    def get_status(self):
        # On retire le multiplicateur * 100 si ENERGY_MAX est déjà à 100
        # Ou on s'assure de renvoyer une fraction de 100.
        return {
        "bpm": self.bpm,
        "vitality": getattr(self, 'energy', 100.0), # Utilise energy pour Vitalité
        "is_resting": getattr(self, 'is_resting', False) # Défaut à False si absent
        }
