#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""            __
        __    /\ \  __          __
       /\ \  _\.\ \/\ \  __    /\ \
      _\.\ \/\ \.\ \.\ \/\ \  _\.\ \
     /\ \.\ \.\ \.\ \.\ \.\ \/\ \.\ \
     \.\_\.\_\.\_\.\_\.\_\.\_\.\_\.\_\
      \/_/\/_/\/_/\/_/\/_/\/_/\/_/\/_/
        a N A    A I    P e r s o n a 

aNA v5.4 - Configuration Module (Persona & Authentic Alignment)

Description: Centralization of dynamic thresholds for AI customization and authentic alignment. This module defines the adjustable parameters that shape the AI's persona, temperament, and responsiveness. It ensures an "Authentic Alignment" between the user's vision and the AI's homeostatic behavior. By modifying these values, the system's reactions are synchronized with biological realism, allowing for a personalized and ethically grounded experience without compromising the architecture's integrity.

Description (FR) : Centralisation des seuils dynamiques pour la personnalisation et l'alignement authentique. Ce module définit les paramètres ajustables qui déterminent la Persona, le tempérament et la réactivité de l'IA. Il assure un « Alignement Authentique » entre la vision de l'utilisateur et le comportement homéostatique de l'IA. En modifiant ces valeurs, les réactions du système sont synchronisées avec le réalisme biologique, permettant un alignement fonctionnel et une expérience personnalisée sans compromettre l'intégrité de l'architecture.

Architecture, concept and supervision: Theriault Benoit
Collaboration, research and code: Google DeepMind (Gemini)
"""

import os
import sys
import json

# -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
# -  TEMPERAMENT SELECTOR / SÉLECTEUR DE TEMPERAMENT (FR)  -
# -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
# This section allows users to select a predefined temperament profile, which adjusts the AI's parameters to create different behavioral tendencies.
# Cette section permet aux utilisateurs de sélectionner un profil de tempérament prédéfini, qui ajuste les paramètres de l'IA pour créer différentes tendances comportementales.
ACTIVE_PROFILE = "LEARNING_memorization"

PROFILES = {
    "LEARNING_memorization": { # Apprentissage (mémorisation)
        "title": "The Sponge (Learning and Consolidation)",
        "AMYGDALA_SENSITIVITY": 0.3,
        "THALAMIC_THRESHOLD": 0.45,
        "ATP_CONSUMPTION": 0.001,
        "THRESHOLD_NMDA": 0.08,
        "MYELIN_EFFICIENCY_COEFF": 2.5,
        "BASE_BPM": 62.0,
        "MAX_BPM": 112.0
    },
    "ANALYSIS_reflection": {   # Analyse (réflexion)
        "title": "The Thinker (Problem Solving)",
        "AMYGDALA_SENSITIVITY": 0.8,
        "THALAMIC_THRESHOLD": 0.25,
        "ATP_CONSUMPTION": 0.003,
        "THRESHOLD_NMDA": 0.15,
        "MYELIN_EFFICIENCY_COEFF": 1.8,
        "BASE_BPM": 72.0,
        "MAX_BPM": 124.0
    },
    "RESEARCH_curiosity": {    # Recherche (curiosité)
        "title": "The Explorer (Innovation and Survival)",
        "AMYGDALA_SENSITIVITY": 1.8,
        "THALAMIC_THRESHOLD": 0.05, # test min  0.1
        "ATP_CONSUMPTION": 0.006,
        "THRESHOLD_NMDA": 0.40,
        "MYELIN_EFFICIENCY_COEFF": 1.2,
        "BASE_BPM": 85.0,
        "MAX_BPM": 136.0  
    },
    "REST_meditation": {       # Repos (méditation)
        "title": "Active Maintenance (Recovery)",
        "AMYGDALA_SENSITIVITY": 0.1,
        "THALAMIC_THRESHOLD": 0.80, 
        "ATP_CONSUMPTION": -0.05,
        "THRESHOLD_NMDA": 0.70,
        "MYELIN_EFFICIENCY_COEFF": 1.0,
        "BASE_BPM": 55.0,
        "MAX_BPM": 108.0
    },
    "VOID_spare": {            # Espace libre
        "title": "Open profile (Future expansion)",
        # Reserved for future development / Réservé pour une évolution ultérieure
    }
}
selected = PROFILES[ACTIVE_PROFILE]
AMYGDALA_SENSITIVITY      = selected["AMYGDALA_SENSITIVITY"]
THALAMIC_THRESHOLD        = selected["THALAMIC_THRESHOLD"]
ATP_CONSUMPTION           = selected["ATP_CONSUMPTION"]
THRESHOLD_NMDA            = selected["THRESHOLD_NMDA"]
MYELIN_EFFICIENCY_COEFF   = selected["MYELIN_EFFICIENCY_COEFF"]
BASE_BPM                  = selected["BASE_BPM"]
MAX_BPM                   = selected["MAX_BPM"]

# -  -  -  -  -  -  -  -  -  -  -  -  -  -   ARCHITECTURAL MANIFESTO / MANIFESTE ARCHITECTURAL (FR)  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  
# -  "The inclusion of these specific biological modules is not a stylistic choice, but a mechanical necessity.                                -
# -   Their presence is vital for systemic function, coherent learning, and the emergence of a truly grounded World Model."                    -
# - « L'inclusion de ces modules biologiques précis n'est pas un choix esthétique, mais une nécessité mécanique. Leur présence est             -
# -   vitale au fonctionnement systémique, à l'apprentissage cohérent et à l'émergence d'un Modèle du Monde (World Model) réellement ancré. »  -
# -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

# -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
# -  METABOLISM and CIRCADIAN (The survival instinct) / METABOLISM & CIRCADIAN (L'instinct de survie, FR)  -
# -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
# Homeostasis (Without energy, no cognition) / Homéostasie (Sans énergie, aucune cognition)
CURRENT_ATP = 1.0                  # Current energy level (100%) Min: 0.15 (Survival Threshold) Default: 1.0 Max: 1.20 (Hyper-Vigilance) / Niveau d'énergie actuel (100%)
# ATP_CONSUMPTION = 0.001            # Fatigue per cycle Min: 0.001 (endurance) Default: 0.001 Max: 0.005 (rapid depletion) / Fatigue par cycle
ATP_RECOVERY_RATE = 0.10           # Energy restoration rate per cycle. Min: 0.05 (slow) Default: 0.10 Max: 0.30 (fast) / Vitesse de restauration de l'énergie par cycle
HIPPO_RECOVERY = 0.08              # Hippocampal energy recovery Min: 0.01 (Slow, Fatigue Quickly) Default: 0.08 Max: 0.20 (High Cognitive Endurance) / Récupération énergétique de l'Hippocampe 
ATP_FATIGUE_ZONE = 0.40            # Hypervigilance Trigger Min: 0.30 (rapid fatigue) Mid: (0.15 and 0.40) Max: 0.60 (late fatigue) / Déclenchement de l'hyper-vigilance 
ATP_CRITICAL_THRESHOLD = 0.10      # Transition to REFRACTORY_REST mode Min: 0.05 (very critical) Default: 0.10 Max: 0.30 (less critical) / Passage en mode REFRACTORY_REST 
ATP_CRITICAL_MIN = 0.20            # NMDA locking safety threshold Min: 0.05 (Extreme Survival) Default: 0.20 Max: 0.40 (High Energy Caution) / Seuil de sécurité pour le verrouillage NMDA

# Circadian rhythm (Maintenance cycles) / Rythme circadien (cycles de maintenance)
CIRCADIAN_SLEEP_START = 23         # Beginning of the consolidation phase Min: 0 Default: 22 Max: 23 h / Début de la phase de consolidation
CIRCADIAN_SLEEP_END = 7            # End of the consolidation phase Min: 0 Default: 6 Max: 23 h / Fin de la phase de consolidation
WAKE_UP_THRESHOLD = 0.80           # Vigilance required for wakefulness Min: 0.60 (late) Default: 0.80 Max: 0.95 (early) / Vigilance requise pour l'éveil

# -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
# -  THE THALAMIC GATE (The Sensory Gatekeeper) / THE THALAMIC GATE (Le portier sensoriel, FR) -
# -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
# Consciousness and heart rate (BPM) / La conscience et le rythme cardiaque (BPM)
BASE_SYNAPTIC_LATENCY = 0.5        # Basic neuronal response time Min: 0.1 (fast) Default: 0.5 Max: 2.0 s (slow) / Temps de réponse neuronal de base
RTN_BASE_INHIBITION = 0.1          # Default Thalamic Silence Level Min: 0.0 (No Inhibition) Default: 0.1 Max: 0.5 (Strong Inhibition) / Niveau de silence thalamique par défaut 
THALAMIC_REFRACTORY_PERIOD = 0.05  # Goalkeeper recovery time Min: 0.01 (Fast) Default: 0.05 Max: 0.20 (Slow) / Temps de récupération du portier
LOW_POWER_THRESHOLD = 0.30         # Triggering of synaptic bridle Min: 0.15 Default: 0.30 (resilient) Max: 0.50 (sensitive) / Déclenchement du bridage synaptique

# Cardiac parameters (Pulse) / Paramètres cardiaques (pulsation)
PULSE_FRICTION = 0.93              # Heart rate damping Min: 0.80 (unstable) Default: 0.93 Max: 0.99 (ultra-stable) / Amortissement du rythme cardiaque 
DOPA_TO_HZ_GAIN = 20.0             # Dopamine sensitivity Min: 5.0 (low sensitivity) Default: 20.0 Max: 50.0 (hyper-reactive) / Sensibilité à la dopamine 
# BASE_BPM = 65.0                    # Resting rhythm (Homeostatic target) Min: 60.0 (deep sleep) Default: 65.0 Max: 100.0 (alert) / Rythme de repos (Cible homéostatique) 
# MAX_BPM = 136.0                    # Ceiling of emotional reactivity Min: 100.0 (little emotional reactivity) Default: 136.0 Max: 170.0 (alert) / Plafond de réactivité émotionnelle
CRITICAL_VIGILANCE_BPM = 200.0     # --> À INTÉGRER - Survival limit (Maximum alert) Min: 122 Default: 200 Max: 200 / Limite de survie (Alerte maximale)
BRADYCARDIA_BPM = 45.0             # Nighttime protection rhythm Min: 45.0 (bradycardia) Default: 45.0 Max: 60.0 (resting rate) / Rythme de protection nocturne
RECOGNITION_METABOLIC_DROP = 6.0   # Target BPM reduction upon pattern match (no savings) Default: 6.0 Max: 10.0 (high efficiency) / Une reconnaissance réduit le BPM cible

# THALAMIC OSCILLATION (Cognitive speed) / THALAMIC OSCILLATION (La vitesse cognitive)
THALAMUS_VIGILANCE_FACTOR = 0.72   # Basic attention span (%) Min: 1 Default: 72 Max: 100 / Capacité d'attention de base (%)
THALAMUS_DECAY_FACTOR = 0.15       # Goalkeeper's return-to-balance (%) Min: 0.1 (slow) Default: 0.15 Max 0.5 (fast) / Vitesse de retour à l'équilibre du portier (%)
# THALAMIC_THRESHOLD = 0.35          # Filtering threshold (related to the Persona, %) Min: 0.05 (Anxious) Default: 0.35 Max: 0.45 (Stoic) / Seuil de filtrage (lié à la Persona, %)

SENSORY_WEIGHTS = {                # Sensory priorities Total: 1.0 / Priorités sensorielles
    "haptic": 0.40,                # Min: 0.10 Default: 0.40 Max: 0.50 (responsive)
    "visual": 0.80,                # Min: 0.05 Default: 0.80 Max: 0.80 (visual dominates)
    "auditory": 0.50               # Min: 0.10 Default: 0.50 Max: 0.60 (attentive to noise)
}

# -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
# - CORTICAL LAYERS & ATTENTION (The treatment) / CORTICAL LAYERS & ATTENTION (Le traitement, FR) -
# -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
# Defines the effectiveness of the "Thalamo-Cortical Bridge" / Définit l'efficacité du « pont thalamo-cortical »
BIOLOGICAL_ACCURACY_TARGET = 0.65  # Target for biological realism (0.0 to 1.0) Min: 0.0 (abstract) Default: 0.65 Max: 1.0 (fully biological) / Cible pour le réalisme biologique (0.0 à 1.0)
TRAUMA_NORA_THRESHOLD = 0.6        # Trauma Threshold for Noradrenaline Min: 0.1 (low trauma) Default: 0.6 Max: 0.9 (high trauma) / Seuil de traumatisme pour la noradrénaline
# AMYGDALA_SENSITIVITY = 0.5         # Emotional reactivity Min: 0.1 (unperturbed) Default: 0.5 Max: 2.0 (hyper-reactive) / Réactivité émotionnelle
ADRENALINE_RELEASE_FACTOR = 0.4    # Intensity of the stress response Min: 0.1 (calm) Default: 0.4 Max: 1.0 (explosive) / Intensité de la réponse au stress

# Diaper effectiveness & Caution / Efficacité des couches & Attention 
L4_EFFICIENCY = 0.90               # Layer IV Efficiency Min: 0.1 (inefficient) Default: 0.90 Max: 0.99 (ultra-efficient) / Efficacité de la couche IV (réception thalamique)
L23_EFFICIENCY = 0.85              # Layer II/III Efficiency Min: 0.1 (inefficient) Default: 0.85 Max: 0.99 (ultra-efficient) / Efficacité des couches II/III (intégration corticale)
L5_EFFICIENCY = 0.85               # Layer V Efficiency Min: 0.1 (inefficient) Default: 0.85 Max: 0.99 (ultra-efficient) / Efficacité de la couche V (commande motrice)
L6_EFFICIENCY = 0.80               # Layer VI Efficiency Min: 0.1 (inefficient) Default: 0.80 Max: 0.99 (ultra-efficient) / Efficacité de la couche VI (rétroaction corticale)
L6_GAIN = 0.8                      # Cortical Brake Strength Min: 0.0 (no brake) Default: 0.8 Max: 2.0 (total inhibition) / Force du frein cortical 
CORTICAL_RESONANCE_FACTOR = 0.9    # Prediction persistence  Min: 0.10 (unstable) Default: 0.9 Max: 0.95 (stable) / Persistance de la prédiction 
ACH_ATTENTION_MULTIPLIER = 1.5     # Acetylcholine Attention Multiplier Min: 0.5 (distracted) Default: 1.5 Max: 2.0 (hyper-focused) / Multiplicateur d'attention à l'acétylcholine
ATTENTION_MIN_GAIN = 0.01          # Minimum attention gain Min: 0.01 (distracted) Default: 0.01 Max: 0.10 (always attentive) / Gain d'attention minimum

# -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -   -  -  -  -  -  -  -  -
# -  PLASTICITY & RESONANCE (Memory) / PLASTICITÉ ET RÉSONANCE (Mémoire, FR)  -
# -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -   -  -  -  -  -  -  -  -
# Memory repair and the strengthening of pathways / Suture mémorielle et le renforcement des chemins
SYNAPTIC_PLASTICITY = 0.05         # Baseline learning rate Min: 0.001 (slow learning) Default: 0.05 Max: 0.10 (fast learning) / Vitesse d'apprentissage de base
# THRESHOLD_NMDA = 0.1              # Memory Lock Threshold (NMDA, "Magnesium ion") Min: 0.1 (Easy learning/credulous) Default: 0.65 Max: 0.9 (Difficult/critical learning) / Seuil pour le verrouillage des souvenirs 
AMPA_BASE_THRESHOLD = 0.15         # Activation threshold AMPA (Basic transmission) Min: 0.05 (Extreme sensitivity) Default: 0.15 Max: 0.30 (Must be strong to be heard) / Seuil d'activation AMPA
LTP_GAIN_FACTOR = 0.25             # Facteur de renforcement (LTP) Min: 0.05 (Slow plasticity) Default: 0.25 Max: 0.50 (Ultra-fast/unstable plasticity) / Seuil d'activation AMPA
ENCODE_THRESHOLD = 0.7             # Energy Required for Encoding Min: 0.1 (Everything is memorized) Default: 0.7 Max: 1.0 (Nothing is memorized without emotional shock) / Intensité requise pour la mémorisation 

# Myelination and Conductivity / La Myélinisation et Conductivité 
MYELIN_RATE = 0.04                 # Pathway strengthening rate Min: 0.001 (slow wiring) Default: 0.04 Max: 0.05 (fast wiring) / Vitesse de renforcement des chemins 
FLASH_MYELIN_BOOST = 0.05          # Myelin boost during flash engraving Min: 0.01 (subtle) Default: 0.05 Max: 0.10 (dramatic) / Boost de myéline lors de la gravure flash
# MYELIN_EFFICIENCY_COEFF = 2.0      # Richness of the wiring Min: 1.0 (standard) Default: 2.0 Max: 2.5 (super-conducteur)/ Richesse du câblage 
MAX_MYELIN_DENSITY = 1.0           # Maximum synaptic insulation. Min: 0.1 (raw fiber) Default: 1.0 Max: 1.0 (fully myelinated) / Densité maximale de myéline (isolation synaptique)
BASE_CONDUCTIVITY = 0.7            # Neural flow concept Min: 0.1 (Slow/Viscous Flux) Default: 0.7 Max: 1.0 (Instantaneous/Fluid Flux) / Concept de flux neuronal 
MIN_RESISTANCE = 0.1               # Minimum synaptic resistance Min: 0.01 (Superconducting Synapses) Default: 0.1 Max: 0.2 (Always Resistant Synapses) / Résistance synaptique minimale 
RESONANCE_GAIN = 0.20              # Memory amplification gain during an alpha interaction Min: 0.05 (subtle) Default: 0.20 Max: 0.50 (intense) / Gain d'amplification mémorielle lors d'une interaction Alpha
NEURON_PLASTICITY_DECAY = 0.9999   # Plasticity decay per cycle Min: 0.90 (rapid forgetting) Default: 0.9999 Max: 0.9999 (long-term retention) / Décay de la plasticité par cycle

# -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
# -  CHEMICAL CORE (Limbic & Signals) / NOYAU CHIMIQUE (Système limbique et signaux, FR) -
# -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
# Factors influencing emotions / Facteurs d'influence émotionnelle
DOPA_INJECTION_NEW = 0.20          # Surprise (High Dopamine) Min: 0.05 (Little Surprise) Default: 0.20 Max: 0.50 (Extreme Surprise) / Surprise (Dopamine haute) 
DOPA_INJECTION_KNOWN = 0.05        # Habit (Low Dopamine) Min: 0.01 (Little Dopamine) Default: 00.05 Max: 0.50 (Moderate Dopamine) / Habitude (Dopamine basse) 
NOISE_LEVEL = 0.01                 # Biological Realism (Background Noise) Min: 0.0 (No Noise) Default: 0.01 Max: 0.10 (A lot of noise; beyond this, the signal becomes unreadable) / Réalisme biologique (Bruit de fond)

def get_config():
    """
    Returns the complete configuration for injection into the organs 
    Retourne la configuration complète pour injection dans les organes (FR)
    """
    return {k: v for k, v in globals().items() if k.isupper()}

# -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
# -   “For every complex problem, there is a solution that is simple, neat, and wrong.”  -
# -  « À chaque problème complexe correspond une solution simple, élégante et fausse. »  -
# -                                                                  — H.L. Mencken      -
# -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
