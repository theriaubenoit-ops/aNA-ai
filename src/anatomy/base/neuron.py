#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Neuron Class - The fundamental unit of the aNA v5.1 architecture

This class represents a single neuron with:
- 3D spatial positioning and relationships
- Electrical charge dynamics and firing behavior
- Power consumption and energy management
- Layer-specific properties for cortical organization
- Integration with neuromodulator systems

Architecture, concept and supervision: Benoit Theriault
Collaboration, research and code: Gemini
"""

import numpy as np
from typing import Tuple, Optional, Dict, Any
from dataclasses import dataclass


@dataclass
class NeuronConfig:
    """Configuration avancée pour la simulation AMPA/NMDA et Myéline"""
    
    # Plasticité AMPA/NMDA (LTP)
    learning_rate: float = 0.02       # Pas d'apprentissage de base (AMPA)
    nmda_threshold: float = 0.4      # Seuil pour activer la mémoire profonde
    
    # Structure (Myéline)
    myelination_rate: float = 0.01    # Vitesse de "câblage" physique

    # Electrical properties
    resting_potential: float = -70.0  # mV
    threshold_potential: float = -55.0  # mV
    firing_potential: float = 30.0  # mV
    refractory_period: int = 5  # time steps
    
    # Energy properties
    base_energy_consumption: float = 0.01 # Métabolisme
    firing_energy_cost: float = 0.1 # Métabolisme
    energy_recovery_rate: float = 0.005 # Métabolisme
    min_energy_threshold: float = 0.1
    
    # Structural properties
    dendritic_radius: float = 50.0  # micrometers
    axonal_length: float = 200.0  # micrometers
    
    # Layer-specific properties
    layer_id: int = 0  # 0-5 for cortical layers I-VI
    layer_threshold_modifier: float = 1.0
    layer_connectivity_modifier: float = 1.0 # Anatomie


class Neuron:
    """
    A single neuron with 3D positioning, electrical dynamics, and energy management.
    
    This class models the fundamental properties of biological neurons including:
    - Spatial relationships and connectivity
    - Membrane potential dynamics and action potentials
    - Energy consumption and metabolic processes
    - Layer-specific cortical properties
    - Integration with neuromodulatory systems
    """
    
    def __init__(self, position: np.ndarray, config: Optional[NeuronConfig] = None):
        """
        Initialize a neuron with 3D position and configuration.
        
        Args:
            position: 3D coordinates [x, y, z] in micrometers
            config: Neuron configuration parameters
        """
        self.position = np.array(position, dtype=float)
        self.config = config or NeuronConfig()

        # Synaptic properties
        self.ampa_receptors = 0.1  # Sensibilité de base
        self.nmda_threshold = 0.7  # Seuil de dépolarisation pour ouvrir la mémoire
        self.synaptic_weight = 0.1 # Le poids réel de la connexion
                
        # Electrical state
        self.membrane_potential = self.config.resting_potential
        self.refractory_timer = 0
        self.is_firing = False
        
        # Energy state
        self.energy_level = 1.0  # Normalized 0.0 to 1.0
        self.energy_consumed = 0.0
        
        # Structural state
        self.synaptic_strength = 1.0
        self.myelination_level = 0.0
        self.plasticity = 0.5
        
        # Activity tracking
        self.spike_history = []
        self.last_spike_time = -1
        self.activity_counter = 0
        
        # Neuromodulator sensitivity
        self.neuromodulator_sensitivity = {
            'dopamine': 1.0,
            'acetylcholine': 1.0,
            'serotonin': 1.0,
            'norepinephrine': 1.0,
            'no_gas': 1.0
        }
        
        # Layer-specific properties
        self._update_layer_properties()
    
    def _update_layer_properties(self):
        """Update properties based on cortical layer"""
        # Layer-specific threshold adjustments
        layer_thresholds = {
            0: 1.5,  # Layer I: Molecular (highest threshold)
            1: 0.8,  # Layer II: External Granular
            2: 0.8,  # Layer III: External Pyramidal
            3: 0.6,  # Layer IV: Internal Granular (lowest threshold - sensory input)
            4: 1.2,  # Layer V: Internal Pyramidal (motor output)
            5: 1.0   # Layer VI: Multiform
        }
        
        # Layer-specific connectivity
        layer_connectivity = {
            0: 0.3,  # Layer I: Feedback integration
            1: 0.9,  # Layer II: Inter-lobar connections
            2: 0.9,  # Layer III: Association areas
            3: 1.2,  # Layer IV: Sensory gateway
            4: 0.7,  # Layer V: Motor output
            5: 0.8   # Layer VI: Thalamic regulation
        }
        
        self.config.layer_threshold_modifier = layer_thresholds[self.config.layer_id]
        self.config.layer_connectivity_modifier = layer_connectivity[self.config.layer_id]
    
    def calculate_distance(self, other_neuron: 'Neuron') -> float:
        """
        Calculate Euclidean distance to another neuron.
        
        Args:
            other_neuron: Target neuron
            
        Returns:
            Distance in micrometers
        """
        return np.linalg.norm(self.position - other_neuron.position)
    
    def can_connect_to(self, other_neuron: 'Neuron') -> bool:
        """
        Determine if this neuron can form a synaptic connection.
        
        Args:
            other_neuron: Potential target neuron
            
        Returns:
            True if connection is possible
        """
        distance = self.calculate_distance(other_neuron)
        max_distance = self.config.dendritic_radius * (1 + self.myelination_level)
        return distance <= max_distance
    
    def receive_input(self, input_strength: float, neuromodulators: Dict[str, float]):
        """
        Process incoming synaptic input with neuromodulator effects.
        
        Args:
            input_strength: Raw synaptic input strength
            neuromodulators: Current neuromodulator levels in the local environment
        """
        if self.refractory_timer > 0 or self.energy_level < self.config.min_energy_threshold:
            return
        
        # Apply neuromodulator effects
        modulated_input = self._apply_neuromodulator_effects(input_strength, neuromodulators)
        
        # Update membrane potential
        self.membrane_potential += modulated_input
        
        # Apply natural decay
        self.membrane_potential *= 0.98
    
    def _apply_neuromodulator_effects(self, input_strength: float, neuromodulators: Dict[str, float]) -> float:
        # 1. Calcul des effets individuels (ton code actuel)
        dopamine_effect = 1.0 + (neuromodulators.get('dopamine', 0.0) * 0.5)
        ach_effect = 1.0 + (neuromodulators.get('acetylcholine', 0.0) * 0.3)
        serotonin_effect = 1.0 - (neuromodulators.get('serotonin', 0.0) * 0.2)
        norepinephrine_effect = 1.0 + (neuromodulators.get('norepinephrine', 0.0) * 0.4)
        no_effect = 1.0 + (neuromodulators.get('no_gas', 0.0) * 0.2)

        # 2. LOGIQUE DE SAUVETAGE : L'atténuation par la certitude
        # Si l'input est déjà fort (le neurone a reconnu le pattern), 
        # on réduit drastiquement le multiplicateur.
        total_modulation = (dopamine_effect * ach_effect * serotonin_effect * norepinephrine_effect * no_effect)
        
        # Frein métabolique : plus input_strength est proche de 1.0, 
        # plus on ramène la modulation vers 1.0 (neutre)
        frein = max(0.0, 1.0 - input_strength) 
        modulation_calmee = 1.0 + (total_modulation - 1.0) * frein

        return input_strength * modulation_calmee
    
    def update(self, time_step: int, neuromodulators: Dict[str, float]):
        """
        Update neuron state for one time step.
        
        Args:
            time_step: Current simulation time step
            neuromodulators: Current neuromodulator levels
        """
        # Handle refractory period
        if self.refractory_timer > 0:
            self.refractory_timer -= 1
            if self.refractory_timer == 0:
                self.membrane_potential = self.config.resting_potential
                self.is_firing = False
        
        # Check for action potential
        elif self.membrane_potential >= self.config.threshold_potential * self.config.layer_threshold_modifier:
            self._fire_action_potential(time_step)
        
        # Update energy levels
        self._update_energy()
        
        # Update plasticity based on activity
        self._update_plasticity(neuromodulators)
        
        # Update myelination based on repeated firing
        self._update_myelination()
    
    def _fire_action_potential(self, time_step: int):
        """Execute action potential firing"""
        self.is_firing = True
        self.membrane_potential = self.config.firing_potential
        self.refractory_timer = self.config.refractory_period
        self.last_spike_time = time_step
        self.activity_counter += 1
        
        # Record spike
        self.spike_history.append(time_step)
        if len(self.spike_history) > 100:  # Keep last 100 spikes
            self.spike_history.pop(0)
    


    def _update_energy(self):
        """Update energy consumption and recovery - ACTIVATED v5.9"""
        
        # 1. Consommation de base (Entretien des pompes ioniques)
        energy_cost = self.config.base_energy_consumption
        
        # 2. Coût du Potentiel d'Action (Le "Spike")
        # C'est ici que l'ATP est massivement consommé
        if self.is_firing:
            energy_cost += self.config.firing_energy_cost
        
        # 3. Modulation par couche (Ex: La couche V consomme plus)
        energy_cost *= self.config.layer_connectivity_modifier
        
        # 4. Mise à jour du stock d'ATP
        self.energy_level -= energy_cost
        self.energy_consumed += energy_cost
        
        # 5. Récupération (Synthèse d'ATP / Repos)
        if self.energy_level < 1.0:
            self.energy_level += self.config.energy_recovery_rate
        
        # 6. Sécurité (L'énergie ne peut pas être négative)
        self.energy_level = max(0.0, min(1.0, self.energy_level))
    
    def _update_plasticity(self, neuromodulators: dict = None): # Ajout de l'argument
        """
        Simulation de la plasticité Hebbienne v5.9.
        Intègre la synergie entre dépolarisation (AMPA) et consolidation (NMDA)
        modulée par le contexte émotionnel (Amygdale).
        """
        # Initialisation par défaut si aucun dictionnaire n'est passé
        nm = neuromodulators if neuromodulators else {}
        
        # Récupération des facteurs d'influence (Ex: Noradrénaline pour l'alerte)
        ne_boost = nm.get('norepinephrine', 0.0) * 0.5 
        da_boost = nm.get('dopamine', 0.0) * 0.2

        if self.is_firing:
            # 1. Calcul de l'impact du signal (Potentiel local)
            # L'influence émotionnelle (NE/DA) facilite le passage du seuil NMDA
            impact_signal = self.plasticity * (1.0 + self.myelination_level + ne_boost)
            
            # 2. Logique de recrutement des récepteurs
            if impact_signal > self.config.nmda_threshold:
                # Seuil NMDA franchi : LTP forte
                # On booste le gain si l'émotion est forte
                gain = self.config.learning_rate * (2.5 + da_boost)
                self.plasticity += gain
            else:
                # Activation AMPA seule
                self.plasticity += self.config.learning_rate
        
        # 3. HOMÉOSTASIE (Le fameux 0.999)
        # On pourrait imaginer que l'émotion réduit temporairement l'homéostasie 
        # pour "fixer" la trace (évite l'érosion immédiate).
        decay_factor = 0.999 + (min(0.0009, ne_boost * 0.001)) 
        self.plasticity *= decay_factor
        
        # 4. Limites biologiques
        self.plasticity = max(0.01, min(1.0, self.plasticity))
    
    def _update_myelination(self):
        """Force la croissance de la gaine dès la dépolarisation"""
        if self.is_firing: 
            # On ignore le last_spike_time pour ce test
            increment = 0.01  # On revient à une valeur plus réaliste
            self.myelination_level += increment
            
            # Cap à 1.0 (Conductivité max +50%)
            if self.myelination_level > 1.0:
                self.myelination_level = 1.0
    
    def get_output_strength(self) -> float:
        """
        Get the output strength when this neuron fires.
        
        Returns:
            Output signal strength
        """
        if not self.is_firing:
            return 0.0
        
        # Base output strength modified by various factors
        base_strength = 1.0
        energy_modifier = self.energy_level  # Weaker output when low energy
        plasticity_modifier = self.plasticity  # Stronger output with higher plasticity
        myelination_modifier = 1.0 + self.myelination_level * 0.5  # Faster conduction
        
        return (base_strength * energy_modifier * plasticity_modifier * 
                myelination_modifier * self.config.layer_connectivity_modifier)
    
    def get_output_strength(self) -> float:
        """
        Calcule la force du signal de sortie (Conductivité) lors du déclenchement.
        Fusionne la plasticité, la myélinisation et l'état énergétique.
        """
        if not self.is_firing:
            return 0.0
        
        # 1. Facteur de Conductivité (Concept Benoit Theriault)
        # La myélinisation augmente la vitesse et la force de conduction.
        conductivité_myéline = 1.0 + (self.myelination_level * 0.5)
        
        # 2. Facteur Métabolique (Vitalité)
        # Un niveau d'énergie bas affaiblit physiquement le signal de sortie.
        modulateur_energie = self.energy_level
        
        # 3. Facteur de Plasticité (LTP)
        # Reflète l'efficacité synaptique apprise au fil des cycles.
        efficacité_synaptique = self.plasticity
        
        # Résultante finale : Justesse scientifique et performance
        # On inclut le modificateur de couche pour respecter l'anatomie corticale.
        return (efficacité_synaptique * conductivité_myéline * modulateur_energie * self.config.layer_connectivity_modifier)
        
    def reset(self):
        """Reset neuron to initial state"""
        self.membrane_potential = self.config.resting_potential
        self.refractory_timer = 0
        self.is_firing = False
        self.energy_level = 1.0
        self.energy_consumed = 0.0
        self.spike_history = []
        self.last_spike_time = -1
        self.activity_counter = 0
        self.plasticity = 0.5
        self.myelination_level = 0.0


class NeuronPopulation:
    """
    A population of neurons with spatial organization and collective behavior.
    """
    
    def __init__(self, positions: np.ndarray, config: Optional[NeuronConfig] = None):
        """
        Initialize a population of neurons.
        
        Args:
            positions: Array of 3D positions for each neuron
            config: Default configuration for all neurons
        """
        self.config = config or NeuronConfig()
        self.neurons = []
        
        # Create neurons with layer assignment based on position
        for i, pos in enumerate(positions):
            neuron_config = NeuronConfig()
            neuron_config.layer_id = self._assign_layer(pos)
            neuron_config.position = pos
            self.neurons.append(Neuron(pos, neuron_config))
    
    def _assign_layer(self, position: np.ndarray) -> int:
        """Assign cortical layer based on 3D position"""
        # Simplified layer assignment based on y-coordinate (depth)
        y = position[1]
        if y > 0.8:
            return 0  # Layer I
        elif y > 0.6:
            return 1  # Layer II
        elif y > 0.4:
            return 2  # Layer III
        elif y > 0.2:
            return 3  # Layer IV
        elif y > 0.0:
            return 4  # Layer V
        else:
            return 5  # Layer VI
    
    def update(self, time_step: int, neuromodulators: Dict[str, float]):
        """Update all neurons in the population"""
        for neuron in self.neurons:
            neuron.update(time_step, neuromodulators)
    
    def get_firing_neurons(self) -> list:
        """Get list of currently firing neurons"""
        return [i for i, neuron in enumerate(self.neurons) if neuron.is_firing]
    
    def get_average_potential(self) -> float:
        """Get average membrane potential of the population"""
        if not self.neurons:
            return 0.0
        return np.mean([n.membrane_potential for n in self.neurons])
    
    def get_average_energy(self) -> float:
        """Get average energy level of the population"""
        if not self.neurons:
            return 0.0
        return np.mean([n.energy_level for n in self.neurons])
    
    def get_activity_rate(self) -> float:
        """Get percentage of neurons currently firing"""
        if not self.neurons:
            return 0.0
        firing_count = sum(1 for n in self.neurons if n.is_firing)
        return firing_count / len(self.neurons)
    
    def get_average_activity(self) -> float:
        """Get average activity level of the population (same as activity rate)"""
        return self.get_activity_rate()
