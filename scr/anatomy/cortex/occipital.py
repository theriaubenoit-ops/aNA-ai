#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Occipital Lobe implementation for aNA v4

This module implements the Occipital Lobe with proper cortical layer organization
and retinotopic mapping from LGN (Thalamus) to V1 Layer IV.

Key features:
- Retinotopic mapping from LGN to V1 Layer IV
- NeuronPopulation classes for each visual area (V1, V2, V3)
- 6-layer cortical organization
- Layer VI feedback to Thalamus (Pulvinar)
- Visual input processing from intensity matrices
"""

import numpy as np
from typing import Dict, List, Tuple, Optional, Union
from dataclasses import dataclass
from enum import Enum

from anatomy.neuron import Neuron, NeuronConfig, NeuronPopulation
from anatomy.thalamus import ThalamicNucleusType
from core.neural_transmission import NeuralTransmission
from anatomy.cortex.lobe_base import VisualCorticalLobe


class VisualAreaType(Enum):
    """Types of visual areas"""
    V1 = "V1"          # Primary visual cortex
    V2 = "V2"          # Secondary visual area  
    V3 = "V3"          # Third visual area


@dataclass
class RetinotopicMapping:
    """Configuration for retinotopic mapping from LGN to V1"""
    lgn_size: Tuple[int, int]
    v1_size: Tuple[int, int]
    magnification_factor: float = 1.0
    eccentricity_scaling: float = 1.0


class V1Area:
    """V1 (Primary Visual Cortex) with proper layer organization"""
    
    def __init__(self, position: np.ndarray, size: Tuple[int, int] = (40, 40)):
        self.position = position
        self.size = size
        self.retinotopic_map = None
        self.populations = {}  # Layer-specific populations
        
        self._initialize_layers()
        self._setup_retinotopic_mapping()
    
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
        """Initialize 6-layer cortical organization for V1"""
        base_pos = self.position
        
        # Layer I (Molecular layer) - minimal neurons
        layer1_config = NeuronConfig(
            layer_id=0,  # Layer I
            threshold_potential=-60.0,
            base_energy_consumption=0.005, firing_energy_cost=0.05
        )
        layer1_positions = self._generate_layer_positions(base_pos + np.array([0, 0, 2.0]), 
                                                         int(self.size[0] * self.size[1] * 0.1))
        self.populations['layer1'] = NeuronPopulation(
            layer1_positions,
            config=layer1_config
        )
        
        # Layer II/III (External granular/pyramidal) - association
        layer23_config = NeuronConfig(
            layer_id=1,  # Layer II
            threshold_potential=-55.0,
            base_energy_consumption=0.008, firing_energy_cost=0.08
        )
        layer23_positions = self._generate_layer_positions(base_pos + np.array([0, 0, 1.5]), 
                                                          int(self.size[0] * self.size[1] * 0.25))
        self.populations['layer23'] = NeuronPopulation(
            layer23_positions,
            config=layer23_config
        )
        
        # Layer IV (Internal granular) - primary input from LGN
        layer4_config = NeuronConfig(
            layer_id=3,  # Layer IV
            threshold_potential=-52.0,
            base_energy_consumption=0.009, firing_energy_cost=0.09
        )
        layer4_positions = self._generate_layer_positions(base_pos + np.array([0, 0, 1.0]), 
                                                         int(self.size[0] * self.size[1] * 0.35))
        self.populations['layer4'] = NeuronPopulation(
            layer4_positions,
            config=layer4_config
        )
        
        # Layer V (Internal pyramidal) - output to subcortical
        layer5_config = NeuronConfig(
            layer_id=4,  # Layer V
            threshold_potential=-54.0,
            base_energy_consumption=0.0085, firing_energy_cost=0.085
        )
        layer5_positions = self._generate_layer_positions(base_pos + np.array([0, 0, 0.5]), 
                                                         int(self.size[0] * self.size[1] * 0.2))
        self.populations['layer5'] = NeuronPopulation(
            layer5_positions,
            config=layer5_config
        )
        
        # Layer VI (Multiform) - feedback to thalamus
        layer6_config = NeuronConfig(
            layer_id=5,  # Layer VI
            threshold_potential=-56.0,
            base_energy_consumption=0.007, firing_energy_cost=0.07
        )
        layer6_positions = self._generate_layer_positions(base_pos + np.array([0, 0, 0.0]), 
                                                         int(self.size[0] * self.size[1] * 0.1))
        self.populations['layer6'] = NeuronPopulation(
            layer6_positions,
            config=layer6_config
        )
    
    def _setup_retinotopic_mapping(self):
        """Set up retinotopic mapping from LGN to V1 Layer IV"""
        # Create mapping from LGN coordinates to V1 coordinates
        lgn_width, lgn_height = 64, 64  # Typical LGN size
        v1_width, v1_height = self.size
        
        self.retinotopic_map = RetinotopicMapping(
            lgn_size=(lgn_width, lgn_height),
            v1_size=(v1_width, v1_height),
            magnification_factor=0.625,  # V1 has higher resolution than LGN
            eccentricity_scaling=1.2    # More cortical area for fovea
        )
    
    def process_retinotopic_input(self, lgn_input: np.ndarray, neuromodulators: Dict[str, float]):
        """Process retinotopic input from LGN to V1 Layer IV"""
        # Ensure input is 2D
        if lgn_input.ndim == 1:
            # If 1D, reshape to square matrix
            size = int(np.sqrt(len(lgn_input)))
            lgn_input = lgn_input.reshape((size, size))
        
        # CASCADE BASELINE: Occipital lobe maintains small baseline activity (0.10)
        # This ensures the occipital is never completely shut down
        baseline_activity = 0.10
        
        # Calculate average input intensity (this is the thalamic output)
        avg_input = np.mean(lgn_input)
        
        # Apply occipital baseline to ensure never goes to zero
        # Formula: (Thalamic_Input + Baseline) × 0.90, clamped to biological limits
        raw_output = (avg_input + baseline_activity) * 0.90
        
        # MANAGE SATURATION: If result exceeds 1.0, clamp to 1.0
        occipital_output = min(raw_output, 1.0)
        
        # Apply neuromodulatory effects
        modulated_input = occipital_output
        
        # Acetylcholine enhances sensory processing
        if 'acetylcholine' in neuromodulators:
            modulated_input *= (1.0 + neuromodulators['acetylcholine'] * 0.2)  # Reduced modulation
        
        # Norepinephrine increases alertness
        if 'norepinephrine' in neuromodulators:
            modulated_input *= (1.0 + neuromodulators['norepinephrine'] * 0.1)  # Reduced modulation
        
        # Ensure output never goes below baseline
        modulated_input = max(modulated_input, baseline_activity)
        
        # Convert to membrane potential input
        membrane_input = modulated_input * 50.0  # Scale to appropriate range
        
        # Apply to all V1 Layer IV neurons
        for neuron in self.populations['layer4'].neurons:
            neuron.receive_input(membrane_input, neuromodulators)
            neuron.update(0, neuromodulators)
    
    def process_interlayer_connections(self, neuromodulators: Dict[str, float]):
        """Process connections between V1 layers"""
        # Layer IV → Layer II/III (feedforward)
        layer4 = self.populations['layer4']
        layer23 = self.populations['layer23']
        
        # Calculate average activity in Layer IV
        layer4_activity = layer4.get_average_activity()
        
        # Feedforward to Layer II/III - Decreasing Cascade (1.00 → 0.95)
        for neuron in layer23.neurons:
            input_strength = layer4_activity * 0.95  # Proper cascade scaling
            
            # Dopamine enhances association
            if 'dopamine' in neuromodulators:
                input_strength *= (1.0 + neuromodulators['dopamine'] * 0.1)  # Reduced modulation
            
            neuron.receive_input(input_strength, neuromodulators)
            neuron.update(0, neuromodulators)
        
        # Layer II/III → Layer V (output processing) - Decreasing Cascade (0.95 → 0.90)
        layer5 = self.populations['layer5']
        
        layer23_activity = layer23.get_average_activity()
        
        for neuron in layer5.neurons:
            input_strength = layer23_activity * 0.90  # Proper cascade scaling
            
            # Serotonin modulates output
            if 'serotonin' in neuromodulators:
                input_strength *= (1.0 - neuromodulators['serotonin'] * 0.05)  # Reduced modulation
            
            neuron.receive_input(input_strength, neuromodulators)
            neuron.update(0, neuromodulators)
        
        # Layer V → Layer VI (feedback preparation) - Decreasing Cascade (0.90 → 0.85)
        layer6 = self.populations['layer6']
        
        layer5_activity = layer5.get_average_activity()
        
        for neuron in layer6.neurons:
            input_strength = layer5_activity * 0.85  # Proper cascade scaling
            
            # Generate feedback signal based on input strength
            feedback_strength = input_strength * 0.8  # Proper scaling to 0-1 range
            neuron.feedback_signal = feedback_strength
            
            # Apply biological clamping
            input_strength = max(0.0, min(1.0, input_strength))
            feedback_strength = max(0.0, min(1.0, feedback_strength))
            
            neuron.receive_input(input_strength, neuromodulators)
            neuron.update(0, neuromodulators)
    
    def get_feedback_signal(self) -> float:
        """Get Layer VI feedback signal to Thalamus (Pulvinar)"""
        layer6 = self.populations['layer6']
        # Calculate average feedback signal from all Layer VI neurons
        if not layer6.neurons:
            return 0.0
        
        total_feedback = sum(getattr(neuron, 'feedback_signal', 0.0) for neuron in layer6.neurons)
        return total_feedback / len(layer6.neurons)
    
    def get_visual_features(self) -> Dict[str, float]:
        """Get visual feature detection results"""
        layer4 = self.populations['layer4']
        layer23 = self.populations['layer23']
        
        return {
            'basic_features': layer4.get_average_activity(),
            'complex_features': layer23.get_average_activity(),
            'output_activity': self.populations['layer5'].get_average_activity(),
            'feedback_activity': self.get_feedback_signal()
        }


class V2Area:
    """V2 (Secondary Visual Area) for shape integration"""
    
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
        """Initialize V2 layers with shape processing specialization"""
        base_pos = self.position
        
        # V2 has similar layer organization but different connectivity
        layer_ratios = [0.05, 0.15, 0.25, 0.30, 0.15, 0.10]
        
        for layer_id in range(6):
            config = NeuronConfig(
                layer_id=layer_id,
                threshold_potential=-55.0 + (layer_id * 0.5),
                base_energy_consumption=0.007 + (layer_id * 0.001),
                firing_energy_cost=0.07 + (layer_id * 0.001)
            )
            
            # Fix: Ensure layer_id is within bounds for layer_ratios
            if layer_id < len(layer_ratios):
                population_size = int(self.size[0] * self.size[1] * layer_ratios[layer_id])
            else:
                population_size = int(self.size[0] * self.size[1] * 0.10)  # Default ratio
            
            layer_positions = self._generate_layer_positions(
                base_pos + np.array([0, 0, 2.0 - (layer_id * 0.3)]),
                population_size
            )
            
            self.populations[f'layer{layer_id + 1}'] = NeuronPopulation(
                layer_positions,
                config=config
            )
    
    def process_input(self, v1_features: Dict[str, float], neuromodulators: Dict[str, float]):
        """Process V1 feature inputs"""
        # V2 integrates V1 features for shape recognition - Decreasing Cascade (0.90 → 0.85)
        input_strength = v1_features.get('complex_features', 0.0) * 0.85  # Proper cascade scaling
        
        for population in self.populations.values():
            for neuron in population.neurons:
                modulated_input = input_strength
                
                # Dopamine enhances shape learning
                if 'dopamine' in neuromodulators:
                    modulated_input *= (1.0 + neuromodulators['dopamine'] * 0.1)  # Reduced modulation
                
                # Apply biological clamping
                modulated_input = max(0.0, min(1.0, modulated_input))
                
                neuron.receive_input(modulated_input, neuromodulators)
                neuron.update(0, neuromodulators)
    
    def get_shape_outputs(self) -> Dict[str, float]:
        """Get shape recognition outputs"""
        layer23 = self.populations['layer2']
        layer4 = self.populations['layer4']
        
        return {
            'line_detection': layer23.get_average_activity(),
            'angle_detection': layer4.get_average_activity(),
            'shape_complexity': (layer23.get_average_activity() + layer4.get_average_activity()) / 2
        }


class V3Area:
    """V3 (Third Visual Area) for motion and depth processing"""
    
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
        """Initialize V3 layers with motion processing specialization"""
        base_pos = self.position
        
        # V3 layer ratios for motion processing
        layer_ratios = [0.04, 0.12, 0.20, 0.35, 0.20, 0.09]
        
        for layer_id in range(6):
            config = NeuronConfig(
                layer_id=layer_id,
                threshold_potential=-54.0 + (layer_id * 0.3),
                base_energy_consumption=0.008 + (layer_id * 0.0005),
                firing_energy_cost=0.08 + (layer_id * 0.0005)
            )
            
            # Fix: Ensure layer_id is within bounds for layer_ratios
            if layer_id < len(layer_ratios):
                population_size = int(self.size[0] * self.size[1] * layer_ratios[layer_id])
            else:
                population_size = int(self.size[0] * self.size[1] * 0.09)  # Default ratio
            
            layer_positions = self._generate_layer_positions(
                base_pos + np.array([0, 0, 2.0 - (layer_id * 0.3)]),
                population_size
            )
            
            self.populations[f'layer{layer_id + 1}'] = NeuronPopulation(
                layer_positions,
                config=config
            )
    
    def process_input(self, v2_shapes: Dict[str, float], neuromodulators: Dict[str, float]):
        """Process V2 shape inputs - Final cascade step (0.85 → 0.80)"""
        input_strength = v2_shapes.get('shape_complexity', 0.0) * 0.80  # Proper cascade scaling
        
        for population in self.populations.values():
            for neuron in population.neurons:
                modulated_input = input_strength
                
                # Norepinephrine enhances motion processing
                if 'norepinephrine' in neuromodulators:
                    modulated_input *= (1.0 + neuromodulators['norepinephrine'] * 0.1)  # Reduced modulation
                
                # Apply biological clamping
                modulated_input = max(0.0, min(1.0, modulated_input))
                
                neuron.receive_input(modulated_input, neuromodulators)
                neuron.update(0, neuromodulators)
    
    def get_motion_outputs(self) -> Dict[str, float]:
        """Get motion and depth processing outputs"""
        layer4 = self.populations['layer4']
        layer5 = self.populations['layer5']
        
        return {
            'motion_detection': layer4.get_average_activity(),
            'depth_perception': layer5.get_average_activity(),
            'motion_complexity': (layer4.get_average_activity() + layer5.get_average_activity()) / 2
        }


class OccipitalLobe:
    """Complete Occipital Lobe with 6-layer cortical architecture and V1, V2, V3 areas"""
    
    def __init__(self, position: np.ndarray = np.array([0.0, 40.0, 0.0])):
        self.position = position
        self.v1 = None
        self.v2 = None
        self.v3 = None
        self.feedback_to_thalamus = 0.0
        
        # Initialize 6-layer cortical architecture
        self.cortical_layers = VisualCorticalLobe(position)
        
        self._initialize_areas()
    
    def _initialize_areas(self):
        """Initialize all visual areas with proper positioning"""
        base_pos = self.position
        
        # V1 (Primary Visual Cortex) - receives direct LGN input
        v1_pos = base_pos + np.array([0.0, 0.0, 0.0])
        self.v1 = V1Area(v1_pos, size=(40, 40))
        
        # V2 (Secondary Visual Area) - receives V1 output
        v2_pos = base_pos + np.array([20.0, 0.0, 0.0])
        self.v2 = V2Area(v2_pos, size=(30, 30))
        
        # V3 (Third Visual Area) - receives V2 output
        v3_pos = base_pos + np.array([40.0, 0.0, 0.0])
        self.v3 = V3Area(v3_pos, size=(25, 25))
    
    def process_visual_input(self, visual_matrix: Union[np.ndarray, List[List[float]]], 
                           neuromodulators: Dict[str, float]):
        """Process visual input matrix through the occipital hierarchy"""
        # Convert input to numpy array
        if isinstance(visual_matrix, list):
            visual_matrix = np.array(visual_matrix)
        
        # Ensure input is 2D
        if visual_matrix.ndim == 1:
            # Assume square matrix
            size = int(np.sqrt(len(visual_matrix)))
            visual_matrix = visual_matrix.reshape((size, size))
        
        # 1. V1 processing - retinotopic mapping from LGN
        self.v1.process_retinotopic_input(visual_matrix, neuromodulators)
        self.v1.process_interlayer_connections(neuromodulators)
        
        # 2. V2 processing - shape integration from V1
        v1_features = self.v1.get_visual_features()
        self.v2.process_input(v1_features, neuromodulators)
        
        # 3. V3 processing - motion and depth from V2
        v2_shapes = self.v2.get_shape_outputs()
        self.v3.process_input(v2_shapes, neuromodulators)
        
        # 4. Generate feedback to Thalamus (Pulvinar)
        self.feedback_to_thalamus = self.v1.get_feedback_signal()
    
    def process_neural_transmission(self, transmission: NeuralTransmission):
        """Process neural transmission through 6-layer cortical architecture"""
        # Extract transmission data
        signal_strength = transmission.get_signal_strength()
        neuromodulators = transmission.get_neuromodulators()
        
        # Process through 6-layer cortical architecture
        cortical_output = self.cortical_layers.process_through_layers(signal_strength, neuromodulators)
        
        # Create visual matrix from cortical processing
        v1_size = self.v1.size if self.v1 else (8, 8)
        visual_matrix = np.full(v1_size, cortical_output)
        
        # Process through occipital hierarchy
        self.process_visual_input(visual_matrix, neuromodulators)
        
        # Get outputs from all areas
        outputs = self.get_visual_outputs()
        
        # Add cortical layer monitoring data
        cortical_monitoring = self.cortical_layers.get_layer_outputs()
        outputs['cortical_monitoring'] = cortical_monitoring
        
        # Add precision monitoring for dashboard
        precision_data = self.cortical_layers.get_precision_monitoring()
        outputs['precision_monitoring'] = precision_data
        
        return outputs
    
    def get_visual_outputs(self) -> Dict[str, Union[Dict, float]]:
        """Get outputs from all visual areas"""
        outputs = {
            'v1_features': self.v1.get_visual_features(),
            'v2_shapes': self.v2.get_shape_outputs(),
            'v3_motion': self.v3.get_motion_outputs(),
            'feedback_to_thalamus': self.feedback_to_thalamus
        }
        
        # CASCADE BASELINE: Ensure occipital maintains its own baseline (0.10)
        # This ensures the occipital is never completely shut down
        baseline_activity = 0.10
        
        # Apply baseline to V1 features
        if 'basic_features' in outputs['v1_features']:
            outputs['v1_features']['basic_features'] = max(outputs['v1_features']['basic_features'], baseline_activity)
        if 'complex_features' in outputs['v1_features']:
            outputs['v1_features']['complex_features'] = max(outputs['v1_features']['complex_features'], baseline_activity)
        if 'output_activity' in outputs['v1_features']:
            outputs['v1_features']['output_activity'] = max(outputs['v1_features']['output_activity'], baseline_activity)
        
        # Apply baseline to V2 shapes
        if 'line_detection' in outputs['v2_shapes']:
            outputs['v2_shapes']['line_detection'] = max(outputs['v2_shapes']['line_detection'], baseline_activity)
        if 'angle_detection' in outputs['v2_shapes']:
            outputs['v2_shapes']['angle_detection'] = max(outputs['v2_shapes']['angle_detection'], baseline_activity)
        if 'shape_complexity' in outputs['v2_shapes']:
            outputs['v2_shapes']['shape_complexity'] = max(outputs['v2_shapes']['shape_complexity'], baseline_activity)
        
        # Apply baseline to V3 motion
        if 'motion_detection' in outputs['v3_motion']:
            outputs['v3_motion']['motion_detection'] = max(outputs['v3_motion']['motion_detection'], baseline_activity)
        if 'depth_perception' in outputs['v3_motion']:
            outputs['v3_motion']['depth_perception'] = max(outputs['v3_motion']['depth_perception'], baseline_activity)
        if 'motion_complexity' in outputs['v3_motion']:
            outputs['v3_motion']['motion_complexity'] = max(outputs['v3_motion']['motion_complexity'], baseline_activity)
        
        return outputs
    
    def get_feedback_to_thalamus(self) -> float:
        """Get Layer VI feedback signal to Pulvinar (Thalamus) for focus adjustment"""
        return self.feedback_to_thalamus
    
    def get_shape_recognition(self) -> Dict[str, float]:
        """Get comprehensive shape recognition results"""
        v1_features = self.v1.get_visual_features()
        v2_shapes = self.v2.get_shape_outputs()
        v3_motion = self.v3.get_motion_outputs()
        
        return {
            'basic_features': v1_features.get('basic_features', 0.0),
            'complex_features': v1_features.get('complex_features', 0.0),
            'line_detection': v2_shapes.get('line_detection', 0.0),
            'angle_detection': v2_shapes.get('angle_detection', 0.0),
            'shape_complexity': v2_shapes.get('shape_complexity', 0.0),
            'motion_detection': v3_motion.get('motion_detection', 0.0),
            'depth_perception': v3_motion.get('depth_perception', 0.0),
            'overall_visual_confidence': (
                v1_features.get('output_activity', 0.0) * 0.3 +
                v2_shapes.get('shape_complexity', 0.0) * 0.4 +
                v3_motion.get('motion_complexity', 0.0) * 0.3
            )
        }
    
    def reset(self):
        """Reset all visual areas"""
        if self.v1:
            for population in self.v1.populations.values():
                for neuron in population.neurons:
                    neuron.reset()
        
        if self.v2:
            for population in self.v2.populations.values():
                for neuron in population.neurons:
                    neuron.reset()
        
        if self.v3:
            for population in self.v3.populations.values():
                for neuron in population.neurons:
                    neuron.reset()
        
        self.feedback_to_thalamus = 0.0


# Convenience functions for specialized occipital implementations
def create_primary_occipital(position: np.ndarray = None) -> OccipitalLobe:
    """Create an occipital lobe optimized for primary visual processing"""
    if position is None:
        position = np.array([0.0, 40.0, 0.0])
    
    occipital = OccipitalLobe(position)
    
    # Enhance V1 for detailed feature detection
    occipital.v1.size = (50, 50)
    
    return occipital


def create_associative_occipital(position: np.ndarray = None) -> OccipitalLobe:
    """Create an occipital lobe optimized for shape association"""
    if position is None:
        position = np.array([0.0, 40.0, 0.0])
    
    occipital = OccipitalLobe(position)
    
    # Enhance V2/V3 for complex processing
    occipital.v2.size = (40, 40)
    occipital.v3.size = (35, 35)
    
    return occipital


def create_full_occipital(position: np.ndarray = None) -> OccipitalLobe:
    """Create a complete occipital lobe with balanced processing"""
    if position is None:
        position = np.array([0.0, 40.0, 0.0])
    
    occipital = OccipitalLobe(position)
    
    # Balanced enhancement
    occipital.v1.size = (45, 45)
    occipital.v2.size = (35, 35)
    occipital.v3.size = (30, 30)
    
    return occipital
