#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
aNA v5.1 - The Centralized Genome of aNA
Description: This module acts as the organism's genetic fingerprint. It catalogs and initializes all the "Organs" (Thalamus, Hippocampus, Cortex), enabling consistent instantiation and seamless communication between subcortical and cortical systems. Without this registry, the organism loses its unified structure and its ability to maintain global homeostasis.

aNA v5.1 - Le Génome Centralisé d'aNA (FR)
Description :  Ce module agit comme l'empreinte génétique de l'organisme. Il répertorie et initialise l'ensemble des "Organes" (Thalamus, Hippocampe, Cortex) permettant une instanciation cohérente et une communication fluide entre les systèmes subcorticaux et corticaux. Sans ce registre, l'organisme perd sa structure unifiée et sa capacité à maintenir une homéostasie globale.
"""

# --- CONFIGURATION DU CŒUR ---
INPUT_CONFIG = {
    "UNICODE_NORM": 1114111.0,  # Plafond Unicode (Mathématique, pas tempérament)
    "DEFAULT_NUCLEUS": "MGN"
}

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
