#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
aNA v5.3 - Configuration Module (Temperament)
Description: Centralization of dynamic thresholds for AI customization. This module defines the adjustable parameters that shape the AI's temperament and responsiveness. By modifying these values, users can create different personality profiles, from calm to anxious, while maintaining the underlying architecture's stability. These parameters influence how the AI reacts to stimuli, manages energy, and processes information, allowing for a personalized experience without compromising the system's integrity.

aNA v5.3 - Configuration Module (Le temperament) (FR)
Description : Centralisation des seuils dynamiques pour la personnalisation de l'IA. Ce module définit les paramètres ajustables qui déterminent le tempérament et la réactivité de l'IA. En modifiant ces valeurs, les utilisateurs peuvent créer différents profils de personnalité, du calme à l'anxiété, tout en préservant la stabilité de l'architecture sous-jacente. Ces paramètres influencent la manière dont l'IA réagit aux stimuli, gère son énergie et traite l'information, permettant ainsi une expérience personnalisée sans compromettre l'intégrité du système.

Architecture, concept and supervision: Benoit Theriault
Collaboration, research and code: Gemini
"""

import os
import sys
import json

# --- TEMPERAMENT SELECTOR / SÉLECTEUR DE TEMPERAMENT (FR) ---
# This section allows users to select a predefined temperament profile, which adjusts the AI's parameters to create different behavioral tendencies.
# Cette section permet aux utilisateurs de sélectionner un profil de tempérament prédéfini, qui ajuste les paramètres de l'IA pour créer différentes tendances comportementales.
ACTIVE_PROFILE = "HIGH_PERFORMER"

PROFILES = {
    "HIGH_PERFORMER": {
        "AMYGDALA_SENSITIVITY": 0.5,
        "THALAMIC_THRESHOLD": 0.35,
        "ATP_CONSUMPTION": 0.001,
        "THRESHOLD_NMDA": 0.1,
        "MYELIN_EFFICIENCY_COEFF": 2.0
    },
    "AVERAGE": {
        "AMYGDALA_SENSITIVITY": 1.0,
        "THALAMIC_THRESHOLD": 0.15,
        "ATP_CONSUMPTION": 0.003,
        "THRESHOLD_NMDA": 0.25,
        "MYELIN_EFFICIENCY_COEFF": 1.5
    },
    "TIRED": {
        "AMYGDALA_SENSITIVITY": 1.8,
        "THALAMIC_THRESHOLD": 0.05, # Très bas, le portier est trop fatigué pour filtrer
        "ATP_CONSUMPTION": 0.005,
        "THRESHOLD_NMDA": 0.5, # Besoin de plus de répétitions pour verrouiller les souvenirs
        "MYELIN_EFFICIENCY_COEFF": 1.0
    }
}
selected = PROFILES[ACTIVE_PROFILE]
AMYGDALA_SENSITIVITY      = selected["AMYGDALA_SENSITIVITY"]
THALAMIC_THRESHOLD        = selected["THALAMIC_THRESHOLD"]
ATP_CONSUMPTION           = selected["ATP_CONSUMPTION"]
THRESHOLD_NMDA            = selected["THRESHOLD_NMDA"]
MYELIN_EFFICIENCY_COEFF   = selected["MYELIN_EFFICIENCY_COEFF"]

# -  -  -  -  ARCHITECTURAL MANIFESTO / MANIFESTE ARCHITECTURAL (FR) -  -  -  -  - #
#  "The inclusion of these specific biological modules is not a stylistic choice,  #
#  but a mechanical necessity. Their presence is vital for systemic function,      #
#  coherent learning, and the emergence of a truly grounded World Model."          #
#                                                                                  #
# "L'inclusion de ces modules biologiques précis n'est pas un choix esthétique,    #
#  mais une nécessité mécanique. Leur présence est vitale au fonctionnement        #
#  systémique, à l'apprentissage cohérent et à l'émergence d'un Modèle du Monde    #
#  (World Model) réellement ancré."                                                #
# -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  #

# --- PERSONALITY HYPERPARAMETERS / HYPER-PARAMÈTRES DE PERSONNALITÉ (FR) ---
# AMYGDALA_SENSITIVITY = 0.5       # Amygdala Sensitivity Min: 0.1 (unperturbed) Max: 2.0 (hyper-reactive) / Sensibilité de l'amygdale 
ADRENALINE_RELEASE_FACTOR = 0.4    # Adrenaline Release Factor Min: 0.1 (calm) Max: 1.0 (explosive) / Facteur de libération d'adrénaline 
ACH_ATTENTION_MULTIPLIER = 1.5     # Acetylcholine Attention Multiplier Min: 0.5 (distracted) Max: 2.0 (hyper-focused) / Multiplicateur d'attention à l'acétylcholine
ATTENTION_MIN_GAIN = 0.01          # Minimum attention gain Min: 0.01 (distracted) Max: 0.10 (always attentive) / Gain d'attention minimum
L23_EFFICIENCY = 0.85              # Layer II/III Efficiency Min: 0.1 (inefficient) Max: 0.99 (ultra-efficient) / Efficacité des couches II/III (intégration corticale)
L4_EFFICIENCY = 0.90               # Layer IV Efficiency Min: 0.1 (inefficient) Max: 0.99 (ultra-efficient) / Efficacité de la couche IV (réception thalamique)
L5_EFFICIENCY = 0.85               # Layer V Efficiency Min: 0.1 (inefficient) Max: 0.99 (ultra-efficient) / Efficacité de la couche V (commande motrice)
L6_EFFICIENCY = 0.80               # Layer VI Efficiency Min: 0.1 (inefficient) Max: 0.99 (ultra-efficient) / Efficacité de la couche VI (rétroaction corticale)
L6_GAIN = 0.8                      # Cortical Brake Strength Min: 0.0 (no brake) Max: 2.0 (total inhibition) / Force du frein cortical 
TRAUMA_NORA_THRESHOLD = 0.6        # Trauma Threshold for Noradrenaline Min: 0.1 (low trauma) Max: 0.9 (high trauma) / Seuil de traumatisme pour la noradrénaline
FLASH_MYELIN_BOOST = 0.05          # Myelin boost during flash engraving Min: 0.01 (subtle) Max: 0.10 (dramatic) / Boost de myéline lors de la gravure flash
BIOLOGICAL_ACCURACY_TARGET = 0.65  # Target for biological realism (0.0 to 1.0) Min: 0.0 (abstract) Max: 1.0 (fully biological) / Cible pour le réalisme biologique (0.0 à 1.0)

# --- HEART CONFIGURATION & METABOLISM / CONFIGURATION DU CŒUR & MÉTABOLISME (FR) ---
BASE_BPM = 65.0                    # Cruising Heart Rate Min: 60.0 (deep sleep) Max: 100.0 (alert) / Rythme de croisière 
MAX_BPM = 136.0                    # Excitation limit Min: 100.0 (little emotional reactivity) Max: 170.0 (alert) / Limite d'excitation
MAX_VIGILANCE_BPM = 200.0          # Safety ceiling Min: 170.0 (intense stress) Max: 200.0 (extreme emergency) / Plafond de sécurité 
BRADYCARDIA_BPM = 45.0             # Protective Heart Rate Min: 45.0 (bradycardia) Max: 60.0 (resting rate) / Rythme de protection 
PULSE_FRICTION = 0.93              # Heart rate damping Min: 0.80 (unstable) Max: 0.99 (ultra-stable) / Amortissement du rythme cardiaque 
DOPA_TO_HZ_GAIN = 20.0             # Dopamine sensitivity Min: 5.0 (low sensitivity) Max: 50.0 (hyper-reactive) / Sensibilité à la dopamine 
THALAMUS_BASE_BPM = 72.0           # Resting heart rate (target) Min: 60.0 (deep sleep) Max: 100.0 (alert) / Rythme cardiaque de repos (cible)
THALAMUS_MAX_BPM = 150.0           # Absolute safety ceiling. Min: 120.0 (high stress) Max: 180.0 (critical limit) / Plafond absolu de sécurité (limite critique)
THALAMUS_DECAY_FACTOR = 0.15       # Speed ​​of return to rest (0.1 = 10% per cycle) Min: 0.1 (slow) Max 0.5 (fast) / Vitesse de retour au calme (0.1 = 10% par cycle)
RECOGNITION_METABOLIC_DROP = 6.0   # Target BPM reduction upon pattern match (no savings) Max: 10.0 (high efficiency) / Une reconnaissance réduit le BPM cible

# --- ENERGY THRESHOLDS / SEUILS ÉNERGÉTIQUES (FR) ---
ATP_CRITICAL_THRESHOLD = 0.10      # Transition to REFRACTORY_REST mode Min: 0.05 (very critical) Max: 0.30 (less critical) / Passage en mode REFRACTORY_REST 
ATP_FATIGUE_ZONE = 0.40            # Hypervigilance Trigger Min: 0.30 (rapid fatigue) Mid: (0.15 and 0.40) Max: 0.60 (late fatigue) / Déclenchement de l'hyper-vigilance 
# ATP_CONSUMPTION = 0.001          # Fatigue per cycle Min: 0.001 (endurance) Max: 0.005 (rapid depletion) / Fatigue par cycle
RECOVERY_RATE = 0.05               # ATP Recharge Rate (Sleep) Min: 0.01 (slow recovery) Max: 0.20 (rapid recovery) / Vitesse de recharge ATP (Sommeil)
WAKE_UP_THRESHOLD = 0.80           # Wake-Up Threshold Min: 0.60 (late wake-up) Max: 0.95 (early wake-up) / Seuil de réveil 

# --- PLASTICITY & LEARNING (Hippocampus/Cortex) / PLASTICITÉ & APPRENTISSAGE (Hippocampe/Cortex) (FR) ---
AMPA_BASE_THRESHOLD = 0.15         # Activation threshold AMPA (Basic transmission) Min: 0.05 (Extreme sensitivity) Max: 0.30 (Must be strong to be heard) / Seuil d'activation AMPA
# THRESHOLD_NMDA = 0.65              # Memory Lock Threshold (NMDA, "Magnesium ion") Min: 0.1 (Easy learning/credulous) Max: 0.9 (Difficult/critical learning) / Seuil pour le verrouillage des souvenirs 
LTP_GAIN_FACTOR = 0.25             # Facteur de renforcement (LTP) Min: 0.05 (Slow plasticity) Max: 0.50 (Ultra-fast/unstable plasticity) / Seuil d'activation AMPA
ATP_CRITICAL_MIN = 0.20            # Parameter for the future "NMDA_Lock" Min: 0.05 (Extreme Survival) Max: 0.40 (High Energy Caution) / Paramètre pour le futur "NMDA_Lock"
CURRENT_ATP = 1.0                  # Current energy level  Min: 0.15 (Survival Threshold) Max: 1.20 (Hyper-Vigilance) / Niveau d'énergie actuel
ENCODE_THRESHOLD = 0.7             # Energy Required for Encoding Min: 0.1 (Everything is memorized) Max: 1.0 (Nothing is memorized without emotional shock) / Intensité requise pour la mémorisation 
HIPPO_RECOVERY = 0.08              # Hippocampal energy recovery Min: 0.01 (Slow Recovery, Fatigue Quickly) Max: 0.20 (High Cognitive Endurance) / Récupération énergétique de l'Hippocampe 
SYNAPTIC_PLASTICITY = 0.05         # Baseline learning rate Min: 0.001 (slow learning) Max: 0.10 (fast learning) / Vitesse d'apprentissage de base
MYELIN_RATE = 0.04               # Pathway strengthening rate Min: 0.001 (slow wiring) Max: 0.05 (fast wiring) / Vitesse de renforcement des chemins 
# MYELIN_EFFICIENCY_COEFF = 1.5      # Richness of the wiring Min: 1.0 (standard) Max: 2.5  (super-conducteur)/ Richesse du câblage 
MAX_MYELIN_DENSITY = 1.0           # Maximum synaptic insulation. Min: 0.1 (raw fiber) Max: 1.0 (fully myelinated) / Densité maximale de myéline (isolation synaptique)
CORTICAL_RESONANCE_FACTOR = 0.9    # Prediction persistence  Min: 0.10 (unstable) Max: 0.95 (stable) / Persistance de la prédiction 
BASE_CONDUCTIVITY = 0.7            # Neural flow concept Min: 0.1 (Slow/Viscous Flux) Max: 1.0 (Instantaneous/Fluid Flux) / Concept de flux neuronal 
MIN_RESISTANCE = 0.1               # Minimum synaptic resistance Min: 0.01 (Superconducting Synapses) Max: 0.2 (Always Resistant Synapses) / Résistance synaptique minimale 
NEURON_PLASTICITY_DECAY = 0.9999   # Plasticity decay per cycle Min: 0.90 (rapid forgetting) Max: 0.9999 (long-term retention) / Décay de la plasticité par cycle

# --- SIGNAL & DOPAMINE SETTINGS / RÉGLAGES DES SIGNAUX & DOPAMINE (FR) ---
DOPA_INJECTION_NEW = 0.20          # Surprise (High Dopamine) Min: 0.05 (Little Surprise) Max: 0.50 (Extreme Surprise) / Surprise (Dopamine haute) 
DOPA_INJECTION_KNOWN = 0.05        # Habit (Low Dopamine) Min: 0.01 (Little Dopamine) Max: 0.50 (Moderate Dopamine) / Habitude (Dopamine basse) 
RTN_BASE_INHIBITION = 0.1          # Default Thalamic Silence Level Min: 0.0 (No Inhibition) Max: 0.5 (Strong Inhibition) / Niveau de silence thalamique par défaut 
NOISE_LEVEL = 0.01                 # Biological Realism (Background Noise) Min: 0.0 (No Noise) Max: 0.10 (A lot of noise; beyond this, the signal becomes unreadable) / Réalisme biologique (Bruit de fond)

# --- THALAMIC & SENSORY PARAMETERS / PARAMÈTRES THALAMIQUES & SENSORIELS (FR) ---
# THALAMIC_THRESHOLD = 0.35          # THALAMIC THRESHOLD (Average human) Min: 0.05 (Anxious) Max: 0.45 (Stoic) / SEUIL THALAMIQUE
THALAMIC_REFRACTORY_PERIOD = 0.05  # RECOVERY TIME Min: 0.01 (Fast) Max: 0.20 (Slow) / TEMPS DE RÉCUPÉRATION

# --- Relative importance of the senses / Importance relative des sens (FR) ---
SENSORY_WEIGHTS = {                # AVERAGE HUMAN (visual priority) Total: 1.0 (Sensory weights) / HUMAIN MOYEN (priorité visuel) 
    "haptic": 0.40,                # Min: 0.10 Max: 0.50 (responsive)
    "visual": 0.80,                # Min: 0.05 Max: 0.80 (visual dominates)
    "auditory": 0.50               # Min: 0.10 Max: 0.60 (attentive to noise)
}

def get_config():
    """
    Returns the complete configuration for injection into the organs. This function centralizes all the parameters, allowing for easy adjustments and ensuring that all components of the architecture are aligned with the same temperament settings.
    """
    return {
        "ACTIVE_PROFILE": ACTIVE_PROFILE,
        "PROFILES": PROFILES,
        "ATTENTION_MIN_GAIN": ATTENTION_MIN_GAIN,
        "AMYGDALA_SENSITIVITY": AMYGDALA_SENSITIVITY,
        "ADRENALINE_RELEASE_FACTOR": ADRENALINE_RELEASE_FACTOR,
        "ACH_ATTENTION_MULTIPLIER": ACH_ATTENTION_MULTIPLIER,
        "L23_EFFICIENCY": L23_EFFICIENCY,
        "L4_EFFICIENCY": L4_EFFICIENCY,
        "L5_EFFICIENCY": L5_EFFICIENCY,
        "L6_EFFICIENCY": L6_EFFICIENCY,
        "L6_GAIN": L6_GAIN,
        "TRAUMA_NORA_THRESHOLD": TRAUMA_NORA_THRESHOLD,
        "FLASH_MYELIN_BOOST": FLASH_MYELIN_BOOST,
        "BIOLOGICAL_ACCURACY_TARGET": BIOLOGICAL_ACCURACY_TARGET,
        "BASE_BPM": BASE_BPM,
        "MAX_BPM": MAX_BPM,   
        "BRADYCARDIA_BPM": BRADYCARDIA_BPM,   
        "MAX_VIGILANCE_BPM": MAX_VIGILANCE_BPM,
        "ATP_CRITICAL_THRESHOLD": ATP_CRITICAL_THRESHOLD,
        "ATP_FATIGUE_ZONE": ATP_FATIGUE_ZONE,
        "RECOVERY_RATE": RECOVERY_RATE,
        "THALAMIC_THRESHOLD": THALAMIC_THRESHOLD,
        "SENSORY_WEIGHTS": SENSORY_WEIGHTS,
        "THALAMIC_REFRACTORY_PERIOD": THALAMIC_REFRACTORY_PERIOD,
        "WAKE_UP_THRESHOLD": WAKE_UP_THRESHOLD,
        "PULSE_FRICTION": PULSE_FRICTION,
        "DOPA_TO_HZ_GAIN": DOPA_TO_HZ_GAIN,
        "RECOGNITION_METABOLIC_DROP": RECOGNITION_METABOLIC_DROP,
        "THALAMUS_BASE_BPM": THALAMUS_BASE_BPM,
        "THALAMUS_MAX_BPM": THALAMUS_MAX_BPM,
        "THALAMUS_DECAY_FACTOR": THALAMUS_DECAY_FACTOR,
        "AMPA_BASE_THRESHOLD": AMPA_BASE_THRESHOLD,
        "THRESHOLD_NMDA": THRESHOLD_NMDA,
        "LTP_GAIN_FACTOR": LTP_GAIN_FACTOR,
        "ATP_CRITICAL_MIN": ATP_CRITICAL_MIN,
        "CURRENT_ATP": CURRENT_ATP,
        "ENCODE_THRESHOLD": ENCODE_THRESHOLD,
        "HIPPO_RECOVERY": HIPPO_RECOVERY,
        "SYNAPTIC_PLASTICITY": SYNAPTIC_PLASTICITY,
        "DOPA_INJECTION_NEW": DOPA_INJECTION_NEW,
        "DOPA_INJECTION_KNOWN": DOPA_INJECTION_KNOWN,
        "RTN_BASE_INHIBITION": RTN_BASE_INHIBITION,
        "BASE_CONDUCTIVITY": BASE_CONDUCTIVITY,
        "MIN_RESISTANCE": MIN_RESISTANCE,
        "NEURON_PLASTICITY_DECAY": NEURON_PLASTICITY_DECAY,
        "NOISE_LEVEL": NOISE_LEVEL,
        "MYELIN_EFFICIENCY_COEFF": MYELIN_EFFICIENCY_COEFF,
        "CORTICAL_RESONANCE_FACTOR": CORTICAL_RESONANCE_FACTOR,
        "MYELIN_RATE": MYELIN_RATE,
        "MAX_MYELIN_DENSITY": MAX_MYELIN_DENSITY,
        "ATP_CONSUMPTION": ATP_CONSUMPTION
    }

# -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -#
#  “For every complex problem, there is a solution that is simple, neat, and wrong.”   #
#  « À chaque problème complexe correspond une solution simple, élégante et fausse. »  #
#                                                                   — H.L. Mencken     #
# -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -#
