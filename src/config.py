#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
aNA v5.2 - Configuration Module (Temperament)
Description: Centralization of dynamic thresholds for AI customization. This module defines the adjustable parameters that shape the AI's temperament and responsiveness. By modifying these values, users can create different personality profiles, from calm to anxious, while maintaining the underlying architecture's stability. These parameters influence how the AI reacts to stimuli, manages energy, and processes information, allowing for a personalized experience without compromising the system's integrity.

aNA v5.2 - Configuration Module (Le Tempérament) (FR)
Description : Centralisation des seuils dynamiques pour la personnalisation de l'IA. Ce module définit les paramètres ajustables qui déterminent le tempérament et la réactivité de l'IA. En modifiant ces valeurs, les utilisateurs peuvent créer différents profils de personnalité, du calme à l'anxiété, tout en préservant la stabilité de l'architecture sous-jacente. Ces paramètres influencent la manière dont l'IA réagit aux stimuli, gère son énergie et traite l'information, permettant ainsi une expérience personnalisée sans compromettre l'intégrité du système.

Architecture, concept and supervision: Benoit Theriault
Collaboration, research and code: Gemini
"""

# -  -  -  -  -  PHILOSOPHICAL ANCHOR / ANCRAGE PHILOSOPHIQUE (FR)  -  -  -  -  -  - #
# "The inclusion of these specific biological modules is not a stylistic choice,     #
# but a mechanical necessity. Their presence is vital for the systemic function,     #
# coherent learning, and the emergence of a truly grounded World Model."             #
# -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  - #

# --- PERSONALITY HYPERPARAMETERS / HYPER-PARAMÈTRES DE PERSONNALITÉ (FR) ---
AMYGDALA_SENSITIVITY = 1.0      # Amygdala Sensitivity Min: 0.1 (unperturbed) Max: 2.0 (hyper-reactive) / Sensibilité de l'amygdale 
ADRENALINE_RELEASE_FACTOR = 0.4 # Adrenaline Release Factor Min: 0.1 (calm) Max: 1.0 (explosive) / Facteur de libération d'adrénaline 
L6_GAIN = 0.5                   # Cortical Brake Strength Min: 0.0 (no brake) Max: 2.0 (total inhibition) / Force du frein cortical 

# --- HEART CONFIGURATION & METABOLISM / CONFIGURATION DU CŒUR & MÉTABOLISME (FR) ---
BASE_BPM = 120.0                # Cruising Heart Rate Min: 60.0 (deep sleep) Max: 140.0 (alert) / Rythme de croisière 
BRADYCARDIA_BPM = 45.0          # Protective Heart Rate Min: 45.0 (bradycardia) Max: 60.0 (resting rate) / Rythme de protection 
MAX_VIGILANCE_BPM = 240.0       # Safety ceiling Min: 180.0 (intense stress) Max: 240.0 (extreme emergency) / Plafond de sécurité 
PULSE_FRICTION = 0.98           # Heart rate damping Min: 0.80 (unstable) Max: 0.99 (ultra-stable) / Amortissement du rythme cardiaque 
DOPA_TO_HZ_GAIN = 20.0          # Dopamine sensitivity Min: 5.0 (low sensitivity) Max: 50.0 (hyper-reactive) / Sensibilité à la dopamine 

# --- ENERGY THRESHOLDS / SEUILS ÉNERGÉTIQUES (FR) ---
ATP_CRITICAL_THRESHOLD = 0.20   # Transition to REFRACTORY_REST mode Min: 0.05 (very critical) Max: 0.30 (less critical) / Passage en mode REFRACTORY_REST 
ATP_FATIGUE_ZONE = 0.40         # Hypervigilance Trigger Min: 0.30 (rapid fatigue) Max: 0.60 (late fatigue) / Déclenchement de l'hyper-vigilance 
RECOVERY_RATE = 0.05            # ATP Recharge Rate (Sleep) Min: 0.01 (slow recovery) Max: 0.20 (rapid recovery) / Vitesse de recharge ATP (Sommeil)
WAKE_UP_THRESHOLD = 0.80        # Wake-Up Threshold Min: 0.60 (late wake-up) Max: 0.95 (early wake-up) / Seuil de réveil 

# --- PLASTICITY & LEARNING (Hippocampus/Cortex) / PLASTICITÉ & APPRENTISSAGE (Hippocampe/Cortex) (FR) ---
THRESHOLD_NMDA = 0.4            # Memory Lock Threshold Min: 0.1 (easy to encode) Max: 0.9 (difficult to encode) / Seuil pour le verrouillage des souvenirs 
ENCODE_THRESHOLD = 0.7          # Energy Required for Encoding Min: 0.1 (encoding) Easy) Max: 1.0 (difficult memorization) / Intensité requise pour la mémorisation 
HIPPO_RECOVERY = 0.08           # Hippocampal energy recovery Min: 0.01 (slow recovery) Max: 0.20 (fast recovery) / Récupération énergétique de l'Hippocampe 
SYNAPTIC_PLASTICITY = 0.01      # Baseline learning rate Min: 0.001 (slow learning) Max: 0.10 (fast learning) / Vitesse d'apprentissage de base
MYELIN_RATE = 0.01              # Pathway strengthening rate Min: 0.001 (slow wiring) Max: 0.05 (fast wiring) / Vitesse de renforcement des chemins 
BASE_CONDUCTIVITY = 0.7         # Neural flow concept Min: 0.1 (low) Max: 1.0 (high) / Concept de flux neuronal 
MIN_RESISTANCE = 0.1            # Minimum synaptic resistance Min: 0.001 (very low) Max: 0.05 (highest resistance) / Résistance synaptique minimale 

# --- SIGNAL & DOPAMINE SETTINGS / RÉGLAGES DES SIGNAUX & DOPAMINE (FR) ---
DOPA_INJECTION_NEW = 0.20       # Surprise (High Dopamine) Min: 0.05 (Little Surprise) Max: 0.50 (Extreme Surprise) / Surprise (Dopamine haute) 
DOPA_INJECTION_KNOWN = 0.05     # Habit (Low Dopamine) Min: 0.01 (Little Dopamine) Max: 0.50 (Moderate Dopamine) / Habitude (Dopamine basse) 
RTN_BASE_INHIBITION = 0.1       # Default Thalamic Silence Level Min: 0.0 (No Inhibition) Max: 0.5 (Strong Inhibition) / Niveau de silence thalamique par défaut 
NOISE_LEVEL = 0.01              # Biological Realism (Background Noise) Min: 0.0 (No Noise) Max: 0.10 (A lot of noise; beyond this, the signal becomes unreadable) / Réalisme biologique (Bruit de fond)


def get_config():
    """
    Returns the complete configuration for injection into the organs. This function centralizes all the parameters, allowing for easy adjustments and ensuring that all components of the architecture are aligned with the same temperament settings.
    """
    return {
        "AMYGDALA_SENSITIVITY": AMYGDALA_SENSITIVITY,
        "ADRENALINE_RELEASE_FACTOR": ADRENALINE_RELEASE_FACTOR,
        "L6_GAIN": L6_GAIN,
        "BASE_BPM": BASE_BPM,
        "BRADYCARDIA_BPM": BRADYCARDIA_BPM,   
        "MAX_VIGILANCE_BPM": MAX_VIGILANCE_BPM,
        "ATP_CRITICAL_THRESHOLD": ATP_CRITICAL_THRESHOLD,
        "ATP_FATIGUE_ZONE": ATP_FATIGUE_ZONE,
        "RECOVERY_RATE": RECOVERY_RATE,
        "WAKE_UP_THRESHOLD": WAKE_UP_THRESHOLD,
        "PULSE_FRICTION": PULSE_FRICTION,
        "DOPA_TO_HZ_GAIN": DOPA_TO_HZ_GAIN,
        "THRESHOLD_NMDA": THRESHOLD_NMDA,
        "ENCODE_THRESHOLD": ENCODE_THRESHOLD,
        "HIPPO_RECOVERY": HIPPO_RECOVERY,
        "SYNAPTIC_PLASTICITY": SYNAPTIC_PLASTICITY,
        "DOPA_INJECTION_NEW": DOPA_INJECTION_NEW,
        "DOPA_INJECTION_KNOWN": DOPA_INJECTION_KNOWN,
        "RTN_BASE_INHIBITION": RTN_BASE_INHIBITION,
        "BASE_CONDUCTIVITY": BASE_CONDUCTIVITY,
        "NOISE_LEVEL": NOISE_LEVEL
    }

# -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  - #
#    “For every complex problem, there is a solution that is simple, neat, and wrong.” — H.L. Mencken     #
# -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  - #
