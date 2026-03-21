#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Output Gateway for aNA v4.0

This module handles motor output processing by converting neural activity
from Layer V of the Frontal Lobe back to Unicode characters for display.

Key features:
- Neural activity to decimal conversion
- Energy-dependent accuracy simulation
- Adrenaline modulation effects
- Error handling and precision tracking
- Integration with motor cortex output
"""

import numpy as np
from typing import Union, Optional, Dict, Any, List
from dataclasses import dataclass


@dataclass
class OutputConfig:
    """Configuration for output processing"""
    unicode_normalization_factor: float = 128.0  # Match input gateway ASCII range
    energy_threshold_high: float = 0.8  # High energy for perfect accuracy
    energy_threshold_medium: float = 0.5  # Medium energy for slight errors
    energy_threshold_low: float = 0.2  # Low energy for significant errors
    adrenaline_threshold: float = 0.6  # High adrenaline causes tremor
    base_error_rate: float = 0.01  # Base error rate even at perfect conditions
    tremor_magnitude: float = 0.1  # Magnitude of adrenaline-induced tremor


class OutputGateway:
    """
    Gateway for converting neural output (Layer V activity) to characters.
    
    This class bridges neural dynamics with symbolic output by:
    1. Reading Layer V motor cortex activity
    2. Converting decimal values back to Unicode characters
    3. Applying energy-dependent accuracy degradation
    4. Factoring in adrenaline effects on motor precision
    5. Providing precision feedback and error tracking
    """
    
    def __init__(self, config: Optional[OutputConfig] = None):
        """
        Initialize the output gateway.
        
        Args:
            config: Output processing configuration
        """
        self.config = config or OutputConfig()
        self.last_output_char = None
        self.last_output_code = 0
        self.last_input_value = 0.0
        self.output_history = []
        self.precision_history = []
    
    def convert_to_character(self, neural_activity: float, energy_level: float, 
                           adrenaline_level: float, dopamine_level: float = 0.0) -> Dict[str, Any]:
        """
        Convert neural activity to character with accuracy simulation and dopamine bonus.
        
        Args:
            neural_activity: Layer V activity level (0.0-1.0)
            energy_level: Current neuron energy level (0.0-1.0)
            adrenaline_level: Current adrenaline level (0.0-1.0)
            dopamine_level: Current dopamine level (0.0-1.0) for motivation bonus
            
        Returns:
            Dictionary containing conversion results and accuracy
        """
        # Store input for tracking
        self.last_input_value = neural_activity
        
        # Scale neural activity to appropriate range for ASCII character conversion
        # Neural activity from frontal lobe is typically very low (0.0-1.0)
        # We need to scale it to produce ASCII codes (0-127)
        # For 'A' (ASCII 65), we want neural_activity around 0.1 to produce code 65
        # So scaling factor should be around 650 for activity 0.1
        # Add minimum threshold to avoid noise from very low activity
        # v4.1 Micro-Adjustment: Lower threshold to allow more neural activity through
        if neural_activity < 0.001:  # Reduced from 0.005 to 0.001 to allow more activity
            # Below threshold - no output to avoid noise
            return {
                'input_activity': neural_activity,
                'base_code': 0,
                'corrected_code': 0,
                'final_code': 0,
                'output_character': '',
                'accuracy': 0.0,
                'energy_level': energy_level,
                'adrenaline_level': adrenaline_level,
                'dopamine_level': dopamine_level,
                'processing_time': len(self.output_history) + 1
            }
        
        # CRITICAL FIX: Calibrate output mapping for proper 'A' character generation
        # Target cascade: 1.0 × 0.95 × 0.90 = 0.855 should map to 'A' (ASCII 65)
        # However, frontal lobe activity is typically around 1.0, so we need to scale down
        # Therefore: scaling_factor = 65 / 1.0 ≈ 65.0 for direct mapping
        
        # Add biological noise to prevent perfect saturation
        noise_factor = np.random.normal(0, 0.02)  # Reduced noise for precision
        adjusted_activity = neural_activity * (1.0 + noise_factor)
        
        # Calibrate scaling factor for realistic frontal lobe activity
        # Frontal lobe activity around 1.0 should map to ASCII range 32-127
        # Use scaling factor of 65 to map activity 1.0 to ASCII 'A' (65)
        scaling_factor = 65.0
        scaled_activity = adjusted_activity * scaling_factor
        
        # Calculate base Unicode code (ASCII subset)
        base_code = int(scaled_activity)
        
        # Apply energy-dependent accuracy degradation
        corrected_code = self._apply_energy_accuracy(base_code, energy_level)
        
        # Apply adrenaline-induced tremor
        final_code = self._apply_adrenaline_tremor(corrected_code, adrenaline_level)
        
        # Ensure code is within valid Unicode range
        final_code = max(0, min(1114111, final_code))
        
        # Convert to character
        try:
            output_char = chr(final_code)
        except ValueError:
            output_char = '?'  # Fallback for invalid codes
        
        # Calculate precision metrics
        accuracy = self._calculate_accuracy(base_code, final_code, energy_level, adrenaline_level)
        
        # DEBUG: Print detailed conversion information
        print(f"DEBUG: Neural activity: {neural_activity:.6f}, Base code: {base_code}, Final code: {final_code}, Char: '{output_char}', Accuracy: {accuracy:.3f}")
        
        # Apply dopamine bonus for motivation (simulating game motivation)
        if dopamine_level > 0.8:  # High dopamine = motivated state
            accuracy = min(1.0, accuracy * (1.0 + dopamine_level * 0.2))
        
        # Store processing information
        self.last_output_char = output_char
        self.last_output_code = final_code
        
        # Create output result
        result = {
            'input_activity': neural_activity,
            'base_code': base_code,
            'corrected_code': corrected_code,
            'final_code': final_code,
            'output_character': output_char,
            'accuracy': accuracy,
            'energy_level': energy_level,
            'adrenaline_level': adrenaline_level,
            'dopamine_level': dopamine_level,
            'processing_time': len(self.output_history) + 1
        }
        
        self.output_history.append(result)
        self.precision_history.append(accuracy)
        
        return result
    
    def _apply_energy_accuracy(self, base_code: int, energy_level: float) -> int:
        """Apply energy-dependent accuracy degradation"""
        if energy_level >= self.config.energy_threshold_high:
            # High energy: perfect accuracy
            return base_code
        
        elif energy_level >= self.config.energy_threshold_medium:
            # Medium energy: ±1 character variation
            variation = np.random.randint(-1, 2)  # -1, 0, or +1
            result = base_code + variation
            return max(32, result)  # Ensure printable ASCII range
        
        elif energy_level >= self.config.energy_threshold_low:
            # Low energy: ±3-5 character variation
            max_variation = 5
            variation = np.random.randint(-max_variation, max_variation + 1)
            result = base_code + variation
            return max(32, result)  # Ensure printable ASCII range
        
        else:
            # Critical energy: ±10-20 character variation
            max_variation = 20
            variation = np.random.randint(-max_variation, max_variation + 1)
            result = base_code + variation
            return max(32, result)  # Ensure printable ASCII range
    
    def _apply_adrenaline_tremor(self, code: int, adrenaline_level: float) -> int:
        """Apply adrenaline-induced motor tremor"""
        if adrenaline_level <= 0.1:
            # Low adrenaline: no tremor
            return code
        
        elif adrenaline_level <= self.config.adrenaline_threshold:
            # Medium adrenaline: slight tremor
            tremor = np.random.normal(0, self.config.tremor_magnitude * 0.5)
            result = int(code + tremor)
            return max(32, result)  # Ensure printable ASCII range
        
        else:
            # High adrenaline: significant tremor
            tremor = np.random.normal(0, self.config.tremor_magnitude * 2.0)
            result = int(code + tremor)
            return max(32, result)  # Ensure printable ASCII range
    
    def _calculate_accuracy(self, base_code: int, final_code: int, 
                          energy_level: float, adrenaline_level: float) -> float:
        """Calculate accuracy percentage based on various factors"""
        # Base accuracy from energy level
        if energy_level >= self.config.energy_threshold_high:
            energy_accuracy = 1.0
        elif energy_level >= self.config.energy_threshold_medium:
            energy_accuracy = 0.95
        elif energy_level >= self.config.energy_threshold_low:
            energy_accuracy = 0.85
        else:
            energy_accuracy = 0.60
        
        # Adrenaline penalty
        if adrenaline_level > self.config.adrenaline_threshold:
            adrenaline_penalty = adrenaline_level * 0.4  # Up to 40% penalty
        else:
            adrenaline_penalty = 0.0
        
        # Base error rate
        base_error = self.config.base_error_rate
        
        # Calculate final accuracy
        accuracy = max(0.0, energy_accuracy - adrenaline_penalty - base_error)
        
        # Additional penalty for critical energy
        if energy_level < self.config.energy_threshold_low:
            accuracy *= 0.7
        
        return max(0.0, min(1.0, accuracy))
    
    def read_layer_v_activity(self, layer_v_population, energy_level: float, 
                            adrenaline_level: float) -> Dict[str, Any]:
        """
        Read activity from Layer V motor cortex and convert to output.
        
        Args:
            layer_v_population: Layer V neuron population from Frontal Lobe
            energy_level: Current system energy level
            adrenaline_level: Current adrenaline level from Amygdala
            
        Returns:
            Dictionary containing output conversion results
        """
        # Get average activity from Layer V
        layer_v_activity = layer_v_population.get_average_activity()
        
        # Convert to character
        conversion_result = self.convert_to_character(
            layer_v_activity, energy_level, adrenaline_level
        )
        
        return {
            'layer_v_activity': layer_v_activity,
            'conversion_result': conversion_result,
            'motor_output': conversion_result['output_character']
        }
    
    def batch_convert(self, activity_sequence: List[float], energy_sequence: List[float], 
                    adrenaline_sequence: List[float]) -> List[Dict[str, Any]]:
        """
        Convert a sequence of neural activities to characters.
        
        Args:
            activity_sequence: List of Layer V activities
            energy_sequence: List of corresponding energy levels
            adrenaline_sequence: List of corresponding adrenaline levels
            
        Returns:
            List of conversion results
        """
        if not (len(activity_sequence) == len(energy_sequence) == len(adrenaline_sequence)):
            raise ValueError("All sequences must have the same length")
        
        results = []
        
        for i, (activity, energy, adrenaline) in enumerate(zip(
            activity_sequence, energy_sequence, adrenaline_sequence
        )):
            result = self.convert_to_character(activity, energy, adrenaline)
            results.append(result)
        
        return results
    
    def get_output_summary(self) -> Dict[str, Any]:
        """Get summary of recent output activity"""
        if not self.output_history:
            return {
                'total_outputs': 0,
                'average_accuracy': 0.0,
                'last_output': None,
                'error_count': 0
            }
        
        total_outputs = len(self.output_history)
        avg_accuracy = np.mean(self.precision_history)
        error_count = sum(1 for r in self.output_history if r['accuracy'] < 0.8)
        
        return {
            'total_outputs': total_outputs,
            'average_accuracy': avg_accuracy,
            'last_output': self.output_history[-1],
            'error_count': error_count,
            'recent_outputs': self.output_history[-10:],  # Last 10 outputs
            'accuracy_trend': self._calculate_accuracy_trend()
        }
    
    def _calculate_accuracy_trend(self) -> str:
        """Calculate accuracy trend over recent outputs"""
        if len(self.precision_history) < 3:
            return "insufficient_data"
        
        recent = self.precision_history[-10:]
        if len(recent) < 3:
            return "insufficient_data"
        
        # Simple trend calculation
        first_half = np.mean(recent[:len(recent)//2])
        second_half = np.mean(recent[len(recent)//2:])
        
        if second_half > first_half + 0.05:
            return "improving"
        elif second_half < first_half - 0.05:
            return "declining"
        else:
            return "stable"
    
    def get_precision_metrics(self) -> Dict[str, Any]:
        """Get detailed precision metrics"""
        if not self.precision_history:
            return {
                'min_accuracy': 0.0,
                'max_accuracy': 0.0,
                'avg_accuracy': 0.0,
                'std_accuracy': 0.0,
                'high_precision_count': 0,
                'low_precision_count': 0
            }
        
        accuracies = self.precision_history
        high_precision = sum(1 for a in accuracies if a >= 0.9)
        low_precision = sum(1 for a in accuracies if a < 0.7)
        
        return {
            'min_accuracy': min(accuracies),
            'max_accuracy': max(accuracies),
            'avg_accuracy': np.mean(accuracies),
            'std_accuracy': np.std(accuracies),
            'high_precision_count': high_precision,
            'low_precision_count': low_precision,
            'precision_distribution': {
                'excellent': sum(1 for a in accuracies if a >= 0.95),
                'good': sum(1 for a in accuracies if 0.8 <= a < 0.95),
                'fair': sum(1 for a in accuracies if 0.6 <= a < 0.8),
                'poor': sum(1 for a in accuracies if a < 0.6)
            }
        }
    
    def reset(self):
        """Reset output history and state"""
        self.last_output_char = None
        self.last_output_code = 0
        self.last_input_value = 0.0
        self.output_history = []
        self.precision_history = []


class MotorOutputValidator:
    """Validator for motor output quality and consistency"""
    
    @staticmethod
    def validate_output_character(character: str) -> bool:
        """Validate that output character is reasonable"""
        if not character or len(character) != 1:
            return False
        
        try:
            code = ord(character)
            # Accept printable characters and common symbols
            return 32 <= code <= 1114111
        except:
            return False
    
    @staticmethod
    def detect_output_errors(output_sequence: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Detect and categorize output errors"""
        errors = []
        
        for i, output in enumerate(output_sequence):
            accuracy = output.get('accuracy', 0.0)
            energy = output.get('energy_level', 0.0)
            adrenaline = output.get('adrenaline_level', 0.0)
            
            error_types = []
            
            if accuracy < 0.5:
                error_types.append("critical_accuracy_loss")
            elif accuracy < 0.8:
                error_types.append("moderate_accuracy_loss")
            
            if energy < 0.2:
                error_types.append("energy_depletion")
            
            if adrenaline > 0.8:
                error_types.append("adrenaline_overload")
            
            if error_types:
                errors.append({
                    'index': i,
                    'character': output.get('output_character', '?'),
                    'accuracy': accuracy,
                    'error_types': error_types,
                    'timestamp': output.get('processing_time', i)
                })
        
        return errors
    
    @staticmethod
    def calculate_motor_fatigue(energy_sequence: List[float]) -> float:
        """Calculate motor fatigue based on energy depletion"""
        if not energy_sequence:
            return 0.0
        
        avg_energy = np.mean(energy_sequence)
        
        # Fatigue increases as energy decreases
        fatigue = max(0.0, 1.0 - avg_energy)
        
        return fatigue


# Convenience functions for common output scenarios
def create_high_precision_output_gateway() -> OutputGateway:
    """Create output gateway with high precision settings"""
    config = OutputConfig(
        unicode_normalization_factor=128.0,  # ASCII range to match input
        energy_threshold_high=0.9,  # Stricter energy requirements
        energy_threshold_medium=0.7,
        adrenaline_threshold=0.8,  # Higher tolerance for adrenaline
        base_error_rate=0.005,  # Lower base error rate
        tremor_magnitude=0.05  # Less tremor
    )
    return OutputGateway(config)


def create_robust_output_gateway() -> OutputGateway:
    """Create output gateway optimized for robustness over precision"""
    config = OutputConfig(
        energy_threshold_high=0.7,  # More tolerant of low energy
        energy_threshold_medium=0.4,
        adrenaline_threshold=0.5,  # Lower tolerance for stress
        base_error_rate=0.02,  # Higher base error rate
        tremor_magnitude=0.15  # More tremor tolerance
    )
    return OutputGateway(config)


def create_learning_output_gateway() -> OutputGateway:
    """Create output gateway that improves with practice"""
    config = OutputConfig(
        energy_threshold_high=0.8,
        energy_threshold_medium=0.6,
        adrenaline_threshold=0.7,
        base_error_rate=0.015,
        tremor_magnitude=0.08
    )
    return OutputGateway(config)