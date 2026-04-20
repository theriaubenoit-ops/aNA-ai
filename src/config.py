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

# ==============================================================================================
#  SEE PROFILES NEURAL PERFORMANCE (BELOW) / VOIR PROFILS DE PERFORMANCES NEURALES (CI-DESSOUS)
# ==============================================================================================

# --- PERSONALITY HYPERPARAMETERS / HYPER-PARAMÈTRES DE PERSONNALITÉ (FR) ---
# AMYGDALA_SENSITIVITY = 0.5       # Amygdala Sensitivity Min: 0.1 (unperturbed) Max: 2.0 (hyper-reactive) / Sensibilité de l'amygdale 
ADRENALINE_RELEASE_FACTOR = 0.4    # Adrenaline Release Factor Min: 0.1 (calm) Max: 1.0 (explosive) / Facteur de libération d'adrénaline 
# L6_GAIN = 0.8                      # Cortical Brake Strength Min: 0.0 (no brake) Max: 2.0 (total inhibition) / Force du frein cortical 

# --- HEART CONFIGURATION & METABOLISM / CONFIGURATION DU CŒUR & MÉTABOLISME (FR) ---
BASE_BPM = 72.0                    # Cruising Heart Rate Min: 60.0 (deep sleep) Max: 140.0 (alert) / Rythme de croisière 
MAX_BPM = 160.0                    # Excitation limit Min: 110.0 (little emotional reactivity) Max: 220.0 (alert) / Limite d'excitation
MAX_VIGILANCE_BPM = 200.0          # Safety ceiling Min: 180.0 (intense stress) Max: 240.0 (extreme emergency) / Plafond de sécurité 
BRADYCARDIA_BPM = 45.0             # Protective Heart Rate Min: 45.0 (bradycardia) Max: 60.0 (resting rate) / Rythme de protection 
PULSE_FRICTION = 0.98              # Heart rate damping Min: 0.80 (unstable) Max: 0.99 (ultra-stable) / Amortissement du rythme cardiaque 
DOPA_TO_HZ_GAIN = 20.0             # Dopamine sensitivity Min: 5.0 (low sensitivity) Max: 50.0 (hyper-reactive) / Sensibilité à la dopamine 

# --- ENERGY THRESHOLDS / SEUILS ÉNERGÉTIQUES (FR) ---
# ATP_CRITICAL_THRESHOLD = 0.10      # Transition to REFRACTORY_REST mode Min: 0.05 (very critical) Max: 0.30 (less critical) / Passage en mode REFRACTORY_REST 
ATP_FATIGUE_ZONE = 0.40            # Hypervigilance Trigger Min: 0.30 (rapid fatigue) Max: 0.60 (late fatigue) / Déclenchement de l'hyper-vigilance 
# ATP_CONSUMPTION = 0.001          # Fatigue per cycle Min: 0.001 (endurance) Max: 0.005 (rapid depletion) / Fatigue par cycle
RECOVERY_RATE = 0.05               # ATP Recharge Rate (Sleep) Min: 0.01 (slow recovery) Max: 0.20 (rapid recovery) / Vitesse de recharge ATP (Sommeil)
WAKE_UP_THRESHOLD = 0.80           # Wake-Up Threshold Min: 0.60 (late wake-up) Max: 0.95 (early wake-up) / Seuil de réveil 

# --- PLASTICITY & LEARNING (Hippocampus/Cortex) / PLASTICITÉ & APPRENTISSAGE (Hippocampe/Cortex) (FR) ---
AMPA_BASE_THRESHOLD = 0.15         # Seuil d'activation AMPA (Transmission de base) Min: 0.05 (Extreme sensitivity) Max: 0.30 (Must be strong to be heard) / Seuil d'activation AMPA
# THRESHOLD_NMDA = 0.65              # Memory Lock Threshold (NMDA, "Magnesium ion") Min: 0.1 (Easy learning/credulous) Max: 0.9 (Difficult/critical learning) / Seuil pour le verrouillage des souvenirs 
LTP_GAIN_FACTOR = 0.25             # Facteur de renforcement (LTP) Min: 0.05 (Slow plasticity) Max: 0.50 (Ultra-fast/unstable plasticity) / Seuil d'activation AMPA
ATP_CRITICAL_MIN = 0.20            # Parameter for the future "NMDA_Lock" Min: 0.05 (Extreme Survival) Max: 0.40 (High Energy Caution) / Paramètre pour le futur "NMDA_Lock"
CURRENT_ATP = 1.0                  # Current energy level  Min: 0.00 (...) Max: 0.00 (...) / Niveau d'énergie actuel
ENCODE_THRESHOLD = 0.7             # Energy Required for Encoding Min: 0.1 (Everything is memorized) Max: 1.0 (Nothing is memorized without emotional shock) / Intensité requise pour la mémorisation 
HIPPO_RECOVERY = 0.08              # Hippocampal energy recovery Min: 0.01 (Slow Recovery, Fatigue Quickly) Max: 0.20 (High Cognitive Endurance) / Récupération énergétique de l'Hippocampe 
# SYNAPTIC_PLASTICITY = 0.05         # Baseline learning rate Min: 0.001 (slow learning) Max: 0.10 (fast learning) / Vitesse d'apprentissage de base
# MYELIN_RATE = 0.04               # Pathway strengthening rate Min: 0.001 (slow wiring) Max: 0.05 (fast wiring) / Vitesse de renforcement des chemins 
# MYELIN_EFFICIENCY_COEFF = 1.5      # Richness of the wiring Min: 1.0 (standard) Max: 2.5  (super-conducteur)/ Richesse du câblage 
# CORTICAL_RESONANCE_FACTOR = 0.9    # Prediction persistence  Min: 0.10 (unstable) Max: 0.95 (stable) / Persistance de la prédiction 
BASE_CONDUCTIVITY = 0.7            # Neural flow concept Min: 0.1 (Slow/Viscous Flux) Max: 1.0 (Instantaneous/Fluid Flux) / Concept de flux neuronal 
MIN_RESISTANCE = 0.1               # Minimum synaptic resistance Min: 0.01 (Superconducting Synapses) Max: 0.2 (Always Resistant Synapses) / Résistance synaptique minimale 

# --- SIGNAL & DOPAMINE SETTINGS / RÉGLAGES DES SIGNAUX & DOPAMINE (FR) ---
DOPA_INJECTION_NEW = 0.20          # Surprise (High Dopamine) Min: 0.05 (Little Surprise) Max: 0.50 (Extreme Surprise) / Surprise (Dopamine haute) 
DOPA_INJECTION_KNOWN = 0.05        # Habit (Low Dopamine) Min: 0.01 (Little Dopamine) Max: 0.50 (Moderate Dopamine) / Habitude (Dopamine basse) 
RTN_BASE_INHIBITION = 0.1          # Default Thalamic Silence Level Min: 0.0 (No Inhibition) Max: 0.5 (Strong Inhibition) / Niveau de silence thalamique par défaut 
# NOISE_LEVEL = 0.01                 # Biological Realism (Background Noise) Min: 0.0 (No Noise) Max: 0.10 (A lot of noise; beyond this, the signal becomes unreadable) / Réalisme biologique (Bruit de fond)

# --- THALAMIC & SENSORY PARAMETERS / PARAMÈTRES THALAMIQUES & SENSORIELS (FR) ---
# THALAMIC_THRESHOLD = 0.35          # THALAMIC THRESHOLD (Average human) Min: 0.05 (Anxious) Max: 0.45 (Stoic) / SEUIL THALAMIQUE
THALAMIC_REFRACTORY_PERIOD = 0.05  # RECOVERY TIME Min: 0.01 (Fast) Max: 0.20 (Slow) / TEMPS DE RÉCUPÉRATION

# --- Relative importance of the senses / Importance relative des sens (FR) ---
SENSORY_WEIGHTS = {                # AVERAGE HUMAN (visual priority) Total: 1.0 (Sensory weights) / HUMAIN MOYEN (priorité visuel) 
    "haptic": 0.30,                # Min: 0.10 Max: 0.50 (responsive)
    "visual": 0.80,                # Min: 0.05 Max: 0.80 (visual dominates)
    "auditory": 0.50               # Min: 0.10 Max: 0.60 (attentive to noise)
}

# =============================================================
# PROFILE: NEURAL PERFORMANCE CONFIGURATION
# =============================================================

# --- OPTION A: HIGH-PERFORMING HUMAN (High Plasticity & Focus) ---
# Maximum neuroplasticity, optimal stress management and thalamic focus.
# """
AMYGDALA_SENSITIVITY      = 0.5
L6_GAIN                   = 0.8
SYNAPTIC_PLASTICITY       = 0.05
MYELIN_RATE               = 0.04
MYELIN_EFFICIENCY_COEFF   = 2.0
CORTICAL_RESONANCE_FACTOR = 0.9
THALAMIC_THRESHOLD        = 0.35
THRESHOLD_NMDA            = 0.65
ATP_CRITICAL_THRESHOLD    = 0.10
ATP_CONSUMPTION           = 0.001
NOISE_LEVEL               = 0.01
# """

# --- OPTION B: AVERAGE HUMAN (Standard Baseline) ---
# The default values tested.
"""
AMYGDALA_SENSITIVITY      = 1.0   
L6_GAIN                   = 0.5    
SYNAPTIC_PLASTICITY       = 0.01  
MYELIN_RATE               = 0.03  
MYELIN_EFFICIENCY_COEFF   = 1.5    
CORTICAL_RESONANCE_FACTOR = 0.6   
THALAMIC_THRESHOLD        = 0.15  
THRESHOLD_NMDA            = 0.4    
ATP_CRITICAL_THRESHOLD    = 0.20  
ATP_CONSUMPTION           = 0.003  
NOISE_LEVEL               = 0.02   
"""

# --- OPTION C: TIRED/SATURATED HUMAN (Saturated & Exhausted) ---
# Low ATP, emotional hyper-reactivity, and encoding difficulty.
"""
AMYGDALA_SENSITIVITY      = 1.8    
L6_GAIN                   = 0.2    
SYNAPTIC_PLASTICITY       = 0.002  
MYELIN_RATE               = 0.01   
MYELIN_EFFICIENCY_COEFF   = 1.0    
CORTICAL_RESONANCE_FACTOR = 0.2    
THALAMIC_THRESHOLD        = 0.15  
THRESHOLD_NMDA            = 0.9    
ATP_CRITICAL_THRESHOLD    = 0.30   
ATP_CONSUMPTION           = 0.005 
NOISE_LEVEL               = 0.08   
"""


def get_config():
    """
    Returns the complete configuration for injection into the organs. This function centralizes all the parameters, allowing for easy adjustments and ensuring that all components of the architecture are aligned with the same temperament settings.
    """
    return {
        "AMYGDALA_SENSITIVITY": AMYGDALA_SENSITIVITY,
        "ADRENALINE_RELEASE_FACTOR": ADRENALINE_RELEASE_FACTOR,
        "L6_GAIN": L6_GAIN,
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
        "NOISE_LEVEL": NOISE_LEVEL,
        "MYELIN_EFFICIENCY_COEFF": MYELIN_EFFICIENCY_COEFF,
        "CORTICAL_RESONANCE_FACTOR": CORTICAL_RESONANCE_FACTOR,
        "MYELIN_RATE": MYELIN_RATE,
        "ATP_CONSUMPTION": ATP_CONSUMPTION
    }

# -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -#
#  “For every complex problem, there is a solution that is simple, neat, and wrong.”   #
#  « À chaque problème complexe correspond une solution simple, élégante et fausse. »  #
#                                                                   — H.L. Mencken     #
# -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -#
