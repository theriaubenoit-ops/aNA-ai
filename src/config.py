#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
aNA v5.1 - Configuration Module
Keep the default values ​​to ensure architecture stability.
Temperature parameters can be adjusted for experimentation.

aNA v5.1 - Configuration Module (FR)
Conservez les valeurs par défaut pour garantir la stabilité de l'architecture.
Les paramètres de tempérament peuvent être ajustés pour des expérimentations.
"""

# --- Valeurs par défaut (Ne pas modifier) ---
DEFAULT_AMYGDALA_SENSITIVITY = 1.0
DEFAULT_ADRENALINE_RELEASE_FACTOR = 0.5

# --- Paramètres actifs (Modifiables pour expérimentation) ---
# Vous pouvez modifier ces valeurs pour changer le tempérament de l'IA.
# Si vous voulez revenir à la normale, recopiez les valeurs par défaut.

AMYGDALA_SENSITIVITY = 1.0          # Personnalité actuelle
ADRENALINE_RELEASE_FACTOR = 0.4     # Personnalité actuelle

# --- Aide à la configuration ---
"""
Profils suggérés :
- "Nerveux"    : AMYGDALA_SENSITIVITY = 0.3, ADRENALINE_RELEASE_FACTOR = 0.8
- "Calme"      : AMYGDALA_SENSITIVITY = 1.5, ADRENALINE_RELEASE_FACTOR = 0.2
- "Perfectionniste": AMYGDALA_SENSITIVITY = 1.0, ADRENALINE_RELEASE_FACTOR = 0.4
"""

# --- Paramètres v5.9 (Ajoutés pour la boucle L6-Thalamus) ---
L6_GAIN = 1.2            # Force du frein cortical
THRESHOLD_NMDA = 0.4    # Seuil de plasticité
MYELIN_RATE = 0.01      # Vitesse de câblage

def get_config():
    """Retourne la configuration sous forme de dictionnaire pour les organes"""
    return {
        "AMYGDALA_SENSITIVITY": AMYGDALA_SENSITIVITY,
        "ADRENALINE_RELEASE_FACTOR": ADRENALINE_RELEASE_FACTOR,
        "L6_GAIN": L6_GAIN,
        "THRESHOLD_NMDA": THRESHOLD_NMDA,
        "MYELIN_RATE": MYELIN_RATE
    }
