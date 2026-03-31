#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# src/registry.py - Le Génome Centralisé d'aNA v5.9

# --- MÉTABOLISME (Le Courant) ---
METABOLISM = {
    "HEART_RATE_BASE": 60.0,      # Pour l'affichage (BPM)
    "HEART_BASE_HZ": 1.0,         # Pour le calcul (1 Hz = 60 BPM)
    "HEART_MAX_HZ": 45.0,
    "ENERGY_MAX": 1.0,
    "ATP_RECOVERY_RATE": 0.005,
    "REFRACTORY_PERIOD": 0.05,
    "CRITICAL_LEVEL": 0.25        # Plafond de sécurité
}

# --- FLUX NEURONAL (Le Langage Commun) ---
# Correction de l'amnésie : Thalamus et Hippo utilisent ce format unique
SIGNALS = {
    "L4_FORMAT": "L4_INPUT_{nucleus}_{data}",
    "DOPA_INJECTION_NEW": 0.20,    # Surprise (Dopamine haute)
    "DOPA_INJECTION_KNOWN": 0.05,  # Habitude (Dopamine basse)
    "FEEDBACK_L6_GAIN": 0.5,       # Signal inhibiteur du Cortex
    "BASE_CONDUCTIVITY": 0.7,      # Votre concept de flux
    "MIN_RESISTANCE": 0.1          # Résistance synaptique minimale
}

# --- CONFIGURATION DU CŒUR ---
PULSE_CONFIG = {
    "FRICTION": 0.98,            # Amortissement du rythme cardiaque
    "DOPA_TO_HZ_GAIN": 20.0      # Sensibilité du cœur à la dopamine
}

INPUT_CONFIG = {
    "UNICODE_NORM": 1114111.0,  # Plafond Unicode pour la transduction
    "NOISE_LEVEL": 0.01,        # Réalisme biologique
    "DEFAULT_NUCLEUS": "MGN"    # Noyau par défaut pour le texte
}

ORGANS = {
    "THALAMUS": {
        "NUCLEI": ["MGN", "LGN", "MD", "RTN"],
        "RTN_BASE_INHIBITION": 0.1,
        "L6_GAIN": 0.5
    },
    "HIPPOCAMPUS": {
        "SUBFIELDS": ["DG", "CA3", "CA1", "CA2", "CA4"], # Restauration complète
        "ENERGY_MAX": 1.0,
        "RECOVERY": 0.08,
        "BURN_SCIENTIFIC": 0.002,
        "SIGMA_DEFAULT": 3e-07,
        "ENCODE_THRESHOLD": 0.7 
    },
    "NEOCORTEX": {
        "LOBES": ["OCCIPITAL", "TEMPORAL", "PARIETAL", "FRONTAL"],
        "BASE_ACTIVATION": 0.1,
        "SYNAPTIC_PLASTICITY": 0.01
    }
}

CORTEX_CONFIG = {
    "BASE_ACTIVATION": 0.1,
    "MAX_ACTIVATION": 1.0,
    "FEEDBACK_L6_GAIN": 0.5,  # Force du signal qui calme le Thalamus
    "SYNAPTIC_PLASTICITY": 0.01
}

# Mise à jour de la section ORGANS
ORGANS["NEOCORTEX"] = {
    "LOBES": ["OCCIPITAL", "TEMPORAL", "PARIETAL", "FRONTAL"]
}