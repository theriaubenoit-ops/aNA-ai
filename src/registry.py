#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
            ___    __      __ 
       ___ /\  .`./\ \   /\  _`\         A I   i n s p i r e d   b y
     /´ __`\ \ \`.`.\ \ \ \ \/_\`\       n a t u r a l   p l a s t i c i t y
    /\ \/_\ \ \ \.`.`\ \` \ .____.`\.
    \ \___/\_\ \_\`.`. _\ \_\____/`\_\   A u t o n o m o u s   N e u r a l
     \/__/\/_/\/_/  `./_/\/_/    `\/_/   A r c h i t e c t u r e

aNA v5.4 - The Centralized Genome of aNA / aNA v5.4 - Le Génome Centralisé d'aNA (FR)
Description: This module acts as the organism's genetic fingerprint. It catalogs and initializes all the "Organs" (Thalamus, Hippocampus, Cortex), enabling consistent instantiation and seamless communication between subcortical and cortical systems. Without this registry, the organism loses its unified structure and its ability to maintain global homeostasis.

Description (FR) :  Ce module agit comme l'empreinte génétique de l'organisme. Il répertorie et initialise l'ensemble des "Organes" (Thalamus, Hippocampe, Cortex) permettant une instanciation cohérente et une communication fluide entre les systèmes subcorticaux et corticaux. Sans ce registre, l'organisme perd sa structure unifiée et sa capacité à maintenir une homéostasie globale.

Architecture, concept and supervision: Theriault_Benoit
Collaboration, research and code: DeepMind_Gemini
"""

# - - - - - - - - - - - - - ARCHITECTURAL MANIFESTO / MANIFESTE ARCHITECTURAL (FR)  - - - - - - - - - - - - - - +
#  "The inclusion of these specific biological modules is not a stylistic choice, but a mechanical necessity.   +
#   Their presence is vital for systemic function, coherent learning, and the emergence of a truly grounded     +
#   World Model."                                                                                               +
#                                                                                                               +
#  "L'inclusion de ces modules biologiques précis n'est pas un choix esthétique, mais une nécessité mécanique.  +
#   Leur présence est vitale au fonctionnement systémique, à l'apprentissage cohérent et à l'émergence          +
#   d'un Modèle du Monde (World Model) réellement ancré."                                                       +
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - +

# - - HEART CONFIGURATION / CONFIGURATION DU CŒUR (FR) - - +
"""
The SensoryPayload is not a string; it is a sample of physical reality captured for integration into the internal World Model.
"""
INPUT_CONFIG = {
    "UNICODE_NORM": 1114111.0,  # Unicode ceiling (Mathematics, not temperament)
    "DEFAULT_NUCLEUS": "MGN", # By default, symbolic inputs are processed by the MGN nucleus of the Thalamus, which is specialized in complex and modular signals.
    "GATEWAY_READY": True, # Indicates that the input system is operational and ready to process sensory data.
    "DEFAULT_GAIN": 1.0 # Default signal gain for processed inputs, adjustable based on vigilance and metabolic state.
}

# - - CENTRAL ORGAN REGISTRY / REGISTRE CENTRAL DES ORGANES (FR) - - +
"""
This registry defines the core organs of aNA and their key properties. It serves as the blueprint for the architecture, ensuring that all components are aligned and can communicate effectively. The Thalamus, Hippocampus, and Neocortex are defined with their respective substructures, which will be used to guide the development of each module and their interactions.
"""
ORGANS = {
    "THALAMIC_HUB": {
        "NAME": "Thalamic Hub",
        "DESCRIPTION": "Multimodal sensory integrator and attentional gate.",
        "NUCLEI": ["VPL", "CGL", "CGM"],
        "METHODS": ["route_signal", "process_incoming"] 
    },
    "THALAMUS": { # The Thalamus adjusts the BPM according to the gap between the internal prediction and the sensory reality, thus simulating the understanding of the consequences.
        "NUCLEI": ["MGN", "LGN", "MD", "RTN"] # MGN (Medial, Unicode), LGN (Lateral), MD (Mediodorsal) and RTN (Reticulated, Inhibitor "barrier guard").
    },
    "HIPPOCAMPUS": { # The Hippocampus uses the sequence_map to generate spatio-temporal predictions, reducing metabolic surprise (Vigilance) in the face of a stable environment.
        "SUBFIELDS": ["DG", "CA3", "CA1", "CA2", "CA4"]
    },
    "NEOCORTEX": { # The Neocortex, through its layered architecture, refines the sensory input and integrates it with the internal model, allowing for recognition and learning.
        "LOBES": ["OCCIPITAL", "TEMPORAL", "PARIETAL", "FRONTAL"], # Each lobe has a specific role in processing different types of information (visual, auditory, somatosensory, executive functions).
        "INSTANCES": {}, # This will hold the instantiated cortical columns for each lobe, allowing for modular growth and specialization.
        "LAYERS": ["L1", "L2", "L3", "L4", "L5", "L6"], # The layers of the cortex, each with distinct connectivity and functions, are crucial for the hierarchical processing of information and the generation of predictions.
        "UNIT": "CORTICAL_COLUMN", # The fundamental processing unit of the Neocortex is the Cortical Column, which contains a microcircuitry of neurons 
        "NEURONS_PER_COLUMN": 1000, # Each cortical column contains neurons, which is a simplified representation of the complex microcircuitry found in the biological cortex.
        "DESCRIPTION": "Hierarchical structure enabling real-time internal world representation."
    },
    "SUBKORTICAL_SYSTEMS": { 
        "STRIATUM": {
            "NAME": "The Action Selector",
            "FUNCTION": "Gating and Action Selection",
            "INPUTS": ["CorticalL5", "LimbicDopamine"],
            "OUTPUTS": ["Thalamic_RTN_Inhibition", "MotorControl"],
            "DESCRIPTION": "Arbitrates between cortical intents based on emotional value and ATP cost."
        },
        "LIMBIC_SYSTEM": {
            "AMYGDALA": {"FUNCTION": "Emotional Pulse & Threat Assessment"},
            "HIPPOCAMPUS": "Initialized via separate registry"
        },
        "CEREBELLUM": {
            "FUNCTION": "Fine-tuning & Motor-cognitive coordination"
        },
    },
    "MICRO_ARCHITECTURE": {
        "NEUROMODULATORS": ["ACETYLCHOLINE", "ADRENALINE", "CORTISOL", "DOPAMINE", "NO_GAS", "NORADRENALINE", "SEROTONIN"], 
        "UNIT": "NEURON",
        "PROPERTIES": ["Resistance", "Conductivity", "Voltage_Threshold"],
        "TYPES": {
            "SENSORY": { 
                "DESCRIPTION": "Transduction of physical reality into neural signals",
                "STREAMS": {
                    "HAPTIC": "Processed via Unicode Wide mapping (input_haptic.py)",
                    "VISUAL": "Processed via Occipital Lobe mapping (input_visual.py)",
                    "AUDITORY": "Processed via Temporal Lobe mapping (input_auditory.py)"
                }
            },
            "INTERNEURON": "Local processing and inhibitory regulation (GABAergic simulation).",
            "MOTOR": "Output generation and homeostatic adjustment (BPM/ATP control)." 
        }
    }
}    

# - - STANDARDIZED SIGNALS / SIGNALS STANDARDISÉS (FR) - - +
"""
COMMON LANGUAGE / LANGAGE COMMUN :
These dictionaries act as the genetic standard for all organs. 
- SIGNALS: Real-time dynamic flow (What is happening).
- PROPERTIES: Structural state of the units (How they are built).
- PROTOCOLS: Communication and routing formats (Where it goes).
- METRICS: Comparative values for homeostasis (How the system feels).
"""
SIGNALS = {
    "SENSORY": "input_raw",                # Raw signal from sensory organs
    "METABOLIC": "atp_flux",               # Energy state (ATP), influences alertness
    "EMOTIONAL": "amygdala_pulse",         # Limbic modulation (Fear/Excitement/Effort)
    "STRESS": "cortisol_level",            # Cortisol level (stress)
    "REWARD": "dopamine_flux",             # Dopamine flux (reward)
    "SURVIVAL_DRIVE": "atp_deficit_ratio", # Metabolic "Hunger"
    "CURIOSITY_GAIN": "cholinergic_boost"  # Interest in the new
}
PROPERTIES = {
    "PLASTICITY": "nmda_threshold",    # Critical learning threshold (LTP)
    "STRUCTURE": "myelination_level",  # Level of insulation and physical efficiency
    "FLOW": "conductivity",            # Intrinsic signal transmission capacity
    "ELECTRICAL": "membrane_potential" # Membrane potential (electrical)
}
PROTOCOLS = {
    "L4_FORMAT": "L4_INPUT_{nucleus}_{data}" # Thalamo-Cortical routing protocol
}
METRICS = {
    "PREDICTIVE": "expectation_match",      # Reality gap vs Prediction (Surprise/Habit)
    "VITALITY": "atp_reserve",              # Hepatic ATP reserve (vitality)
    "VITALITY_INDEX": "atp_vs_effort_cost", # Survival/Action Ratio
    "SATIETY": "resource_stability"         # Resting state reached
}

#
#  “For every complex problem, there is a solution that is simple, neat, and wrong.”  
#  « À chaque problème complexe correspond une solution simple, élégante et fausse. » 
#                                                                   — H.L. Mencken    

