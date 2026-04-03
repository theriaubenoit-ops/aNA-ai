#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# src/core/pulse.py
import time
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.registry import METABOLISM

class Pulse:
    def __init__(self, bpm=120.0):
        self.bpm = bpm
        self.hz = self.bpm / 60.0 
        self.last_time = time.time() 
        self.atp = 1.0             
        self.energy = 1.0           
        self.dopamine = 0.1         
        self.is_refractory = False
        
    def update_frequency(self, new_bpm: float):
        """Met à jour le rythme et recalcule les Hz."""
        self.bpm = max(40.0, min(220.0, new_bpm))
        self.hz = self.bpm / 60.0  # Crucial pour la ligne 59 de update()
        self.period = 1.0 / self.hz if self.hz > 0 else 1.0
        # self.last_time = time.time() # Optionnel selon ta gestion du dt

        # --- LIGNE SUPPRIMÉE ---
        # print(f"  [Pulse] Nouveau BPM: {self.bpm:.2f}")
        
    def update(self):
        """Méthode appelée dans main.py pour simuler le battement."""
        # Ton code actuel à la ligne 59 utilise METABOLISM["HEART_BASE_HZ"]
        # Assure-toi que self.hz est bien à jour ici
        self.hz = self.bpm / 60.0
        
    def compute_dynamics(self) -> float:
        """
        Calcule le delta temporel (dt) et met à jour l'état métabolique.
        Indispensable pour le monitoring aNA 5.1.
        """
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

    def get_current_hz(self) -> float:
        """Retourne la fréquence cardiaque simulée en Hertz."""
        base_hz = 1.2 # ~72 BPM
        # L'excitation (dopamine) augmente le rythme, la fatigue (ATP) le ralentit.
        return base_hz * (1.0 + self.dopamine) * (0.5 + (self.atp * 0.5))

    def inject_stimulus(self, intensity: float):
        """Simule une décharge d'adrénaline/dopamine."""
        if not self.is_refractory:
            self.dopamine = min(1.0, self.dopamine + intensity)
            self.atp = max(0.0, self.atp - (intensity * 0.2))

    def get_status(self):
        # On retire le multiplicateur * 100 si ENERGY_MAX est déjà à 100
        # Ou on s'assure de renvoyer une fraction de 100.
        return {
            "bpm": self.hz * 60,
            "energy": max(0, self.energy), # On affiche la valeur brute
            "hz": self.hz
        }
