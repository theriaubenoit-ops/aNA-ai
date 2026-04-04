#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Amygdala implementation for aNA v5.1

Communicates with: Input: (<- Thalamus / Cortex) | Output: (-> Pulse / Adrenaline) (-> Hippocampus)

This module implements the Amygdala with its key nuclei (BLA, CEA, MEA) for emotional processing, fear learning, and social behavior. It integrates with the ChemicalCore for neuromodulatory influences, particularly dopamine (Motivation), norepinephrine (Stress), and serotonin (Mood). The Amygdala processes sensory and emotional inputs to modulate memory persistence in the Hippocampus and orchestrate fear responses via the Central Amygdala.

Architecture, concept and supervision: Benoit Theriault
Collaboration, research and code: Gemini
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

from anatomy.base.neuron import Neuron, NeuronConfig

class AmygdalaNucleus(Enum):
    """Amygdala nuclei"""
    BLA = "BLA"           # Basolateral Amygdala - fear learning
    CEA = "CEA"           # Central Amygdala - fear response output
    MEA = "MEA"           # Medial Amygdala - social behavior
    COA = "COA"           # Cortical Amygdala - olfactory processing


@dataclass
class AmygdalaNucleusConfig:
    """Configuration for an amygdala nucleus"""
    nucleus_type: AmygdalaNucleus
    position: np.ndarray
    size: int
    baseline_activity: float = 0.1
    fear_threshold: float = 0.5
    plasticity_rate: float = 1.5


class BasolateralAmygdala:
    """Basolateral Amygdala - fear learning and emotional association"""
    
    def __init__(self, position: np.ndarray, size: int = 400):
        self.position = position
        self.size = size
        self.pyramidal_neurons = []
        self.interneurons = []
        
        self._initialize_neurons()
        self.fear_memory_strength = 0.0
        self.conditioned_stimuli = {}
    
    def _initialize_neurons(self):
        """Initialize BLA neurons"""
        # Pyramidal neurons (principal cells)
        for i in range(self.size):
            x = self.position[0] + np.random.uniform(-10.0, 10.0)
            y = self.position[1] + np.random.uniform(-10.0, 10.0)
            z = self.position[2] + np.random.uniform(-5.0, 5.0)
            
            position = np.array([x, y, z])
            
            config = NeuronConfig(
                layer_id=0,
                threshold_potential=-52.0,
                base_energy_consumption=0.009000000000000001, firing_energy_cost=0.09000000000000001
            )
            neuron = Neuron(position, config)
            self.pyramidal_neurons.append(neuron)
        
        # Interneurons (20% of population)
        interneuron_size = self.size // 5
        for i in range(interneuron_size):
            x = self.position[0] + np.random.uniform(-8.0, 8.0)
            y = self.position[1] + np.random.uniform(-8.0, 8.0)
            z = self.position[2] + np.random.uniform(-3.0, 3.0)
            
            position = np.array([x, y, z])
            
            config = NeuronConfig(
                layer_id=0,
                threshold_potential=-58.0,  # Lower threshold for inhibition
                base_energy_consumption=0.006999999999999999, firing_energy_cost=0.06999999999999999
            )
            neuron = Neuron(position, config)
            self.interneurons.append(neuron)
    
    def process_input(self, sensory_input: float, emotional_valence: float, 
                     neuromodulators: Dict[str, float]):
        """Process sensory and emotional input"""
        # Sensory input drives pyramidal neurons
        for neuron in self.pyramidal_neurons:
            input_signal = sensory_input
            
            # Emotional valence modulates activity
            input_signal *= (1.0 + emotional_valence * 0.5)
            
            # Dopamine enhances fear learning
            if 'dopamine' in neuromodulators:
                input_signal *= (1.0 + neuromodulators['dopamine'] * 0.4)
            
            # Norepinephrine enhances emotional salience
            if 'norepinephrine' in neuromodulators:
                input_signal *= (1.0 + neuromodulators['norepinephrine'] * 0.6)
            
            neuron.receive_input(input_signal, neuromodulators)
            neuron.update(0, neuromodulators)
        
        # Interneurons provide feedback inhibition
        pyramidal_activity = sum(1 for n in self.pyramidal_neurons if n.is_firing) / len(self.pyramidal_neurons)
        
        for neuron in self.interneurons:
            inhibitory_input = pyramidal_activity * 40.0
            neuron.receive_input(inhibitory_input, neuromodulators)
            neuron.update(0, neuromodulators)
    
    def form_fear_memory(self, stimulus: str, strength: float):
        """Form a fear memory association"""
        self.conditioned_stimuli[stimulus] = strength
        self.fear_memory_strength = max(self.fear_memory_strength, strength)
    
    def get_fear_response(self, stimulus: str) -> float:
        """Get fear response to a specific stimulus"""
        if stimulus in self.conditioned_stimuli:
            return self.conditioned_stimuli[stimulus]
        return 0.0
    
    def get_output(self) -> float:
        """Get BLA output to central amygdala"""
        pyramidal_activity = sum(1 for n in self.pyramidal_neurons if n.is_firing) / len(self.pyramidal_neurons)
        inhibition = sum(1 for n in self.interneurons if n.is_firing) / len(self.interneurons)
        
        net_activity = max(0.0, pyramidal_activity - inhibition * 0.3)
        return net_activity * 100.0


class CentralAmygdala:
    """Central Amygdala - fear response output and autonomic control"""
    
    def __init__(self, position: np.ndarray, size: int = 200):
        self.position = position
        self.size = size
        self.output_neurons = []
        self.autonomic_neurons = []
        
        self._initialize_neurons()
        self.fear_threshold = 0.6
        self.autonomic_activation = 0.0
    
    def _initialize_neurons(self):
        """Initialize central amygdala neurons"""
        # Output neurons (to brainstem)
        for i in range(self.size):
            x = self.position[0] + np.random.uniform(-8.0, 8.0)
            y = self.position[1] + np.random.uniform(-8.0, 8.0)
            z = self.position[2] + np.random.uniform(-4.0, 4.0)
            
            position = np.array([x, y, z])
            
            config = NeuronConfig(
                layer_id=0,
                threshold_potential=-50.0,  # Lower threshold for rapid response
                base_energy_consumption=0.008, firing_energy_cost=0.08000000000000002
            )
            neuron = Neuron(position, config)
            self.output_neurons.append(neuron)
        
        # Autonomic neurons (to hypothalamus)
        autonomic_size = self.size // 4
        for i in range(autonomic_size):
            x = self.position[0] + np.random.uniform(-6.0, 6.0)
            y = self.position[1] + np.random.uniform(-6.0, 6.0)
            z = self.position[2] + np.random.uniform(-3.0, 3.0)
            
            position = np.array([x, y, z])
            
            config = NeuronConfig(
                layer_id=0,
                threshold_potential=-55.0,
                base_energy_consumption=0.0075, firing_energy_cost=0.07500000000000001
            )
            neuron = Neuron(position, config)
            self.autonomic_neurons.append(neuron)
    
    def process_input(self, bl_a_input: float, neuromodulators: Dict[str, float]):
        """Process input from BLA"""
        # Output neurons receive BLA input
        for neuron in self.output_neurons:
            input_signal = bl_a_input
            
            # Norepinephrine lowers threshold for fear response
            if 'norepinephrine' in neuromodulators:
                input_signal *= (1.0 + neuromodulators['norepinephrine'] * 0.8)
            
            # Serotonin modulates fear threshold
            if 'serotonin' in neuromodulators:
                # Higher serotonin = higher threshold (anxiolytic effect)
                self.fear_threshold = 0.6 + neuromodulators['serotonin'] * 0.2
            
            neuron.receive_input(input_signal, neuromodulators)
            neuron.update(0, neuromodulators)
        
        # Autonomic neurons get modulated input
        active_output_ratio = sum(1 for n in self.output_neurons if n.is_firing) / len(self.output_neurons)
        
        for neuron in self.autonomic_neurons:
            autonomic_input = active_output_ratio * 60.0
            
            # Stress hormones enhance autonomic response
            if 'norepinephrine' in neuromodulators:
                autonomic_input *= (1.0 + neuromodulators['norepinephrine'] * 0.5)
            
            neuron.receive_input(autonomic_input, neuromodulators)
            neuron.update(0, neuromodulators)
        
        # Update autonomic activation
        autonomic_activity = sum(1 for n in self.autonomic_neurons if n.is_firing) / len(self.autonomic_neurons)
        self.autonomic_activation = autonomic_activity
    
    def get_fear_output(self) -> float:
        """Get fear response output"""
        active_ratio = sum(1 for n in self.output_neurons if n.is_firing) / len(self.output_neurons)
        return active_ratio * 100.0
    
    def get_autonomic_output(self) -> float:
        """Get autonomic nervous system output"""
        return self.autonomic_activation * 100.0


class MedialAmygdala:
    """Medial Amygdala - social behavior and pheromone processing"""
    
    def __init__(self, position: np.ndarray, size: int = 300):
        self.position = position
        self.size = size
        self.social_neurons = []
        
        self._initialize_neurons()
        self.social_memory = {}
    
    def _initialize_neurons(self):
        """Initialize medial amygdala neurons"""
        for i in range(self.size):
            x = self.position[0] + np.random.uniform(-12.0, 12.0)
            y = self.position[1] + np.random.uniform(-12.0, 12.0)
            z = self.position[2] + np.random.uniform(-6.0, 6.0)
            
            position = np.array([x, y, z])
            
            config = NeuronConfig(
                layer_id=0,
                threshold_potential=-53.0,
                base_energy_consumption=0.008, firing_energy_cost=0.08000000000000002
            )
            neuron = Neuron(position, config)
            self.social_neurons.append(neuron)
    
    def process_input(self, social_input: float, neuromodulators: Dict[str, float]):
        """Process social and pheromonal input"""
        for neuron in self.social_neurons:
            input_signal = social_input
            
            # Oxytocin enhances social processing
            if 'oxytocin' in neuromodulators:
                input_signal *= (1.0 + neuromodulators['oxytocin'] * 0.5)
            
            # Vasopressin modulates social recognition
            if 'vasopressin' in neuromodulators:
                input_signal *= (1.0 + neuromodulators['vasopressin'] * 0.3)
            
            # Dopamine modulates social reward
            if 'dopamine' in neuromodulators:
                input_signal *= (1.0 + neuromodulators['dopamine'] * 0.2)
            
            neuron.receive_input(input_signal, neuromodulators)
            neuron.update(0, neuromodulators)
    
    def store_social_memory(self, individual_id: str, valence: float):
        """Store social memory of an individual"""
        self.social_memory[individual_id] = valence
    
    def get_social_response(self, individual_id: str) -> float:
        """Get social response to an individual"""
        if individual_id in self.social_memory:
            return self.social_memory[individual_id]
        return 0.0
    
    def get_output(self) -> float:
        """Get medial amygdala output"""
        active_ratio = sum(1 for n in self.social_neurons if n.is_firing) / len(self.social_neurons)
        return active_ratio * 100.0


class Amygdala:
    """Complete Amygdala with all major nuclei"""
    
    def __init__(self, position: np.ndarray = np.array([-15.0, -25.0, 0.0])):
        self.position = position
        self.bla = None
        self.c_e_a = None
        self.m_e_a = None
        self._internal_activity = 0.0  # Internal activity level for stress response
        
        self._initialize_nuclei()
    
    def _initialize_nuclei(self):
        """Initialize all amygdala nuclei"""
        base_pos = self.position
        
        # Basolateral Amygdala (fear learning)
        bla_pos = base_pos + np.array([-5.0, 5.0, 0.0])
        self.bla = BasolateralAmygdala(bla_pos, size=500)
        
        # Central Amygdala (fear response)
        cea_pos = base_pos + np.array([5.0, 5.0, 0.0])
        self.c_e_a = CentralAmygdala(cea_pos, size=300)
        
        # Medial Amygdala (social behavior)
        mea_pos = base_pos + np.array([0.0, -10.0, 0.0])
        self.m_e_a = MedialAmygdala(mea_pos, size=400)
    
    def process_emotional_input(self, sensory_input: float, emotional_valence: float,
                              social_input: float, neuromodulators: Dict[str, float]):
        """
        Analyse l'entrée et calcule l'impact sur la persistance mémorielle.
        """
        # 1. Basolateral processing (fear learning)
        self.bla.process_input(sensory_input, emotional_valence, neuromodulators)
        
        # 2. Calcul du coefficient de persistance (Impact sur l'Hippocampe)
        # Une valence extrême (très négative ou très positive) doit "verrouiller" la trace
        emotional_impact = abs(emotional_valence)
        
        # 3. Transmission vers le CEA (réponse immédiate)
        bl_a_output = self.bla.get_output()
        self.c_e_a.process_input(bl_a_output, neuromodulators)
        
        # Retourne l'impact pour que l'Hippocampe ajuste son burn_rate
        return emotional_impact, emotional_valence

    def form_emotional_memory(self, stimulus: str, valence: float, type_: str = "fear"):
        """
        Forme une mémoire et définit sa 'résistance' à l'oubli.
        """
        if type_ == "fear":
            # Si la valence est très négative, on sature la trace (Traumatisme)
            strength = abs(valence) * 2.0 if valence < -0.8 else abs(valence)
            self.bla.form_fear_memory(stimulus, strength)
        elif type_ == "social":
            self.m_e_a.store_social_memory(stimulus, valence)
    
    def get_emotional_responses(self) -> Dict[str, float]:
        """Get all emotional responses"""
        return {
            'fear_response': self.c_e_a.get_fear_output(),
            'autonomic_activation': self.c_e_a.get_autonomic_output(),
            'social_response': self.m_e_a.get_output(),
            'bl_a_activity': self.bla.get_output()
        }
    
    def get_fear_threshold(self) -> float:
        """Get current fear response threshold"""
        return self.c_e_a.fear_threshold
    
    def get_activity(self) -> float:
        """Get current amygdala activity level"""
        # Return the internal activity that was updated by update_activity()
        return self._internal_activity
    
    def update_activity(self, stimulus_intensity: float = 0.0):
        """
        Met à jour l'activité avec une distinction nette entre 
        bruit de fond (neutre) et choc (trauma).
        """
        # 1. Gestion du "Cortisol" - Plus de latence pour le neutre
        # On monte le seuil de réaction de 0.1 à 0.4
        if stimulus_intensity > 0.4:
            # Réaction proportionnelle au dépassement du seuil
            gain = (stimulus_intensity - 0.4) * 0.5
            self._internal_activity = min(1.0, self._internal_activity + gain)
        else:
            # Décroissance plus agressive pour "nettoyer" le bruit
            self._internal_activity = max(0.05, self._internal_activity - 0.15)
        
        # 2. Modulation du CEA - ADRENALINE & HOMÉOSTASIE
        if self.c_e_a:
            if stimulus_intensity > 0.7: # Seuil d'alerte critique
                # Seul un choc majeur déclenche l'adrénaline
                self.c_e_a.autonomic_activation = min(1.0, self.c_e_a.autonomic_activation + 0.8)
            else:
                # Recapture massive des neurotransmetteurs si < 0.7
                # On évite que le 0.6 neutre ne maintienne l'alerte
                self.c_e_a.autonomic_activation = max(0.05, self.c_e_a.autonomic_activation - 0.6)
            
            # Ajustement dynamique du seuil de peur
            # Le seuil de base remonte (0.75) pour être plus "difficile" à effrayer
            base_threshold = 0.75
            self.c_e_a.fear_threshold = max(0.2, base_threshold - (stimulus_intensity * 0.3))

        return {
            "cortisol": self._internal_activity,
            "adrenaline": self.c_e_a.autonomic_activation if self.c_e_a else 0.05
        }
    
    def get_adrenaline_level(self):
        """Get current adrenaline level"""
        responses = self.get_emotional_responses()
        return responses['autonomic_activation']
    
    def reset(self):
        """Reset all amygdala nuclei"""
        if self.bla:
            for neuron in self.bla.pyramidal_neurons:
                neuron.reset()
            for neuron in self.bla.interneurons:
                neuron.reset()
            self.bla.fear_memory_strength = 0.0
            self.bla.conditioned_stimuli = {}
        
        if self.c_e_a:
            for neuron in self.c_e_a.output_neurons:
                neuron.reset()
            for neuron in self.c_e_a.autonomic_neurons:
                neuron.reset()
            self.c_e_a.autonomic_activation = 0.0
        
        if self.m_e_a:
            for neuron in self.m_e_a.social_neurons:
                neuron.reset()
            self.m_e_a.social_memory = {}

    def get_synaptic_modulation(self) -> Dict[str, float]:
        """
        Calcule les coefficients de modulation avec un filtre de rupture.
        """
        responses = self.get_emotional_responses()
        
        # 1. Calcul de l'impact (Intensité de la trace)
        # On utilise l'autonomic_activation comme moteur principal
        impact = responses['autonomic_activation'] / 100.0
        
        # 2. Détection du "Flash NMDA" (Le seuil de peur)
        # On ne déclenche le 1.0 que si l'adrénaline dépasse un seuil critique
        # ET que la valence est négative (info récupérée via l'activité interne)
        
        if responses['autonomic_activation'] > 75.0: # Seuil de choc majeur
            fear_level = 1.0
        else:
            # Pour un signal neutre ou modéré, on reste bas
            fear_level = 0.1
            
        return {
            "impact": min(1.0, impact),
            "fear_level": fear_level
        }
    
# Convenience functions for specialized amygdalae
def create_fear_amygdala(position: np.ndarray = None) -> Amygdala:
    """Create an amygdala optimized for fear processing"""
    if position is None:
        position = np.array([-15.0, -25.0, 0.0])
    
    amygdala = Amygdala(position)
    
    # Enhance fear-related nuclei
    amygdala.bla.size = 700           # Enhanced fear learning
    amygdala.c_e_a.size = 500         # Enhanced fear response
    
    return amygdala


def create_social_amygdala(position: np.ndarray = None) -> Amygdala:
    """Create an amygdala optimized for social processing"""
    if position is None:
        position = np.array([-15.0, -25.0, 0.0])
    
    amygdala = Amygdala(position)
    
    # Enhance social-related nuclei
    amygdala.m_e_a.size = 600         # Enhanced social processing
    amygdala.bla.size = 400           # Balanced fear processing
    
    return amygdala
