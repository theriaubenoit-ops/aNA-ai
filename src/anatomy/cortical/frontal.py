#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Frontal Lobe implementation for aNA v4.0

This module implements the Frontal Lobe with proper motor cortex organization
and Layer V specialization for motor output processing.

Key features:
- 6-layer cortical organization with motor specialization
- Layer V pyramidal neurons for motor output
- Integration with Amygdala for adrenaline effects
- Motor planning and execution areas
- Energy-dependent motor precision
"""

import numpy as np
from typing import Dict, List, Tuple, Optional, Union
from dataclasses import dataclass
from enum import Enum

from anatomy.base.neuron import Neuron, NeuronConfig, NeuronPopulation
from anatomy.limbic.amygdala import Amygdala


class MotorAreaType(Enum):
    """Types of motor areas in Frontal Lobe"""
    PREMOTOR = "Premotor"      # Motor planning and coordination
    MOTOR = "Motor"           # Primary motor execution
    PREFRONTAL = "Prefrontal"  # Executive function and decision making


@dataclass
class MotorConfig:
    """Configuration for motor processing"""
    layer_v_density: float = 1.5  # Higher density for motor output
    pyramidal_size: float = 120.0  # Larger pyramidal neurons in Layer V
    motor_threshold_modifier: float = 0.8  # Lower threshold for motor response
    adrenaline_sensitivity: float = 0.3  # Sensitivity to adrenaline effects
    energy_dependency: float = 0.4  # Energy impact on motor precision


class PremotorArea:
    """Premotor area for motor planning and coordination"""
    
    def __init__(self, position: np.ndarray, size: Tuple[int, int] = (30, 30)):
        self.position = position
        self.size = size
        self.populations = {}
        
        self._initialize_layers()
    
    def _generate_layer_positions(self, base_position: np.ndarray, num_neurons: int) -> np.ndarray:
        """Generate 3D positions for neurons in a layer"""
        if num_neurons == 0:
            return np.array([])
        
        # Create a grid pattern for the layer
        grid_size = int(np.ceil(np.sqrt(num_neurons)))
        positions = []
        
        for i in range(num_neurons):
            x = base_position[0] + (i % grid_size) * 2.0
            y = base_position[1] + (i // grid_size) * 2.0
            z = base_position[2] + np.random.uniform(-1.0, 1.0)
            positions.append([x, y, z])
        
        return np.array(positions)
    
    def _initialize_layers(self):
        """Initialize 6-layer organization with motor planning specialization"""
        base_pos = self.position
        
        # Layer I (Molecular) - feedback integration
        layer1_config = NeuronConfig(
            layer_id=0,  # Layer I
            threshold_potential=-62.0,
            base_energy_consumption=0.004, firing_energy_cost=0.04
        )
        layer1_positions = self._generate_layer_positions(base_pos + np.array([0, 0, 2.0]), 
                                                         int(self.size[0] * self.size[1] * 0.08))
        self.populations['layer1'] = NeuronPopulation(
            layer1_positions,
            config=layer1_config
        )
        
        # Layer II/III (Association) - motor planning
        layer23_config = NeuronConfig(
            layer_id=1,  # Layer II
            threshold_potential=-56.0,
            base_energy_consumption=0.007, firing_energy_cost=0.07
        )
        layer23_positions = self._generate_layer_positions(base_pos + np.array([0, 0, 1.5]), 
                                                          int(self.size[0] * self.size[1] * 0.25))
        self.populations['layer23'] = NeuronPopulation(
            layer23_positions,
            config=layer23_config
        )
        
        # Layer IV (Input) - sensory integration
        layer4_config = NeuronConfig(
            layer_id=3,  # Layer IV
            threshold_potential=-53.0,
            base_energy_consumption=0.008, firing_energy_cost=0.08
        )
        layer4_positions = self._generate_layer_positions(base_pos + np.array([0, 0, 1.0]), 
                                                         int(self.size[0] * self.size[1] * 0.30))
        self.populations['layer4'] = NeuronPopulation(
            layer4_positions,
            config=layer4_config
        )
        
        # Layer V (Output) - motor command generation
        layer5_config = NeuronConfig(
            layer_id=4,  # Layer V
            threshold_potential=-52.0,  # Lower threshold for motor response
            base_energy_consumption=0.009, firing_energy_cost=0.09
        )
        layer5_positions = self._generate_layer_positions(base_pos + np.array([0, 0, 0.5]), 
                                                         int(self.size[0] * self.size[1] * 0.25))
        self.populations['layer5'] = NeuronPopulation(
            layer5_positions,
            config=layer5_config
        )
        
        # Layer VI (Feedback) - thalamic regulation
        layer6_config = NeuronConfig(
            layer_id=5,  # Layer VI
            threshold_potential=-58.0,
            base_energy_consumption=0.006, firing_energy_cost=0.06
        )
        layer6_positions = self._generate_layer_positions(base_pos + np.array([0, 0, 0.0]), 
                                                         int(self.size[0] * self.size[1] * 0.12))
        self.populations['layer6'] = NeuronPopulation(
            layer6_positions,
            config=layer6_config
        )
    
    def process_input(self, sensory_input: Dict[str, float], neuromodulators: Dict[str, float]):
        """Process sensory input for motor planning"""
        # Layer IV receives sensory input
        layer4 = self.populations['layer4']
        
        # Convert sensory input to neural activity
        sensory_strength = sensory_input.get('intensity', 0.0) * 80.0
        
        for neuron in layer4.neurons:
            modulated_input = sensory_strength
            
            # Acetylcholine enhances sensory-motor integration
            if 'acetylcholine' in neuromodulators:
                modulated_input *= (1.0 + neuromodulators['acetylcholine'] * 0.3)
            
            neuron.receive_input(modulated_input, neuromodulators)
            neuron.update(0, neuromodulators)
        
        # Feedforward processing through layers
        self._process_interlayer_connections(neuromodulators)
    
    def _process_interlayer_connections(self, neuromodulators: Dict[str, float]):
        """Process connections between premotor layers"""
        # Layer IV → Layer II/III (sensory to planning)
        layer4 = self.populations['layer4']
        layer23 = self.populations['layer23']
        
        layer4_activity = layer4.get_average_activity()
        
        for neuron in layer23.neurons:
            input_strength = layer4_activity * 60.0
            
            # Dopamine enhances motor planning
            if 'dopamine' in neuromodulators:
                input_strength *= (1.0 + neuromodulators['dopamine'] * 0.2)
            
            neuron.receive_input(input_strength, neuromodulators)
            neuron.update(0, neuromodulators)
        
        # Layer II/III → Layer V (planning to execution)
        layer5 = self.populations['layer5']
        
        layer23_activity = layer23.get_average_activity()
        
        for neuron in layer5.neurons:
            input_strength = layer23_activity * 70.0
            
            # Serotonin modulates motor execution
            if 'serotonin' in neuromodulators:
                input_strength *= (1.0 - neuromodulators['serotonin'] * 0.1)
            
            neuron.receive_input(input_strength, neuromodulators)
            neuron.update(0, neuromodulators)
    
    def get_motor_command(self) -> float:
        """Get motor command signal from Layer V"""
        layer5 = self.populations['layer5']
        return layer5.get_average_activity()
    
    def get_planning_activity(self) -> Dict[str, float]:
        """Get premotor planning activity levels"""
        return {
            'sensory_integration': self.populations['layer4'].get_average_activity(),
            'motor_planning': self.populations['layer23'].get_average_activity(),
            'motor_command': self.get_motor_command(),
            'feedback_activity': self.populations['layer6'].get_average_activity()
        }


class MotorArea:
    """Primary motor area for direct motor execution"""
    
    def __init__(self, position: np.ndarray, size: Tuple[int, int] = (35, 35), config: Optional[MotorConfig] = None):
        self.position = position
        self.size = size
        self.config = config or MotorConfig()
        self.populations = {}
        
        self._initialize_layers()
    
    def _generate_layer_positions(self, base_position: np.ndarray, num_neurons: int) -> np.ndarray:
        """Generate 3D positions for neurons in a layer"""
        if num_neurons == 0:
            return np.array([])
        
        # Create a grid pattern for the layer
        grid_size = int(np.ceil(np.sqrt(num_neurons)))
        positions = []
        
        for i in range(num_neurons):
            x = base_position[0] + (i % grid_size) * 2.0
            y = base_position[1] + (i // grid_size) * 2.0
            z = base_position[2] + np.random.uniform(-1.0, 1.0)
            positions.append([x, y, z])
        
        return np.array(positions)
    
    def _initialize_layers(self):
        """Initialize 6-layer organization with motor execution specialization"""
        base_pos = self.position
        
        # Layer I (Molecular) - minimal
        layer1_config = NeuronConfig(
            layer_id=0,  # Layer I
            threshold_potential=-60.0,
            base_energy_consumption=0.004, firing_energy_cost=0.04
        )
        layer1_positions = self._generate_layer_positions(base_pos + np.array([0, 0, 2.0]), 
                                                         int(self.size[0] * self.size[1] * 0.06))
        self.populations['layer1'] = NeuronPopulation(
            layer1_positions,
            config=layer1_config
        )
        
        # Layer II/III (Association) - motor coordination
        layer23_config = NeuronConfig(
            layer_id=1,  # Layer II
            threshold_potential=-55.0,
            base_energy_consumption=0.007, firing_energy_cost=0.07
        )
        layer23_positions = self._generate_layer_positions(base_pos + np.array([0, 0, 1.5]), 
                                                          int(self.size[0] * self.size[1] * 0.20))
        self.populations['layer23'] = NeuronPopulation(
            layer23_positions,
            config=layer23_config
        )
        
        # Layer IV (Input) - premotor input
        layer4_config = NeuronConfig(
            layer_id=3,  # Layer IV
            threshold_potential=-54.0,
            base_energy_consumption=0.008, firing_energy_cost=0.08
        )
        layer4_positions = self._generate_layer_positions(base_pos + np.array([0, 0, 1.0]), 
                                                         int(self.size[0] * self.size[1] * 0.25))
        self.populations['layer4'] = NeuronPopulation(
            layer4_positions,
            config=layer4_config
        )
        
        # Layer V (Output) - motor execution with high density
        layer5_config = NeuronConfig(
            layer_id=4,  # Layer V
            threshold_potential=-50.0,  # Very low threshold for motor response
            base_energy_consumption=0.012, firing_energy_cost=0.12  # High energy consumption
        )
        layer5_positions = self._generate_layer_positions(base_pos + np.array([0, 0, 0.5]), 
                                                         int(self.size[0] * self.size[1] * 0.35 * self.config.layer_v_density))
        self.populations['layer5'] = NeuronPopulation(
            layer5_positions,
            config=layer5_config
        )
        
        # Layer VI (Feedback) - motor regulation
        layer6_config = NeuronConfig(
            layer_id=5,  # Layer VI
            threshold_potential=-57.0,
            base_energy_consumption=0.006, firing_energy_cost=0.06
        )
        layer6_positions = self._generate_layer_positions(base_pos + np.array([0, 0, 0.0]), 
                                                         int(self.size[0] * self.size[1] * 0.14))
        self.populations['layer6'] = NeuronPopulation(
            layer6_positions,
            config=layer6_config
        )
    
    def process_premotor_input(self, premotor_command: float, neuromodulators: Dict[str, float], 
                             energy_level: float, adrenaline_level: float):
        """Process premotor command for execution"""
        # Layer IV receives premotor input
        layer4 = self.populations['layer4']
        
        # Convert premotor command to neural activity
        input_strength = premotor_command * 90.0
        
        for neuron in layer4.neurons:
            modulated_input = input_strength
            
            # Apply neuromodulatory effects
            if 'acetylcholine' in neuromodulators:
                modulated_input *= (1.0 + neuromodulators['acetylcholine'] * 0.4)
            
            if 'dopamine' in neuromodulators:
                modulated_input *= (1.0 + neuromodulators['dopamine'] * 0.3)
            
            neuron.receive_input(modulated_input, neuromodulators)
            neuron.update(0, neuromodulators)
        
        # Feedforward processing with energy and adrenaline effects
        self._process_interlayer_connections(neuromodulators, energy_level, adrenaline_level)
    
    def _process_interlayer_connections(self, neuromodulators: Dict[str, float], 
                                      energy_level: float, adrenaline_level: float):
        """Process connections between motor layers with energy/adrenaline effects"""
        # Layer IV → Layer II/III
        layer4 = self.populations['layer4']
        layer23 = self.populations['layer23']
        
        layer4_activity = layer4.get_average_activity()
        
        # Energy-dependent processing
        energy_modifier = max(0.1, energy_level)  # Prevent complete shutdown
        
        for neuron in layer23.neurons:
            input_strength = layer4_activity * 70.0 * energy_modifier
            
            # Adrenaline effects on coordination
            if adrenaline_level > 0.5:
                # High adrenaline reduces coordination precision
                input_strength *= (1.0 - (adrenaline_level * 0.3))
            
            neuron.receive_input(input_strength, neuromodulators)
            neuron.update(0, neuromodulators)
        
        # Layer II/III → Layer V (motor execution)
        layer5 = self.populations['layer5']
        
        layer23_activity = layer23.get_average_activity()
        
        for neuron in layer5.neurons:
            input_strength = layer23_activity * 80.0 * energy_modifier
            
            # Adrenaline tremor effect on motor precision
            if adrenaline_level > 0.7:
                # High adrenaline causes motor tremor
                tremor_factor = 1.0 + (adrenaline_level * 0.5)
                input_strength *= tremor_factor
            
            # Serotonin stabilization
            if 'serotonin' in neuromodulators:
                input_strength *= (1.0 - neuromodulators['serotonin'] * 0.2)
            
            neuron.receive_input(input_strength, neuromodulators)
            neuron.update(0, neuromodulators)
    
    def get_motor_output(self) -> float:
        """Get final motor output from Layer V"""
        layer5 = self.populations['layer5']
        return layer5.get_average_activity()
    
    def get_motor_state(self) -> Dict[str, float]:
        """Get motor execution state"""
        layer5 = self.populations['layer5']
        
        return {
            'premotor_integration': self.populations['layer4'].get_average_activity(),
            'motor_coordination': self.populations['layer23'].get_average_activity(),
            'motor_output': self.get_motor_output(),
            'layer_v_activity': layer5.get_average_activity(),
            'energy_consumption': layer5.get_average_energy() * 0.1,  # High energy use
            'motor_precision': self._calculate_motor_precision()
        }
    
    def _calculate_motor_precision(self) -> float:
        """Calculate motor precision based on Layer V activity patterns"""
        layer5 = self.populations['layer5']
        
        # Precision based on synchronized firing
        firing_neurons = [n for n in layer5.neurons if n.is_firing]
        if not firing_neurons:
            return 0.0
        
        # Calculate synchronization (simplified)
        avg_potential = np.mean([n.membrane_potential for n in firing_neurons])
        potential_variance = np.var([n.membrane_potential for n in firing_neurons])
        
        # Lower variance = higher precision
        # Fix: Use a small epsilon to prevent division issues and ensure proper scaling
        precision = max(0.0, 1.0 - (potential_variance / max(1000.0, potential_variance + 1.0)))
        
        return precision


class PrefrontalArea:
    """Prefrontal area for executive function and decision making"""
    
    def __init__(self, position: np.ndarray, size: Tuple[int, int] = (25, 25)):
        self.position = position
        self.size = size
        self.populations = {}
        
        self._initialize_layers()
    
    def _generate_layer_positions(self, base_position: np.ndarray, num_neurons: int) -> np.ndarray:
        """Generate 3D positions for neurons in a layer"""
        if num_neurons == 0:
            return np.array([])
        
        # Create a grid pattern for the layer
        grid_size = int(np.ceil(np.sqrt(num_neurons)))
        positions = []
        
        for i in range(num_neurons):
            x = base_position[0] + (i % grid_size) * 2.0
            y = base_position[1] + (i // grid_size) * 2.0
            z = base_position[2] + np.random.uniform(-1.0, 1.0)
            positions.append([x, y, z])
        
        return np.array(positions)
    
    def _initialize_layers(self):
        """Initialize 6-layer organization with executive function specialization"""
        base_pos = self.position
        
        # All layers have higher complexity for executive function
        for layer_id in range(6):
            config = NeuronConfig(
                layer_id=layer_id,
                threshold_potential=-55.0 + (layer_id * 0.3),
                base_energy_consumption=0.008 + (layer_id * 0.001),
                firing_energy_cost=0.08 + (layer_id * 0.001)
            )
            
            population_size = int(self.size[0] * self.size[1] * [0.05, 0.15, 0.30, 0.30, 0.15, 0.05][layer_id])
            
            layer_positions = self._generate_layer_positions(
                base_pos + np.array([0, 0, 2.0 - (layer_id * 0.3)]),
                population_size
            )
            
            self.populations[f'layer{layer_id + 1}'] = NeuronPopulation(
                layer_positions,
                config=config
            )
    
    def process_decision_input(self, inputs: Dict[str, float], neuromodulators: Dict[str, float]):
        """Process decision-making inputs"""
        # Complex integration across all layers
        total_input = sum(inputs.values()) * 50.0
        
        for population in self.populations.values():
            for neuron in population.neurons:
                modulated_input = total_input
                
                # Dopamine enhances decision making
                if 'dopamine' in neuromodulators:
                    modulated_input *= (1.0 + neuromodulators['dopamine'] * 0.4)
                
                # Serotonin stabilizes decisions
                if 'serotonin' in neuromodulators:
                    modulated_input *= (1.0 + neuromodulators['serotonin'] * 0.2)
                
                neuron.receive_input(modulated_input, neuromodulators)
                neuron.update(0, neuromodulators)
    
    def get_decision_output(self) -> Dict[str, float]:
        """Get decision-making outputs"""
        return {
            'executive_activity': self.populations['layer2'].get_average_activity(),
            'decision_confidence': self.populations['layer3'].get_average_activity(),
            'inhibitory_control': self.populations['layer5'].get_average_activity(),
            'working_memory': self.populations['layer4'].get_average_activity()
        }


class FrontalLobe:
    """Complete Frontal Lobe with motor and executive areas"""
    
    def __init__(self, position: np.ndarray = np.array([0.0, -30.0, 0.0])):
        self.position = position
        self.premotor = None
        self.motor = None
        self.prefrontal = None
        self.amygdala_connection = None
        
        self._initialize_areas()
    
    def _initialize_areas(self):
        """Initialize all frontal areas with proper positioning"""
        base_pos = self.position
        
        # Premotor area - planning and coordination
        premotor_pos = base_pos + np.array([-15.0, 0.0, 0.0])
        self.premotor = PremotorArea(premotor_pos, size=(30, 30))
        
        # Motor area - execution (center)
        motor_pos = base_pos + np.array([0.0, 0.0, 0.0])
        self.motor = MotorArea(motor_pos, size=(35, 35))
        
        # Prefrontal area - executive function
        prefrontal_pos = base_pos + np.array([15.0, 0.0, 0.0])
        self.prefrontal = PrefrontalArea(prefrontal_pos, size=(25, 25))
    
    def process_sensory_input(self, sensory_input: Dict[str, float], neuromodulators: Dict[str, float]):
        """Process sensory input through the frontal hierarchy"""
        # 1. Premotor processing (planning)
        self.premotor.process_input(sensory_input, neuromodulators)
        
        # 2. Motor execution
        premotor_command = self.premotor.get_motor_command()
        
        # Get energy and adrenaline levels from neuromodulators
        energy_level = neuromodulators.get('energy', 0.5)  # Default to medium energy
        adrenaline_level = neuromodulators.get('norepinephrine', 0.0)  # Use norepinephrine as adrenaline proxy
        
        self.motor.process_premotor_input(premotor_command, neuromodulators, energy_level, adrenaline_level)
        
        # 3. Prefrontal oversight
        decision_inputs = {
            'sensory': sensory_input.get('intensity', 0.0),
            'motor': self.motor.get_motor_output(),
            'premotor': premotor_command
        }
        self.prefrontal.process_decision_input(decision_inputs, neuromodulators)
    
    def get_motor_output(self) -> float:
        """Get final motor output from Layer V"""
        return self.motor.get_motor_output()
    
    def get_frontal_outputs(self) -> Dict[str, Union[Dict, float]]:
        """Get outputs from all frontal areas"""
        return {
            'premotor': self.premotor.get_planning_activity(),
            'motor': self.motor.get_motor_state(),
            'prefrontal': self.prefrontal.get_decision_output(),
            'final_output': self.get_motor_output()
        }
    
    def get_motor_precision(self) -> float:
        """Get overall motor precision"""
        return self.motor.get_motor_state()['motor_precision']
    
    def reset(self):
        """Reset all frontal areas"""
        if self.premotor:
            for population in self.premotor.populations.values():
                for neuron in population.neurons:
                    neuron.reset()
        
        if self.motor:
            for population in self.motor.populations.values():
                for neuron in population.neurons:
                    neuron.reset()
        
        if self.prefrontal:
            for population in self.prefrontal.populations.values():
                for neuron in population.neurons:
                    neuron.reset()


# Convenience functions for specialized frontal implementations
def create_motor_focused_frontal(position: np.ndarray = None) -> FrontalLobe:
    """Create a frontal lobe optimized for motor execution"""
    if position is None:
        position = np.array([0.0, -30.0, 0.0])
    
    frontal = FrontalLobe(position)
    
    # Enhance motor area
    frontal.motor.size = (45, 45)
    frontal.motor.config.layer_v_density = 2.0  # Very high density
    
    return frontal


def create_executive_focused_frontal(position: np.ndarray = None) -> FrontalLobe:
    """Create a frontal lobe optimized for executive function"""
    if position is None:
        position = np.array([0.0, -30.0, 0.0])
    
    frontal = FrontalLobe(position)
    
    # Enhance prefrontal area
    frontal.prefrontal.size = (35, 35)
    
    return frontal


def create_balanced_frontal(position: np.ndarray = None) -> FrontalLobe:
    """Create a balanced frontal lobe with all areas equally developed"""
    if position is None:
        position = np.array([0.0, -30.0, 0.0])
    
    frontal = FrontalLobe(position)
    
    # Balanced enhancement
    frontal.premotor.size = (35, 35)
    frontal.motor.size = (40, 40)
    frontal.prefrontal.size = (30, 30)
    
    return frontal