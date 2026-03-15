#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
aNA v5.0 - Configuration Module
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
ADRENALINE_RELEASE_FACTOR = 0.5     # Personnalité actuelle

# --- Aide à la configuration ---
"""
Profils suggérés :
- "Nerveux"    : AMYGDALA_SENSITIVITY = 0.3, ADRENALINE_RELEASE_FACTOR = 0.8
- "Calme"      : AMYGDALA_SENSITIVITY = 1.5, ADRENALINE_RELEASE_FACTOR = 0.2
- "Perfectionniste": AMYGDALA_SENSITIVITY = 1.0, ADRENALINE_RELEASE_FACTOR = 0.4
"""