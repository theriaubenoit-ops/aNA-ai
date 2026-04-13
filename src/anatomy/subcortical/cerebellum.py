#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cerebellum implementation for aNA AI Project v5.3b

Communicates with: Input: (<- Cortex / Thalamus) | Output: (-> Motor Outputs / Feedback Loop)

This module implements the Cerebellum with its key layers (Granule, Purkinje, Molecular) and deep nuclei for motor coordination, cognitive processing, and error correction. It integrates with the ChemicalCore for neuromodulatory influences, particularly norepinephrine (Arousal) and serotonin (Mood). The Cerebellum processes mossy fiber and climbing fiber inputs to modulate motor output and cognitive functions through its inhibitory control of the deep nuclei.

Architecture, concept and supervision: Benoit Theriault
Collaboration, research and code: Gemini
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

from anatomy.base.neuron import Neuron, NeuronConfig


class CerebellarLayer(Enum):
    """Cerebellar layers"""
    MOLECULAR = "Molecular"      # Outer layer with stellate and basket cells
    PURKINJE = "Purkinje"       # Purkinje cell layer
    GRANULE = "Granule"         # Inner layer with granule and Golgi cells


@dataclass
class CerebellarRegionConfig:
    """Configuration for a cerebellar region"""
    region_type: str  # motor, cognitive, vestibular
    position: np.ndarray
    size: int
    baseline_activity: float = 0.1
    learning_rate: float = 0.01


class GranuleCellLayer:
    """Granule cell layer - input processing and pattern separation"""
    
    def __init__(self, position: np.ndarray, size: int = 2000):
        self.position = position
        self.size = size
        self.granule_cells = []
        self.golgi_cells = []
        
        self._initialize_neurons()
        self.mossy_fiber_input = 0.0
    
    def _initialize_neurons(self):
        """Initialize granule and Golgi cells"""
        # Granule cells (most numerous neurons in brain)
        for i in range(self.size):
            x = self.position[0] + np.random.uniform(-20.0, 20.0)
            y = self.position[1] + np.random.uniform(-20.0, 20.0)
            z = self.position[2] + np.random.uniform(-5.0, 5.0)
            
            position = np.array([x, y, z])
            
            # Granule cells have very high threshold (sparse coding)
            config = NeuronConfig(
                layer_id=0,
                threshold_potential=-55.0,
                base_energy_consumption=0.006999999999999999, firing_energy_cost=0.06999999999999999
            )
            neuron = Neuron(position, config)
            self.granule_cells.append(neuron)
        
        # Golgi cells (inhibitory interneurons, 1% of granule cells)
        golgi_size = self.size // 100
        for i in range(golgi_size):
            x = self.position[0] + np.random.uniform(-15.0, 15.0)
            y = self.position[1] + np.random.uniform(-15.0, 15.0)
            z = self.position[2] + np.random.uniform(-3.0, 3.0)
            
            position = np.array([x, y, z])
            
            config = NeuronConfig(
                layer_id=0,
                threshold_potential=-55.0,
                base_energy_consumption=0.006, firing_energy_cost=0.06
            )
            neuron = Neuron(position, config)
            self.golgi_cells.append(neuron)
    
    def process_mossy_fiber_input(self, input_signal: float, neuromodulators: Dict[str, float]):
        """Process input from mossy fibers"""
        self.mossy_fiber_input = input_signal
        
        # Granule cells receive mossy fiber input
        for neuron in self.granule_cells:
            # Only strong inputs activate granule cells (high threshold)
            if input_signal > 50.0:  # Threshold for granule cell activation
                modulated_input = input_signal * 0.1  # Scale down
                
                # Noradrenaline enhances granule cell responsiveness
                if 'norepinephrine' in neuromodulators:
                    modulated_input *= (1.0 + neuromodulators['norepinephrine'] * 0.3)
                
                neuron.receive_input(modulated_input, neuromodulators)
            
            neuron.update(0, neuromodulators)
        
        # Golgi cells provide feedback inhibition
        granule_activity = sum(1 for n in self.granule_cells if n.is_firing) / len(self.granule_cells)
        
        for neuron in self.golgi_cells:
            inhibitory_input = granule_activity * 30.0
            neuron.receive_input(inhibitory_input, neuromodulators)
            neuron.update(0, neuromodulators)
    
    def get_parallel_fiber_output(self) -> float:
        """Get output via parallel fibers to Purkinje cells"""
        active_ratio = sum(1 for n in self.granule_cells if n.is_firing) / len(self.granule_cells)
        return active_ratio * 50.0  # Scale down for Purkinje input
    
    def get_golgi_output(self) -> float:
        """Get Golgi cell inhibitory output"""
        active_ratio = sum(1 for n in self.golgi_cells if n.is_firing) / len(self.golgi_cells)
        return active_ratio * 20.0


class PurkinjeCellLayer:
    """Purkinje cell layer - main cerebellar output and learning"""
    
    def __init__(self, position: np.ndarray, size: int = 1000):
        self.position = position
        self.size = size
        self.purkinje_cells = []
        self.climbing_fiber_input = 0.0
        self.learning_rate = 0.01
        self.purkinje_activity = 0.1  # Valeur de base (Baseline)
        
        self._initialize_neurons()
    
    def _initialize_neurons(self):
        """Initialize Purkinje cells"""
        # Purkinje cells arranged in a plane
        for i in range(self.size):
            x = self.position[0] + (i % 25) * 4.0 - 50.0
            y = self.position[1] + (i // 25) * 4.0 - 50.0
            z = self.position[2]
            
            position = np.array([x, y, z])
            
            # Purkinje cells have complex dynamics
            config = NeuronConfig(
                layer_id=0,
                threshold_potential=-55.0,
                base_energy_consumption=0.012, firing_energy_cost=0.12  # High energy consumption
            )
            neuron = Neuron(position, config)
            self.purkinje_cells.append(neuron)
    
    def process_inputs(self, parallel_fiber_input: float, climbing_fiber_input: float, neuromodulators: Dict):
        """Process parallel fiber and climbing fiber inputs"""
        self.climbing_fiber_input = climbing_fiber_input
        self.purkinje_activity = min(1.0, (parallel_fiber_input * 0.01) + (climbing_fiber_input * 0.008))
        
        for neuron in self.purkinje_cells:
            # Parallel fiber input (weak, modulatory)
            pf_input = parallel_fiber_input * 0.1
            
            # Climbing fiber input (strong, instructive)
            cf_input = climbing_fiber_input * 2.0
            
            total_input = pf_input + cf_input
            
            # Dopamine modulates learning
            if 'dopamine' in neuromodulators:
                self.learning_rate = 0.01 + neuromodulators['dopamine'] * 0.02
            
            # Serotonin modulates Purkinje cell excitability
            if 'serotonin' in neuromodulators:
                total_input *= (1.0 + neuromodulators['serotonin'] * 0.2)
            
            neuron.receive_input(total_input, neuromodulators)
            neuron.update(0, neuromodulators)
    
    def get_output(self) -> float:
        """Get Purkinje cell output (inhibitory)"""
        active_ratio = sum(1 for n in self.purkinje_cells if n.is_firing) / len(self.purkinje_cells)
        # Purkinje output is inhibitory, so we invert the signal
        return (1.0 - active_ratio) * 100.0
    
    def get_learning_signal(self) -> float:
        """Get climbing fiber error signal for learning"""
        return self.climbing_fiber_input


class MolecularLayer:
    """Molecular layer - stellate and basket cells for lateral inhibition"""
    
    def __init__(self, position: np.ndarray, size: int = 300):
        self.position = position
        self.size = size
        self.stellate_cells = []
        self.basket_cells = []
        
        self._initialize_neurons()
    
    def _initialize_neurons(self):
        """Initialize stellate and basket cells"""
        # Stellate cells (superficial)
        stellate_size = self.size * 2 // 3
        for i in range(stellate_size):
            x = self.position[0] + np.random.uniform(-15.0, 15.0)
            y = self.position[1] + np.random.uniform(-15.0, 15.0)
            z = self.position[2] + np.random.uniform(2.0, 5.0)  # Superficial
            
            position = np.array([x, y, z])
            
            config = NeuronConfig(
                layer_id=0,
                threshold_potential=-58.0,
                base_energy_consumption=0.006999999999999999, firing_energy_cost=0.06999999999999999
            )
            neuron = Neuron(position, config)
            self.stellate_cells.append(neuron)
        
        # Basket cells (deeper)
        basket_size = self.size // 3
        for i in range(basket_size):
            x = self.position[0] + np.random.uniform(-15.0, 15.0)
            y = self.position[1] + np.random.uniform(-15.0, 15.0)
            z = self.position[2] + np.random.uniform(-2.0, 2.0)  # Deeper
            
            position = np.array([x, y, z])
            
            config = NeuronConfig(
                layer_id=0,
                threshold_potential=-56.0,
                base_energy_consumption=0.008, firing_energy_cost=0.08000000000000002
            )
            neuron = Neuron(position, config)
            self.basket_cells.append(neuron)
    
    def process_parallel_fiber_input(self, parallel_fiber_input: float, neuromodulators: Dict[str, float]):
        """Process parallel fiber input through molecular layer"""
        # Both cell types receive parallel fiber input
        for neuron in self.stellate_cells + self.basket_cells:
            input_signal = parallel_fiber_input * 0.2  # Moderate scaling
            
            # Acetylcholine enhances molecular layer processing
            if 'acetylcholine' in neuromodulators:
                input_signal *= (1.0 + neuromodulators['acetylcholine'] * 0.3)
            
            neuron.receive_input(input_signal, neuromodulators)
            neuron.update(0, neuromodulators)
    
    def get_lateral_inhibition(self) -> float:
        """Get lateral inhibition signal"""
        stellate_activity = sum(1 for n in self.stellate_cells if n.is_firing) / len(self.stellate_cells)
        basket_activity = sum(1 for n in self.basket_cells if n.is_firing) / len(self.basket_cells)
        
        # Combined inhibitory output
        total_inhibition = (stellate_activity + basket_activity) / 2
        return total_inhibition * 50.0


class CerebellarNuclei:
    """Deep cerebellar nuclei - final output stage"""
    
    def __init__(self, position: np.ndarray, size: int = 100):
        self.position = position
        self.size = size
        self.output_neurons = []
        
        self._initialize_neurons()
        self.nuclear_activity = 0.0
    
    def _initialize_neurons(self):
        """Initialize deep cerebellar nuclear neurons"""
        for i in range(self.size):
            x = self.position[0] + np.random.uniform(-5.0, 5.0)
            y = self.position[1] + np.random.uniform(-5.0, 5.0)
            z = self.position[2] + np.random.uniform(-3.0, 3.0)
            
            position = np.array([x, y, z])
            
            config = NeuronConfig(
                layer_id=0,
                threshold_potential=-52.0,
                base_energy_consumption=0.009000000000000001, firing_energy_cost=0.09000000000000001
            )
            neuron = Neuron(position, config)
            self.output_neurons.append(neuron)
    
    def process_input(self, purkinje_input: float, excitatory_input: float, neuromodulators: Dict[str, float]):
        """Process Purkinje inhibition and excitatory drive"""
        for neuron in self.output_neurons:
            # Nuclear neurons receive Purkinje inhibition + excitatory drive
            net_input = excitatory_input - (purkinje_input * 0.5)
            
            # Noradrenaline enhances nuclear excitability
            if 'norepinephrine' in neuromodulators:
                net_input *= (1.0 + neuromodulators['norepinephrine'] * 0.4)
            
            # Serotonin modulates output gain
            if 'serotonin' in neuromodulators:
                net_input *= (1.0 - neuromodulators['serotonin'] * 0.2)
            
            neuron.receive_input(net_input, neuromodulators)
            neuron.update(0, neuromodulators)
        
        # Update nuclear activity
        self.nuclear_activity = sum(1 for n in self.output_neurons if n.is_firing) / len(self.output_neurons)
    
    def get_output(self) -> float:
        """Get final cerebellar output"""
        return self.nuclear_activity * 100.0


class Cerebellum:
    """Complete Cerebellum with all layers and nuclei"""
    
    def __init__(self, position: np.ndarray = np.array([0.0, -40.0, 0.0])):
        self.position = position
        self.granule_layer = None
        self.purkinje_layer = None
        self.molecular_layer = None
        self.deep_nuclei = None
        
        self._initialize_layers()
    
    def _initialize_layers(self):
        """Initialize all cerebellar layers"""
        base_pos = self.position
        
        # Granule cell layer (deep)
        granule_pos = base_pos + np.array([0.0, 0.0, -10.0])
        self.granule_layer = GranuleCellLayer(granule_pos, size=3000)
        
        # Purkinje cell layer (middle)
        purkinje_pos = base_pos + np.array([0.0, 0.0, 0.0])
        self.purkinje_layer = PurkinjeCellLayer(purkinje_pos, size=800)
        
        # Molecular layer (superficial)
        molecular_pos = base_pos + np.array([0.0, 0.0, 10.0])
        self.molecular_layer = MolecularLayer(molecular_pos, size=500)
        
        # Deep cerebellar nuclei
        nuclei_pos = base_pos + np.array([0.0, -20.0, 0.0])
        self.deep_nuclei = CerebellarNuclei(nuclei_pos, size=200)
    
    def process_inputs(self, mossy_fiber_input: float, climbing_fiber_input: float,
                      excitatory_drive: float, neuromodulators: Dict[str, float]):
        """Process all cerebellar inputs"""
        # 1. Granule layer processing
        self.granule_layer.process_mossy_fiber_input(mossy_fiber_input, neuromodulators)
        
        # 2. Molecular layer processing
        pf_output = self.granule_layer.get_parallel_fiber_output()
        self.molecular_layer.process_parallel_fiber_input(pf_output, neuromodulators)
        
        # 3. Purkinje layer processing
        self.purkinje_layer.process_inputs(pf_output, climbing_fiber_input, neuromodulators)
        
        # 4. Deep nuclei processing
        purkinje_output = self.purkinje_layer.get_output()
        self.deep_nuclei.process_input(purkinje_output, excitatory_drive, neuromodulators)
    
    def get_outputs(self) -> Dict[str, float]:
        """Get outputs from all layers"""
        return {
            'granule_layer': self.granule_layer.get_parallel_fiber_output(),
            'purkinje_layer': self.purkinje_layer.get_output(),
            'molecular_layer': self.molecular_layer.get_lateral_inhibition(),
            'deep_nuclei': self.deep_nuclei.get_output(),
            'learning_signal': self.purkinje_layer.get_learning_signal()
        }
    
    def get_motor_coordination_signal(self) -> float:
        """Get motor coordination output"""
        return self.deep_nuclei.get_output()
    
    def get_cognitive_signal(self) -> float:
        """Get cognitive processing signal (from lateral cerebellum)"""
        # Simplified - in reality different cerebellar regions handle different functions
        purkinje_activity = sum(1 for n in self.purkinje_layer.purkinje_cells if n.is_firing) / len(self.purkinje_layer.purkinje_cells)
        return purkinje_activity * 50.0
    
    def reset(self):
        """Reset all cerebellar layers"""
        if self.granule_layer:
            for neuron in self.granule_layer.granule_cells:
                neuron.reset()
            for neuron in self.granule_layer.golgi_cells:
                neuron.reset()
        
        if self.purkinje_layer:
            for neuron in self.purkinje_layer.purkinje_cells:
                neuron.reset()
        
        if self.molecular_layer:
            for neuron in self.molecular_layer.stellate_cells:
                neuron.reset()
            for neuron in self.molecular_layer.basket_cells:
                neuron.reset()
        
        if self.deep_nuclei:
            for neuron in self.deep_nuclei.output_neurons:
                neuron.reset()
            self.deep_nuclei.nuclear_activity = 0.0

    def compute_correction(self, target_pos: np.ndarray, current_pos: np.ndarray) -> np.ndarray:
        """
        Calcule la correction motrice basée sur l'erreur spatiale.
        Simule l'ajustement du cervelet pour atteindre une cible.
        """
        error = target_pos - current_pos
        # On utilise l'activité actuelle du cervelet pour pondérer la correction
        inhibition = self.get_inhibitory_output() / 100.0
        
        # Plus l'inhibition est forte, plus la correction est stable (moins de saccades)
        correction_factor = 0.5 * (1.0 - inhibition * 0.2)
        return error * correction_factor

    def process_feedback(self, error_signal: float):
        """
        Traite le signal d'erreur via les fibres grimpantes.
        Une erreur forte augmente l'activité des cellules de Purkinje.
        """
        # On simule l'entrée des fibres grimpantes (climbing fibers)
        # qui est le signal d'erreur par excellence du cervelet
        neuromodulators = {} # On peut passer des neuromodulateurs si besoin
        
        # Le signal d'erreur impacte directement la couche de Purkinje
        self.purkinje_layer.process_inputs(
            parallel_fiber_input=10.0, # Activité de base
            climbing_fiber_input=error_signal * 100.0, # L'erreur est ici
            neuromodulators=neuromodulators
        )
    
    def get_inhibitory_output(self) -> float:
        """
        Récupère la sortie inhibitrice globale de la couche de Purkinje.
        Cette valeur module l'amplitude de la correction motrice.
        """
        if self.purkinje_layer:
            # On simule l'intégration des décharges des cellules de Purkinje
            # Plus l'activité de la couche est haute, plus l'inhibition est forte.
            return self.purkinje_layer.purkinje_activity * 100.0
        return 0.1

# Convenience functions for specialized cerebella
def create_motor_cerebellum(position: np.ndarray = None) -> Cerebellum:
    """Create a cerebellum optimized for motor coordination"""
    if position is None:
        position = np.array([0.0, -40.0, 0.0])
    
    cerebellum = Cerebellum(position)
    
    # Enhance motor-related processing
    cerebellum.granule_layer.size = 5000      # Enhanced pattern separation
    cerebellum.purkinje_layer.size = 1200    # Enhanced output control
    cerebellum.deep_nuclei.size = 300        # Enhanced motor output
    
    return cerebellum


def create_cognitive_cerebellum(position: np.ndarray = None) -> Cerebellum:
    """Create a cerebellum optimized for cognitive functions"""
    if position is None:
        position = np.array([0.0, -40.0, 0.0])
    
    cerebellum = Cerebellum(position)
    
    # Enhance cognitive processing
    cerebellum.molecular_layer.size = 800    # Enhanced lateral inhibition
    cerebellum.purkinje_layer.size = 1000    # Enhanced cognitive processing
    cerebellum.granule_layer.size = 4000     # Enhanced input processing
    
    return cerebellum