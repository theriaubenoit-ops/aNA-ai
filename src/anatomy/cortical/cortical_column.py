#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cortical Lobe Base Implementation for aNA AI Project v5.4

Communicates with: Input: (<- Thalamus IV) | Input/Output: (<-> Hippocampus) | Output: (-> Thalamus VI Feedback)

This module implements the 6-layer cortical architecture for all brain lobes.
Each lobe processes signals through the biological layers: L4 → L2/3 → L5.

Key Features:
- 6-layer cortical organization (L1, L2/3, L4, L5, L6)
- Signal cascade with biological efficiency factors
- Acetylcholine attention mechanism in L1
- Memory access port in L2/3 for future hippocampus integration
- Real-time precision monitoring for dashboard display

Architecture, concept and supervision: Benoit Theriault
Collaboration, research and code: Gemini, Cline
"""

import numpy as np
import sys
import os
from typing import Dict, Any, Optional
from dataclasses import dataclass

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.config import get_config
from src.registry import ORGANS
from src.anatomy.base.neuron import Neuron, NeuronConfig 

@dataclass
class LayerConfig:
    """Configuration for cortical layers"""
    efficiency: float = 1.0
    name: str = "Layer"
    description: str = "Cortical layer"


class LayerI:
    """
    Layer I (Molecular Layer) (Modulation Noradrénergique)
    """
    def __init__(self):
        self.config = LayerConfig(efficiency=1.0, name="Layer I")
        self.attention_boost = 0.0
        self.trauma_impact = 0.0 # Noradrénaline
    
    def integrate_neuromodulators(self, neuromodulators, recognition_score=0.0):
        config = get_config()
        ach = neuromodulators.get('acetylcholine', 0.0) if isinstance(neuromodulators, dict) else neuromodulators

        base_boost = ach * config.get('ACH_ATTENTION_MULTIPLIER', 1.5)
        novelty_factor = 1.0 - recognition_score
        
        # On ajoute un +0.01 pour éviter le silence total (le division par zéro)
        self.attention_gain = (base_boost * (1.0 + novelty_factor)) + config.get('ATTENTION_MIN_GAIN', 0.01)
        return self.attention_gain

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
        config = get_config()
        self.config = LayerConfig(
            efficiency= config.get('L4_EFFICIENCY', 0.90),
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
        config = get_config()
        self.config = LayerConfig(
            efficiency=config.get('L23_EFFICIENCY', 0.85),
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
        config = get_config()
        self.config = LayerConfig(
            efficiency=config.get('L5_EFFICIENCY', 0.85),
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
        config = get_config()
        self.config = LayerConfig(
            efficiency=config.get('L6_EFFICIENCY', 0.80),
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


class CorticalLobe: # La classe de base
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

    def __init__(self, position=None, hippo_unit=None, **kwargs):
        # 1. Gestion de la position 
        self.position = position if position is not None else np.array([0,0,0])

        # 2. Capture de l'hippocampe (v5.3)
        self.hippo_unit = hippo_unit or kwargs.get('hippo_unit', None)
        
        # Initialize all layers
        self.neurons = []
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
    
    def process_through_layers(self, input_signal: float, neuromodulators: Dict[str, float], recognition_score: float = 0.5) -> float:
        """
        Process signal through all cortical layers.
        
        Args:
            input_signal: Input signal from thalamus or previous lobe
            neuromodulators: Current neuromodulator levels
            
        Returns:
            Final output signal after all layers
        """

        # The signal must be a scalar value processed by the thalamus. If it's not, we return a default value (0.0) to avoid errors in processing.
        if not isinstance(input_signal, (int, float)):
            # Logique de repli ou erreur si le format n'est pas respecté
            return 0.0
    
        # Step 1: Layer I - Neuromodulator integration and attention boost
        self.attention_boost = self.layer1.integrate_neuromodulators(
            neuromodulators, 
            recognition_score=recognition_score
        )
        
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
        config = get_config()
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
                'expected_cascade': config.get('BIOLOGICAL_ACCURACY_TARGET', 0.65),  # la valeur attendue du produit des efficacités 0.90 * 0.85 * 0.85
                'biological_accuracy': abs((self.l5_output / self.layer4.input_activity) - config.get('BIOLOGICAL_ACCURACY_TARGET', 0.65)) if self.layer4.input_activity > 0 else 1.0
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
    
    async def process_input(self, signal_data: str, hippo_unit, neuromodulators: Dict[str, float] = None) -> Dict[str, float]:
        """
        Traitement : Cascade L4 -> L2/3 -> L5 avec modulation chimique.
        """
        config = get_config()

        if neuromodulators:
            self.layer1.integrate_neuromodulators(neuromodulators)
        
        # 1. Calcul du gain global via la Layer I
        current_efficiency = self.layer1.config.efficiency
        
        # 2. Simulation de l'activité neuronale avec impact de la Noradrénaline
        nora = neuromodulators.get("noradrenaline", 0.0) if neuromodulators else 0.0
        
        for n in self.neurons:
            # En cas de trauma (nora > 0.6), on force la myélinisation (Gravure Flash)
            n.is_firing = True
            if nora > config.get('TRAUMA_NORA_THRESHOL', 0.6):
                # Accélération de la plasticité synaptique
                n.myelination_level = min(1.0, n.myelination_level + config.get('FLASH_MYELIN_BOOST', 0.05))
            n._update_myelination()
            n.is_firing = False
            
        # 3. Évaluation via l'unité Hippocampique (Pattern Separation/Completion)
        # La Noradrénaline réduit la tolérance à l'erreur (on veut de la précision brute)
        prediction_error = await hippo_unit.evaluate_prediction(signal_data)
        
        # Plus il y a de trauma, plus le score de reconnaissance est "marqué"
        recognition_score = 1.0 - prediction_error

        self.l6_state = min(1.0, recognition_score)

        return {
            "recognition": recognition_score,
            "l6_feedback": self.l6_state
        }


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

class SimplifiedCorticalColumn:
    def __init__(self, column_id: str):
        self.column_id = column_id
        # Création d'une petite population de neurones représentative
        self.neurons = [Neuron(position=np.array([0, 0, 0])) for _ in range(10)]
        self.layers = {"L4": 0.0, "L23": 0.0, "L5": 0.0, "L6": 0.0}

    def get_average_myelination(self) -> float:
        """Calcule la trace physique (myéline) laissée par l'apprentissage"""
        if not self.neurons:
            return 0.0
        return sum(n.myelination_level for n in self.neurons) / len(self.neurons)

    async def process_input(self, signal_data: str, hippo_unit) -> Dict[str, float]:
        # Simulation de l'activité neuronale lors du passage du signal
        for n in self.neurons:
            # On simule un cycle d'update pour que la myéline progresse si le neurone "tire"
            n.is_firing = True # aNA s'active
            n._update_myelination()
            n.is_firing = False
            
        # ... (le reste de ton code process_input existant) ...
        prediction_error = await hippo_unit.evaluate_prediction(signal_data)
        recognition_score = 1.0 - prediction_error
        self.layers["L6"] = recognition_score
        
        return {
            "recognition": recognition_score,
            "l6_feedback": self.layers["L6"]
        }

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
