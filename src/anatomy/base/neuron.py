#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Neuron implementation for aNA AI Project v5.3 - The fundamental unit of the aNA architecture

Communicates with: Input: (<- Synapses) | Output: (-> Axon / Post-synaptic targets)

Description: This class represents a single neuron with:
- 3D spatial positioning and relationships
- Electrical charge dynamics and firing behavior
- Power consumption and energy management
- Layer-specific properties for cortical organization
- Integration with neuromodulator systems

Architecture, concept and supervision: Benoit Theriault
Collaboration, research and code: Gemini, GPT
"""
import numpy as np
from typing import Tuple, Optional, Dict, Any
from dataclasses import dataclass
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from config import get_config
from registry import ORGANS

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
        
        # Neuromodulator sensitivity [Double? See neuromodulator.py]
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
        """
        Régulation de la réponse synaptique par la chimie et la certitude (v5.3.1).
        """
        # 1. Calcul de l'excitation chimique nette (Somme pondérée plutôt que produit)
        excitateurs = (neuromodulators.get('dopamine', 0.0) * 0.5) + \
                    (neuromodulators.get('norepinephrine', 0.0) * 0.4) + \
                    (neuromodulators.get('acetylcholine', 0.0) * 0.3)
        
        inhibiteurs = (neuromodulators.get('serotonin', 0.0) * 0.2)
        
        net_mod = 1.0 + (excitateurs - inhibiteurs)

        # 2. Logique du Frein : Atténuation par la Saliance
        # Si input_strength est faible, on écoute beaucoup la chimie (exploration).
        # Si input_strength est fort, on protège le pattern (exploitation).
        # On utilise un clamp pour éviter que le frein ne devienne négatif.
        saliance = max(0.0, min(1.0, input_strength))
        atténuation = 1.0 - (saliance * 0.7) # On garde au moins 30% de l'effet chimique
        
        modulation_finale = 1.0 + (net_mod - 1.0) * atténuation
        
        return input_strength * modulation_finale
    
    def update(self, time_step: int, neuromodulators: Dict[str, float] = None):
        """
        Version v5.3.1 - Intégration de la garde métabolique
        """
        # 1. GARDE : Si l'énergie est sous le seuil critique (ex: 0.1),
        # le neurone entre en état de "Sommeil Métabolique".
        if self.energy_level < self.config.min_energy_threshold:
            self.is_firing = False
            self.membrane_potential = self.config.resting_potential # Reset électrique
            self._update_energy() # On ne fait que tenter de récupérer l'énergie
            return 

        # 2. Logique électrique normale si assez d'énergie
        if self.refractory_timer > 0:
            self.refractory_timer -= 1
            if self.refractory_timer == 0:
                self.membrane_potential = self.config.resting_potential
                self.is_firing = False
                
        elif self.membrane_potential >= self.config.threshold_potential * self.config.layer_threshold_modifier:
            self._fire_action_potential(time_step) # Ici on consommera l'ATP au prochain cycle
        
        # 3. Mise à jour des stocks après l'action
        self._update_energy()
        self._update_plasticity(neuromodulators)
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
        """Modèle de respiration métabolique aNA v5.3.2"""
        
        # 1. PERTE : Maintenance basale ("poussière d'énergie") + Métabolisme de base
        maintenance_cost = 0.001 
        energy_cost = self.config.base_energy_consumption + maintenance_cost
        
        # 2. PERTE : Surcoût si le neurone décharge
        if self.is_firing:
            energy_cost += self.config.firing_energy_cost
        
        # 3. APPLICATION : On retire l'énergie consommée
        self.energy_level -= (energy_cost * self.config.layer_connectivity_modifier)
        
        # 4. GAIN : La "Pompe à Glucose" (Récupération lente)
        if not self.is_firing:
            # Remontée lente suggérée pour l'inaction
            self.energy_level += 0.015 # 0.014 minimum, pour éviter les problèmes de récupération
        else:
            # Récupération de base (synthèse ATP standard)
            self.energy_level += self.config.energy_recovery_rate
        
        # 5. ÉQUILIBRE : Clamp de sécurité entre 0 et 1
        self.energy_level = max(0.0, min(1.0, self.energy_level))
    
    def _update_plasticity(self, neuromodulators: dict = None):
        """
        Plasticité Hebbienne v5.3.1 : Synergie AMPA/NMDA et fixation émotionnelle.
        """
        # 1. Sécurisation de la chimie (Évite les crashs Thalamus)
        nm = neuromodulators if neuromodulators is not None else {}
        config = get_config() # Utilisation des constantes globales
        
        # Récupération des modulateurs
        ne_boost = nm.get('norepinephrine', 0.0)
        da_boost = nm.get('dopamine', 0.0)

        if self.is_firing:
            # 2. Calcul de l'impact (La myéline facilite l'ouverture NMDA)
            impact_signal = self.plasticity * (1.0 + self.myelination_level + (ne_boost * 0.5))
            
            if impact_signal > self.config.nmda_threshold:
                # Consolidation forte (LTP) boostée par la Dopamine
                gain = self.config.learning_rate * (2.5 + (da_boost * 0.5))
                self.plasticity += gain
            else:
                # Apprentissage de base (AMPA)
                self.plasticity += self.config.learning_rate
        
        # 3. HOMÉOSTASIE ET FIXATION (Decay)
        # On récupère le decay de base (ex: 0.9999) depuis la config
        base_decay = config.get("NEURON_PLASTICITY_DECAY", 0.9999)
        
        # La Noradrénaline réduit le decay (fixation du souvenir)
        # Plus ne_boost est haut, plus on s'approche de 1.0 (zéro oubli)
        fixation_factor = ne_boost * 0.0001 
        current_decay = min(1.0, base_decay + fixation_factor)
        
        self.plasticity *= current_decay
        
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
        
    def update(self, time_step: int, neuromodulators: Dict[str, float] = None):
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
