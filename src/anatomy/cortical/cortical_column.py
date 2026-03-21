#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cortical Lobe Base Implementation for aNA v5.0

This module implements the 6-layer cortical architecture for all brain lobes.
Each lobe processes signals through the biological layers: L4 → L2/3 → L5.

Key Features:
- 6-layer cortical organization (L1, L2/3, L4, L5, L6)
- Signal cascade with biological efficiency factors
- Acetylcholine attention mechanism in L1
- Memory access port in L2/3 for future hippocampus integration
- Real-time precision monitoring for dashboard display

Architecture, concept and supervision: Benoit Theriault
Collaboration, research and code: Gemini, Cline and GPT
"""

import numpy as np
from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class LayerConfig:
    """Configuration for cortical layers"""
    efficiency: float = 1.0
    name: str = "Layer"
    description: str = "Cortical layer"


class LayerI:
    """
    Layer I (Molecular Layer)
    
    Functions:
    - Neuromodulator integration (dopamine, acetylcholine, serotonin)
    - Interneuron modulation
    - Feedback from higher cortical areas
    - Attention mechanism via acetylcholine
    """
    
    def __init__(self):
        self.config = LayerConfig(
            efficiency=1.0,
            name="Layer I",
            description="Molecular Layer - Neuromodulator Integration"
        )
        self.neuromodulators = {}
        self.attention_boost = 1.0
    
    def integrate_neuromodulators(self, neuromodulators: Dict[str, float]) -> float:
        """
        Integrate neuromodulators to calculate attention boost.
        
        Args:
            neuromodulators: Current neuromodulator levels
            
        Returns:
            Attention boost factor (1.0 = no boost, >1.0 = attention enhancement)
        """
        self.neuromodulators = neuromodulators
        
        # Acetylcholine enhances attention and repairs signal loss
        ach_level = neuromodulators.get('acetylcholine', 0.1)
        dopamine_level = neuromodulators.get('dopamine', 0.1)
        
        # Acetylcholine provides attention boost (up to 30% signal enhancement)
        ach_boost = 1.0 + (ach_level * 0.3)
        
        # Dopamine enhances processing efficiency
        dopamine_boost = 1.0 + (dopamine_level * 0.1)
        
        # Combined attention boost
        self.attention_boost = ach_boost * dopamine_boost
        
        return self.attention_boost


class LayerIV:
    """
    Layer IV (Granular Input Layer)
    
    Functions:
    - Thalamic input reception
    - Initial signal processing
    - Sensory feature extraction
    - 90% efficiency for thalamic input processing
    """
    
    def __init__(self):
        self.config = LayerConfig(
            efficiency=0.90,
            name="Layer IV",
            description="Granular Input Layer - Thalamic Reception"
        )
        self.input_activity = 0.0
        self.processed_signal = 0.0
    
    def process_input(self, input_signal: float) -> float:
        """
        Process thalamic input through Layer IV.
        
        Args:
            input_signal: Raw input signal from thalamus
            
        Returns:
            Processed signal after Layer IV efficiency
        """
        self.input_activity = input_signal
        self.processed_signal = input_signal * self.config.efficiency
        return self.processed_signal


class LayerII_III:
    """
    Layer II/III (Association Layers)
    
    Functions:
    - Association and pattern recognition
    - Signal integration and processing
    - Memory access port for future hippocampus connection
    - LTP/LTD mechanisms
    - 85% efficiency for association processing
    """
    
    def __init__(self):
        self.config = LayerConfig(
            efficiency=0.85,
            name="Layer II/III",
            description="Association Layers - Pattern Recognition"
        )
        self.input_activity = 0.0
        self.association_activity = 0.0
        self.memory_access_port = None  # Future hippocampus connection
    
    def process_association(self, input_signal: float) -> float:
        """
        Process signal through association layers.
        
        Args:
            input_signal: Signal from Layer IV
            
        Returns:
            Association-processed signal
        """
        self.input_activity = input_signal
        self.association_activity = input_signal * self.config.efficiency
        return self.association_activity
    
    def connect_memory(self, hippocampus: Any):
        """Connect to hippocampus for future memory access"""
        self.memory_access_port = hippocampus
    
    def get_memory_access_status(self) -> str:
        """Get status of memory access port"""
        if self.memory_access_port:
            return "CONNECTED"
        else:
            return "READY"


class LayerV:
    """
    Layer V (Pyramidal Output Layer)
    
    Functions:
    - Motor output generation
    - Final processing before transmission
    - Corticospinal/corticobulbar projections
    - 85% efficiency for output generation
    """
    
    def __init__(self):
        self.config = LayerConfig(
            efficiency=0.85,
            name="Layer V",
            description="Pyramidal Output Layer - Motor Planning"
        )
        self.input_activity = 0.0
        self.output_activity = 0.0
    
    def generate_output(self, input_signal: float) -> float:
        """
        Generate final output through Layer V.
        
        Args:
            input_signal: Signal from Layer II/III
            
        Returns:
            Final output signal
        """
        self.input_activity = input_signal
        self.output_activity = input_signal * self.config.efficiency
        return self.output_activity


class LayerVI:
    """
    Layer VI (Pyramidal Feedback Layer)
    
    Functions:
    - Feedback to thalamus
    - Modulatory control
    - Attention regulation
    - 80% efficiency for feedback signals
    """
    
    def __init__(self):
        self.config = LayerConfig(
            efficiency=0.80,
            name="Layer VI",
            description="Pyramidal Feedback Layer - Thalamic Modulation"
        )
        self.input_activity = 0.0
        self.feedback_signal = 0.0
    
    def generate_feedback(self, input_signal: float) -> float:
        """
        Generate feedback signal to thalamus.
        
        Args:
            input_signal: Signal from Layer V
            
        Returns:
            Feedback signal to thalamus
        """
        self.input_activity = input_signal
        self.feedback_signal = input_signal * self.config.efficiency
        return self.feedback_signal


class CorticalLobe:
    """
    Base class for all cortical lobes with 6-layer architecture.
    
    Signal Flow: Input → L4 → L2/3 → L5 → Output
    Feedback: L6 → Thalamus
    
    Key Features:
    - Real-time precision monitoring
    - Acetylcholine attention mechanism
    - Memory access port preparation
    - Biological efficiency cascades
    """
    
    def __init__(self, position: np.ndarray):
        self.position = position
        
        # Initialize all layers
        self.layer1 = LayerI()
        self.layer4 = LayerIV()
        self.layer23 = LayerII_III()
        self.layer5 = LayerV()
        self.layer6 = LayerVI()
        
        # Real-time monitoring variables
        self.l4_output = 0.0
        self.l23_output = 0.0
        self.l5_output = 0.0
        self.l6_feedback = 0.0
        self.precision_loss = 0.0
        self.attention_boost = 1.0
        
        # Overall lobe activity
        self.total_activity = 0.0
    
    def process_through_layers(self, input_signal: float, neuromodulators: Dict[str, float]) -> float:
        """
        Process signal through all cortical layers.
        
        Args:
            input_signal: Input signal from thalamus or previous lobe
            neuromodulators: Current neuromodulator levels
            
        Returns:
            Final output signal after all layers
        """
        # Step 1: Layer I - Neuromodulator integration and attention boost
        self.attention_boost = self.layer1.integrate_neuromodulators(neuromodulators)
        
        # Step 2: Layer IV - Input processing
        self.l4_output = self.layer4.process_input(input_signal)
        
        # Apply attention boost from Layer I to Layer IV output
        self.l4_output *= self.attention_boost
        
        # Step 3: Layer II/III - Association processing
        self.l23_output = self.layer23.process_association(self.l4_output)
        
        # Step 4: Layer V - Output generation
        self.l5_output = self.layer5.generate_output(self.l23_output)
        
        # Step 5: Layer VI - Feedback generation
        self.l6_feedback = self.layer6.generate_feedback(self.l5_output)
        
        # Calculate precision loss for dashboard
        if input_signal > 0:
            self.precision_loss = 1.0 - (self.l5_output / input_signal)
        else:
            self.precision_loss = 0.0
        
        # Update total lobe activity
        self.total_activity = self.l5_output
        
        return self.l5_output
    
    def get_layer_outputs(self) -> Dict[str, float]:
        """Get outputs from all layers for monitoring"""
        return {
            'layer1_attention': self.attention_boost,
            'layer4_output': self.l4_output,
            'layer23_output': self.l23_output,
            'layer5_output': self.l5_output,
            'layer6_feedback': self.l6_feedback,
            'precision_loss': self.precision_loss,
            'total_activity': self.total_activity
        }
    
    def get_precision_monitoring(self) -> Dict[str, Any]:
        """Get precision monitoring data for dashboard"""
        return {
            'signal_flow': {
                'input': self.layer4.input_activity,
                'l4_output': self.l4_output,
                'l23_output': self.l23_output,
                'l5_output': self.l5_output
            },
            'precision_metrics': {
                'overall_efficiency': self.l5_output / self.layer4.input_activity if self.layer4.input_activity > 0 else 0.0,
                'precision_loss': self.precision_loss,
                'attention_boost': self.attention_boost,
                'expected_cascade': 0.65,  # 0.90 * 0.85 * 0.85
                'biological_accuracy': abs((self.l5_output / self.layer4.input_activity) - 0.65) if self.layer4.input_activity > 0 else 1.0
            },
            'layer_status': {
                'l1_status': 'ACTIVE' if self.attention_boost > 1.0 else 'BASELINE',
                'l4_status': 'PROCESSING' if self.l4_output > 0 else 'IDLE',
                'l23_status': 'ASSOCIATING' if self.l23_output > 0 else 'IDLE',
                'l5_status': 'OUTPUTTING' if self.l5_output > 0 else 'IDLE',
                'l6_status': 'FEEDBACK' if self.l6_feedback > 0 else 'IDLE'
            }
        }
    
    def connect_memory(self, hippocampus: Any):
        """Connect to hippocampus via Layer II/III memory access port"""
        self.layer23.connect_memory(hippocampus)
    
    def get_memory_status(self) -> str:
        """Get memory connection status"""
        return self.layer23.get_memory_access_status()
    
    def reset(self):
        """Reset all layers to initial state"""
        self.l4_output = 0.0
        self.l23_output = 0.0
        self.l5_output = 0.0
        self.l6_feedback = 0.0
        self.precision_loss = 0.0
        self.attention_boost = 1.0
        self.total_activity = 0.0
        
        # Reset individual layers
        self.layer1.attention_boost = 1.0
        self.layer4.input_activity = 0.0
        self.layer4.processed_signal = 0.0
        self.layer23.input_activity = 0.0
        self.layer23.association_activity = 0.0
        self.layer5.input_activity = 0.0
        self.layer5.output_activity = 0.0
        self.layer6.input_activity = 0.0
        self.layer6.feedback_signal = 0.0


class CorticalColumns(CorticalLobe):
    """
    Specialized cortical lobe for visual processing.
    
    Features:
    - Enhanced Layer IV for visual input processing
    - Specialized association processing in Layer II/III
    - Optimized output generation in Layer V
    """
    
    def __init__(self, position: np.ndarray):
        super().__init__(position)
        
        # Visual-specific configurations
        self.layer4.config.efficiency = 0.92  # Enhanced visual input processing
        self.layer23.config.efficiency = 0.88  # Enhanced pattern recognition
        self.layer5.config.efficiency = 0.86   # Optimized visual output
    
    def process_visual_input(self, visual_signal: float, neuromodulators: Dict[str, float]) -> Dict[str, float]:
        """
        Process visual input through cortical layers.
        
        Args:
            visual_signal: Visual input signal from thalamus
            neuromodulators: Current neuromodulator levels
            
        Returns:
            Dictionary containing visual processing results
        """
        # Process through layers
        output = self.process_through_layers(visual_signal, neuromodulators)
        
        # Calculate visual-specific metrics
        visual_features = {
            'input_strength': visual_signal,
            'processed_output': output,
            'visual_clarity': output * self.attention_boost,
            'pattern_recognition': self.l23_output,
            'feature_extraction': self.l4_output,
            'output_precision': self.l5_output,
            'feedback_strength': self.l6_feedback,
            'attention_level': self.attention_boost,
            'processing_efficiency': self.l5_output / visual_signal if visual_signal > 0 else 0.0
        }
        
        return visual_features


class MotorCorticalLobe(CorticalLobe):
    """
    Specialized cortical lobe for motor processing.
    
    Features:
    - Enhanced Layer V for motor output generation
    - Specialized feedback mechanisms in Layer VI
    - Optimized for motor planning and execution
    """
    
    def __init__(self, position: np.ndarray):
        super().__init__(position)
        
        # Motor-specific configurations
        self.layer5.config.efficiency = 0.90  # Enhanced motor output
        self.layer6.config.efficiency = 0.85  # Enhanced feedback control
    
    def process_motor_input(self, motor_signal: float, neuromodulators: Dict[str, float]) -> Dict[str, float]:
        """
        Process motor input through cortical layers.
        
        Args:
            motor_signal: Motor planning signal
            neuromodulators: Current neuromodulator levels
            
        Returns:
            Dictionary containing motor processing results
        """
        # Process through layers
        output = self.process_through_layers(motor_signal, neuromodulators)
        
        # Calculate motor-specific metrics
        motor_features = {
            'planning_signal': motor_signal,
            'executed_output': output,
            'motor_precision': output * self.attention_boost,
            'coordination_level': self.l23_output,
            'activation_strength': self.l5_output,
            'feedback_control': self.l6_feedback,
            'attention_focus': self.attention_boost,
            'execution_efficiency': self.l5_output / motor_signal if motor_signal > 0 else 0.0
        }
        
        return motor_features


# Convenience functions for creating specialized lobes
def create_visual_cortical_lobe(position: np.ndarray) -> CorticalColumns:
    """Create a visual cortical lobe optimized for visual processing"""
    return CorticalColumns(position)


def create_motor_cortical_lobe(position: np.ndarray) -> MotorCorticalLobe:
    """Create a motor cortical lobe optimized for motor processing"""
    return MotorCorticalLobe(position)


def create_associative_cortical_lobe(position: np.ndarray) -> CorticalLobe:
    """Create a general associative cortical lobe"""
    return CorticalLobe(position)