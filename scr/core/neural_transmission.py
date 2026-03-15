#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NeuralTransmission class for aNA v5.0

This module defines the standardized data structure for neural communication
between brain regions, with dopamine-enhanced data transmission capabilities.
"""

import numpy as np
from dataclasses import dataclass
from typing import Dict, Any, Optional


@dataclass
class NeuralTransmission:
    """
    Standardized neural transmission data structure.
    
    This class provides a unified format for data transmission between brain regions,
    with dopamine-dependent quality enhancement.
    """
    signal_strength: float
    feature_details: Dict[str, Any]
    noise_level: float
    dopamine_modulation: float
    quality_level: str
    timestamp: float
    
    @classmethod
    def create_from_thalamus(cls, base_signal: float, dopamine_level: float, 
                           timestamp: float = None) -> 'NeuralTransmission':
        """
        Create a neural transmission from thalamic output with dopamine enhancement.
        
        Args:
            base_signal: Base signal strength from thalamus
            dopamine_level: Current dopamine level (0.0-1.0)
            timestamp: Optional timestamp
            
        Returns:
            Enhanced neural transmission
        """
        if timestamp is None:
            timestamp = np.random.random()  # Simulate timing
        
        # Determine quality level based on dopamine
        if dopamine_level >= 0.8:
            quality = "HIGH_DETAIL"
            feature_enhancement = 1.5
            noise_reduction = 0.3
        elif dopamine_level >= 0.5:
            quality = "ENHANCED"
            feature_enhancement = 1.2
            noise_reduction = 0.15
        else:
            quality = "STANDARD"
            feature_enhancement = 1.0
            noise_reduction = 0.0
        
        # Enhance signal based on dopamine
        enhanced_signal = base_signal * feature_enhancement
        
        # Reduce noise based on dopamine
        base_noise = 0.1
        noise_level = max(0.01, base_noise * (1.0 - noise_reduction))
        
        # Create feature details
        feature_details = {
            'spatial_resolution': feature_enhancement,
            'temporal_resolution': feature_enhancement,
            'feature_complexity': feature_enhancement,
            'signal_to_noise_ratio': 1.0 / noise_level,
            'dopamine_boost': dopamine_level
        }
        
        return cls(
            signal_strength=enhanced_signal,
            feature_details=feature_details,
            noise_level=noise_level,
            dopamine_modulation=dopamine_level,
            quality_level=quality,
            timestamp=timestamp
        )
    
    def get_processing_accuracy(self) -> float:
        """
        Get the expected processing accuracy based on transmission quality.
        
        Returns:
            Accuracy factor (0.0-1.0)
        """
        base_accuracy = 0.8
        
        if self.quality_level == "HIGH_DETAIL":
            accuracy_boost = 0.2
        elif self.quality_level == "ENHANCED":
            accuracy_boost = 0.1
        else:
            accuracy_boost = 0.0
        
        # Additional boost from dopamine modulation
        dopamine_boost = self.dopamine_modulation * 0.1
        
        return min(1.0, base_accuracy + accuracy_boost + dopamine_boost)
    
    def get_feature_extraction_quality(self) -> float:
        """
        Get the quality of feature extraction possible with this transmission.
        
        Returns:
            Feature extraction quality factor (1.0-2.0)
        """
        return self.feature_details.get('spatial_resolution', 1.0)
    
    def apply_noise(self) -> float:
        """
        Apply noise to the signal strength.
        
        Returns:
            Noisy signal strength
        """
        noise = np.random.normal(0, self.noise_level)
        return self.signal_strength + noise
    
    def get_signal_strength(self) -> float:
        """Get the signal strength of this transmission"""
        return self.signal_strength
    
    def get_neuromodulators(self) -> Dict[str, float]:
        """Get neuromodulator information from this transmission"""
        return {
            'dopamine': self.dopamine_modulation,
            'acetylcholine': 0.0,  # Default values for other modulators
            'norepinephrine': 0.0,
            'serotonin': 0.0,
            'nitric_oxide': 0.0
        }
    
    def get_quality_description(self) -> str:
        """Get human-readable quality description"""
        descriptions = {
            "STANDARD": "Standard transmission quality",
            "ENHANCED": "Enhanced transmission with improved features",
            "HIGH_DETAIL": "High-detail transmission with maximum fidelity"
        }
        return descriptions.get(self.quality_level, "Unknown quality")


class TransmissionBridge:
    """
    Bridge for standardized data transmission between brain regions.
    
    This class handles the conversion between different data formats
    and ensures dopamine-enhanced transmission quality.
    """
    
    @staticmethod
    def thalamus_to_occipital(thalamic_output: float, 
                            neuromodulators: Dict[str, float]) -> NeuralTransmission:
        """
        Convert thalamic output to occipital input with dopamine enhancement.
        
        Args:
            thalamic_output: Raw output from thalamic nucleus
            neuromodulators: Current neuromodulator levels
            
        Returns:
            Enhanced neural transmission for occipital processing
        """
        dopamine_level = neuromodulators.get('dopamine', 0.0)
        
        return NeuralTransmission.create_from_thalamus(
            base_signal=thalamic_output,
            dopamine_level=dopamine_level
        )
    
    @staticmethod
    def occipital_to_frontal(occipital_output: Dict[str, Any],
                           neuromodulators: Dict[str, float]) -> NeuralTransmission:
        """
        Convert occipital output to frontal input with attention modulation.
        
        Args:
            occipital_output: Output from occipital processing
            neuromodulators: Current neuromodulator levels
            
        Returns:
            Enhanced neural transmission for frontal processing
        """
        dopamine_level = neuromodulators.get('dopamine', 0.0)
        
        # Extract signal strength from occipital output
        signal_strength = occipital_output.get('output_activity', 0.0)
        
        return NeuralTransmission.create_from_thalamus(
            base_signal=signal_strength,
            dopamine_level=dopamine_level
        )
    
    @staticmethod
    def frontal_to_output(frontal_output: float,
                         neuromodulators: Dict[str, float]) -> NeuralTransmission:
        """
        Convert frontal output to motor output with motivation enhancement.
        
        Args:
            frontal_output: Output from frontal lobe
            neuromodulators: Current neuromodulator levels
            
        Returns:
            Enhanced neural transmission for motor output
        """
        dopamine_level = neuromodulators.get('dopamine', 0.0)
        
        return NeuralTransmission.create_from_thalamus(
            base_signal=frontal_output,
            dopamine_level=dopamine_level
        )


# Convenience functions for common transmission scenarios
def create_sensory_transmission(signal: float, dopamine: float) -> NeuralTransmission:
    """Create a sensory transmission with dopamine enhancement"""
    return NeuralTransmission.create_from_thalamus(signal, dopamine)


def create_motor_transmission(signal: float, dopamine: float) -> NeuralTransmission:
    """Create a motor transmission with motivation enhancement"""
    return NeuralTransmission.create_from_thalamus(signal, dopamine)


def get_dopamine_quality_factor(dopamine_level: float) -> float:
    """Get quality enhancement factor based on dopamine level"""
    if dopamine_level >= 0.8:
        return 1.5  # High detail
    elif dopamine_level >= 0.5:
        return 1.2  # Enhanced
    else:
        return 1.0  # Standard