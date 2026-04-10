#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
aNA v5.2 - The Centralized Genome of aNA
Description: This module acts as the organism's genetic fingerprint. It catalogs and initializes all the "Organs" (Thalamus, Hippocampus, Cortex), enabling consistent instantiation and seamless communication between subcortical and cortical systems. Without this registry, the organism loses its unified structure and its ability to maintain global homeostasis.

aNA v5.2 - Le Génome Centralisé d'aNA (FR)
Description :  Ce module agit comme l'empreinte génétique de l'organisme. Il répertorie et initialise l'ensemble des "Organes" (Thalamus, Hippocampe, Cortex) permettant une instanciation cohérente et une communication fluide entre les systèmes subcorticaux et corticaux. Sans ce registre, l'organisme perd sa structure unifiée et sa capacité à maintenir une homéostasie globale.
"""

# --- CONFIGURATION DU CŒUR ---
"""
The SensoryPayload is not a string; it is a sample of physical reality captured for integration into the internal World Model.
"""
INPUT_CONFIG = {
    "UNICODE_NORM": 1114111.0,  # Plafond Unicode (Mathématique, pas tempérament)
    "DEFAULT_NUCLEUS": "MGN",
    "GATEWAY_READY": True, # added
    "DEFAULT_GAIN": 1.0 # added
}

# --- REGISTRE CENTRAL DES ORGANES ---
"""
The Thalamus adjusts the BPM according to the gap between the internal prediction and the sensory reality, thus simulating the understanding of the consequences.
The Hippocampus uses the sequence_map to generate spatio-temporal predictions, reducing metabolic surprise (Vigilance) in the face of a stable environment.
The Neocortex, through its layered architecture, refines the sensory input and integrates it with the internal model, allowing for recognition and learning. The L4 layer processes the raw sensory data, while L2/3 and L6 layers handle the feedback and feedforward loops that enable the organism to adapt its internal state in real-time.
"""
ORGANS = {
    "THALAMUS": {
        "NUCLEI": ["MGN", "LGN", "MD", "RTN"]
    },
    "HIPPOCAMPUS": {
        "SUBFIELDS": ["DG", "CA3", "CA1", "CA2", "CA4"]
    },
    "NEOCORTEX": {
        "LOBES": ["OCCIPITAL", "TEMPORAL", "PARIETAL", "FRONTAL"]
    }
}

# --- SIGNALS STANDARDISÉS ---
"""
These signals are the common language for all organs. They ensure that the Thalamus, Hippocampus, and Cortex can communicate effectively, even as we evolve the architecture. The SIGNALS dictionary defines the standard labels for sensory input, predictive feedback, metabolic state, and emotional modulation, which are crucial for maintaining homeostasis and enabling learning in aNA.
"""
SIGNALS = {
    "SENSORY": "input_raw", # added
    "PREDICTIVE": "expectation_match", # added
    "METABOLIC": "atp_flux", # added
    "EMOTIONAL": "amygdala_pulse", # added
    "L4_FORMAT": "L4_INPUT_{nucleus}_{data}"  # added   # Résistance synaptique minimale
}
