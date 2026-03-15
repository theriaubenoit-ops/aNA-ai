#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hippocampus implementation for aNA v4

This module implements the Hippocampus with all major subregions:
- Dentate Gyrus (DG)
- CA4 (Hilus)
- CA3
- CA2
- CA1
- Subiculum

Each region has specialized neuron types and connectivity patterns for
memory formation, consolidation, and spatial navigation.
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

from .neuron import Neuron, NeuronConfig, NeuronPopulation


class HippocampalRegion(Enum):
    """Hippocampal subregions"""
    DENTATE_GYRUS = "DG"      # Pattern separation
    CA4 = "CA4"               # Hilus, mossy cells
    CA3 = "CA3"               # Autoassociative memory
    CA2 = "CA2"               # Social memory
    CA1 = "CA1"               # Output to cortex
    SUBICULUM = "SUB"         # Final output stage


@dataclass
class HippocampalRegionConfig:
    """Configuration for a hippocampal region"""
    region_type: HippocampalRegion
    position: np.ndarray
    size: int
    neuron_type: str = "pyramidal"  # pyramidal, granule, mossy
    connectivity_pattern: str = "trisynaptic"  # trisynaptic, direct
    plasticity_rate: float = 1.0
    baseline_activity: float = 0.05


class DentateGyrus:
    """Dentate Gyrus - Pattern separation and input filtering"""
    
    def __init__(self, position: np.ndarray, size: int = 500):
        self.position = position
        self.size = size
        self.granule_cells = []
        self.hilar_cells = []
        self.mossy_fibers = []
        self.fear_memories = {}  # Store fear memories
        
        self._initialize_neurons()
    
    def _initialize_neurons(self):
        """Initialize granule cells and hilar cells"""
        # Granule cells (input layer)
        for i in range(self.size):
            # Generate positions in a curved structure
            angle = (i / self.size) * np.pi
            radius = 20.0 + (i / self.size) * 10.0
            
            x = self.position[0] + radius * np.cos(angle)
            y = self.position[1] + radius * np.sin(angle)
            z = self.position[2] + np.random.uniform(-5.0, 5.0)
            
            position = np.array([x, y, z])
            
            # Granule cells have high threshold and sparse firing
            config = NeuronConfig(
                layer_id=0,
                threshold_potential=-50.0,  # High threshold for sparse coding
                base_energy_consumption=0.006, firing_energy_cost=0.06
            )
            neuron = Neuron(position, config)
            self.granule_cells.append(neuron)
        
        # Hilar cells (mossy cells)
        hilar_size = self.size // 10
        for i in range(hilar_size):
            x = self.position[0] + np.random.uniform(-10.0, 10.0)
            y = self.position[1] + np.random.uniform(-10.0, 10.0)
            z = self.position[2] + np.random.uniform(-5.0, 5.0)
            
            position = np.array([x, y, z])
            
            # Mossy cells have lower threshold
            config = NeuronConfig(
                layer_id=0,
                threshold_potential=-55.0,
                base_energy_consumption=0.008, firing_energy_cost=0.08000000000000002
            )
            neuron = Neuron(position, config)
            self.hilar_cells.append(neuron)
    
    def process_input(self, entorhinal_input: float, neuromodulators: Dict[str, float]):
        """Process input from entorhinal cortex"""
        # Granule cells receive direct input
        for neuron in self.granule_cells:
            input_signal = entorhinal_input
            
            # Dopamine enhances LTP in DG
            if 'dopamine' in neuromodulators:
                input_signal *= (1.0 + neuromodulators['dopamine'] * 0.3)
            
            # Acetylcholine increases excitability
            if 'acetylcholine' in neuromodulators:
                input_signal *= (1.0 + neuromodulators['acetylcholine'] * 0.2)
            
            neuron.receive_input(input_signal, neuromodulators)
            neuron.update(0, neuromodulators)
        
        # Hilar cells receive feedback
        active_granule_ratio = sum(1 for n in self.granule_cells if n.is_firing) / len(self.granule_cells)
        
        for neuron in self.hilar_cells:
            feedback_signal = active_granule_ratio * 50.0
            neuron.receive_input(feedback_signal, neuromodulators)
            neuron.update(0, neuromodulators)
    
    def get_mossy_fiber_output(self) -> float:
        """Get output via mossy fibers to CA3"""
        active_ratio = sum(1 for n in self.granule_cells if n.is_firing) / len(self.granule_cells)
        return active_ratio * 100.0
    
    def get_hilar_output(self) -> float:
        """Get hilar cell output"""
        active_ratio = sum(1 for n in self.hilar_cells if n.is_firing) / len(self.hilar_cells)
        return active_ratio * 50.0
    
    def form_fear_memory(self, stimulus: str, strength: float):
        """Form a fear memory associated with a stimulus"""
        self.fear_memories[stimulus] = strength
    
    def get_fear_response(self, stimulus: str) -> float:
        """Get fear response to a specific stimulus"""
        return self.fear_memories.get(stimulus, 0.0)


class CA3Region:
    """CA3 - Autoassociative memory and pattern completion"""
    
    def __init__(self, position: np.ndarray, size: int = 300):
        self.position = position
        self.size = size
        self.pyramidal_cells = []
        self.recurrent_collaterals = []
        
        self._initialize_neurons()
    
    def _initialize_neurons(self):
        """Initialize CA3 pyramidal cells with recurrent connections"""
        for i in range(self.size):
            # Generate positions in a curved structure
            angle = (i / self.size) * np.pi * 1.5
            radius = 15.0 + (i / self.size) * 15.0
            
            x = self.position[0] + radius * np.cos(angle)
            y = self.position[1] + radius * np.sin(angle)
            z = self.position[2] + np.random.uniform(-5.0, 5.0)
            
            position = np.array([x, y, z])
            
            # CA3 pyramidal cells have recurrent connections
            config = NeuronConfig(
                layer_id=0,
                threshold_potential=-52.0,
                base_energy_consumption=0.009000000000000001, firing_energy_cost=0.09000000000000001
            )
            neuron = Neuron(position, config)
            self.pyramidal_cells.append(neuron)
    
    def process_input(self, mossy_fiber_input: float, recurrent_input: float, neuromodulators: Dict[str, float]):
        """Process input from DG and recurrent connections"""
        for neuron in self.pyramidal_cells:
            total_input = mossy_fiber_input + recurrent_input
            
            # Strong mossy fiber input drives CA3
            total_input *= 2.0
            
            # Dopamine enhances pattern completion
            if 'dopamine' in neuromodulators:
                total_input *= (1.0 + neuromodulators['dopamine'] * 0.4)
            
            # Serotonin modulates recurrent activity
            if 'serotonin' in neuromodulators:
                total_input *= (1.0 - neuromodulators['serotonin'] * 0.2)
            
            neuron.receive_input(total_input, neuromodulators)
            neuron.update(0, neuromodulators)
    
    def get_recurrent_activity(self) -> float:
        """Get recurrent collateral activity"""
        active_ratio = sum(1 for n in self.pyramidal_cells if n.is_firing) / len(self.pyramidal_cells)
        return active_ratio * 80.0
    
    def get_output(self) -> float:
        """Get output to CA1"""
        active_ratio = sum(1 for n in self.pyramidal_cells if n.is_firing) / len(self.pyramidal_cells)
        return active_ratio * 100.0


class CA1Region:
    """CA1 - Main output region and temporal processing"""
    
    def __init__(self, position: np.ndarray, size: int = 400):
        self.position = position
        self.size = size
        self.pyramidal_cells = []
        self.interneurons = []
        
        self._initialize_neurons()
    
    def _initialize_neurons(self):
        """Initialize CA1 pyramidal cells and interneurons"""
        # Pyramidal cells
        for i in range(self.size):
            angle = (i / self.size) * np.pi * 1.2
            radius = 20.0 + (i / self.size) * 10.0
            
            x = self.position[0] + radius * np.cos(angle)
            y = self.position[1] + radius * np.sin(angle)
            z = self.position[2] + np.random.uniform(-3.0, 3.0)
            
            position = np.array([x, y, z])
            
            config = NeuronConfig(
                layer_id=0,
                threshold_potential=-53.0,
                base_energy_consumption=0.0085, firing_energy_cost=0.085
            )
            neuron = Neuron(position, config)
            self.pyramidal_cells.append(neuron)
        
        # Interneurons (10% of population)
        interneuron_size = self.size // 10
        for i in range(interneuron_size):
            x = self.position[0] + np.random.uniform(-15.0, 15.0)
            y = self.position[1] + np.random.uniform(-15.0, 15.0)
            z = self.position[2] + np.random.uniform(-5.0, 5.0)
            
            position = np.array([x, y, z])
            
            # Interneurons have lower threshold and inhibitory function
            config = NeuronConfig(
                layer_id=0,
                threshold_potential=-58.0,
                base_energy_consumption=0.006999999999999999, firing_energy_cost=0.06999999999999999
            )
            neuron = Neuron(position, config)
            self.interneurons.append(neuron)
    
    def process_input(self, CA3_input: float, direct_input: float, neuromodulators: Dict[str, float]):
        """Process input from CA3 and direct entorhinal input"""
        # Pyramidal cells receive both inputs
        for neuron in self.pyramidal_cells:
            total_input = CA3_input * 0.7 + direct_input * 0.3
            
            # Acetylcholine enhances direct input
            if 'acetylcholine' in neuromodulators:
                total_input += direct_input * neuromodulators['acetylcholine'] * 0.5
            
            # Norepinephrine increases overall excitability
            if 'norepinephrine' in neuromodulators:
                total_input *= (1.0 + neuromodulators['norepinephrine'] * 0.3)
            
            neuron.receive_input(total_input, neuromodulators)
            neuron.update(0, neuromodulators)
        
        # Interneurons provide feedback inhibition
        pyramidal_activity = sum(1 for n in self.pyramidal_cells if n.is_firing) / len(self.pyramidal_cells)
        
        for neuron in self.interneurons:
            inhibitory_input = pyramidal_activity * 60.0
            neuron.receive_input(inhibitory_input, neuromodulators)
            neuron.update(0, neuromodulators)
    
    def get_output(self) -> float:
        """Get output to subiculum and cortex"""
        active_ratio = sum(1 for n in self.pyramidal_cells if n.is_firing) / len(self.pyramidal_cells)
        inhibition = sum(1 for n in self.interneurons if n.is_firing) / len(self.interneurons)
        
        # Net output accounts for inhibition
        net_activity = max(0.0, active_ratio - inhibition * 0.5)
        return net_activity * 100.0


class Subiculum:
    """Subiculum - Final hippocampal output stage"""
    
    def __init__(self, position: np.ndarray, size: int = 200):
        self.position = position
        self.size = size
        self.output_neurons = []
        
        self._initialize_neurons()
    
    def _initialize_neurons(self):
        """Initialize subicular output neurons"""
        for i in range(self.size):
            x = self.position[0] + np.random.uniform(-10.0, 10.0)
            y = self.position[1] + np.random.uniform(-10.0, 10.0)
            z = self.position[2] + np.random.uniform(-5.0, 5.0)
            
            position = np.array([x, y, z])
            
            config = NeuronConfig(
                layer_id=0,
                threshold_potential=-54.0,
                base_energy_consumption=0.008, firing_energy_cost=0.08000000000000002
            )
            neuron = Neuron(position, config)
            self.output_neurons.append(neuron)
    
    def process_input(self, CA1_input: float, neuromodulators: Dict[str, float]):
        """Process input from CA1"""
        for neuron in self.output_neurons:
            input_signal = CA1_input
            
            # Dopamine modulates output gain
            if 'dopamine' in neuromodulators:
                input_signal *= (1.0 + neuromodulators['dopamine'] * 0.2)
            
            # Serotonin modulates output threshold
            if 'serotonin' in neuromodulators:
                # Higher serotonin = lower output (anxiety-like effect)
                input_signal *= (1.0 - neuromodulators['serotonin'] * 0.1)
            
            neuron.receive_input(input_signal, neuromodulators)
            neuron.update(0, neuromodulators)
    
    def get_output(self) -> float:
        """Get final hippocampal output"""
        active_ratio = sum(1 for n in self.output_neurons if n.is_firing) / len(self.output_neurons)
        return active_ratio * 100.0


class Hippocampus:
    """Complete Hippocampus with all subregions"""
    
    def __init__(self, position: np.ndarray = np.array([10.0, -30.0, 0.0])):
        self.position = position
        self.dentate_gyrus = None
        self.ca3 = None
        self.ca1 = None
        self.subiculum = None
        
        self._initialize_regions()
    
    def _initialize_regions(self):
        """Initialize all hippocampal subregions"""
        base_pos = self.position
        
        # Dentate Gyrus (input region)
        dg_pos = base_pos + np.array([-15.0, 10.0, 0.0])
        self.dentate_gyrus = DentateGyrus(dg_pos, size=600)
        
        # CA3 (autoassociative memory)
        ca3_pos = base_pos + np.array([0.0, 5.0, 0.0])
        self.ca3 = CA3Region(ca3_pos, size=400)
        
        # CA1 (output region)
        ca1_pos = base_pos + np.array([15.0, 5.0, 0.0])
        self.ca1 = CA1Region(ca1_pos, size=500)
        
        # Subiculum (final output)
        sub_pos = base_pos + np.array([0.0, -10.0, 0.0])
        self.subiculum = Subiculum(sub_pos, size=300)
    
    def process_input(self, entorhinal_input: float, neuromodulators: Dict[str, float]):
        """Process input through the trisynaptic circuit"""
        # 1. Dentate Gyrus processing
        self.dentate_gyrus.process_input(entorhinal_input, neuromodulators)
        
        # 2. CA3 processing (mossy fibers + recurrent)
        mossy_output = self.dentate_gyrus.get_mossy_fiber_output()
        recurrent_input = self.ca3.get_recurrent_activity()
        self.ca3.process_input(mossy_output, recurrent_input, neuromodulators)
        
        # 3. CA1 processing (Schaffer collateral + direct)
        ca3_output = self.ca3.get_output()
        direct_input = entorhinal_input * 0.3  # Direct pathway
        self.ca1.process_input(ca3_output, direct_input, neuromodulators)
        
        # 4. Subiculum processing
        ca1_output = self.ca1.get_output()
        self.subiculum.process_input(ca1_output, neuromodulators)
    
    def get_outputs(self) -> Dict[str, float]:
        """Get outputs from all regions"""
        return {
            'dentate_gyrus': self.dentate_gyrus.get_mossy_fiber_output(),
            'ca3': self.ca3.get_output(),
            'ca1': self.ca1.get_output(),
            'subiculum': self.subiculum.get_output(),
            'hilar': self.dentate_gyrus.get_hilar_output()
        }
    
    def get_spatial_signal(self) -> float:
        """Get spatial navigation signal from CA1"""
        # CA1 contains place cells for spatial navigation
        ca1_output = self.ca1.get_output()
        
        # Spatial signal is modulated by theta rhythm (simplified)
        theta_modulation = 0.5 + 0.5 * np.sin(np.pi * ca1_output / 50.0)
        return ca1_output * theta_modulation
    
    def get_memory_signal(self) -> float:
        """Get memory consolidation signal"""
        # Memory signal based on CA3 pattern completion
        ca3_activity = self.ca3.get_output()
        ca1_activity = self.ca1.get_output()
        
        # Memory consolidation = CA3 pattern completion * CA1 output
        return (ca3_activity * ca1_activity) / 100.0
    
    def reset(self):
        """Reset all hippocampal regions"""
        if self.dentate_gyrus:
            for neuron in self.dentate_gyrus.granule_cells:
                neuron.reset()
            for neuron in self.dentate_gyrus.hilar_cells:
                neuron.reset()
        
        if self.ca3:
            for neuron in self.ca3.pyramidal_cells:
                neuron.reset()
        
        if self.ca1:
            for neuron in self.ca1.pyramidal_cells:
                neuron.reset()
            for neuron in self.ca1.interneurons:
                neuron.reset()
        
        if self.subiculum:
            for neuron in self.subiculum.output_neurons:
                neuron.reset()


# Convenience functions for specialized hippocampi
def create_memory_hippocampus(position: np.ndarray = None) -> Hippocampus:
    """Create a hippocampus optimized for memory formation"""
    if position is None:
        position = np.array([10.0, -30.0, 0.0])
    
    hippo = Hippocampus(position)
    
    # Enhance memory-related regions
    hippo.dentate_gyrus.size = 800      # Enhanced pattern separation
    hippo.ca3.size = 600                # Enhanced autoassociative memory
    hippo.ca1.size = 700                # Enhanced output
    
    return hippo


def create_spatial_hippocampus(position: np.ndarray = None) -> Hippocampus:
    """Create a hippocampus optimized for spatial navigation"""
    if position is None:
        position = np.array([10.0, -30.0, 0.0])
    
    hippo = Hippocampus(position)
    
    # Enhance spatial processing
    hippo.ca1.size = 800                # More place cells
    hippo.ca3.size = 500                # Enhanced pattern completion for navigation
    
    return hippo