#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Parietal Lobe Module for aNA v4.0

This module implements the parietal lobe functionality for spatial processing,
sensory integration, and attention coordination. The parietal lobe acts as
the spatial coordinator between visual input and higher cognitive functions.

Key Features:
- Spatial coordinate processing and integration
- Attention focus coordination with thalamus
- Sensory integration from occipital lobe
- Column-aligned monitoring output

Architecture, concept and supervision: Benoit Theriault
Collaboration, research and code: Gemini, Cline and GPT
"""

import numpy as np
from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class ParietalConfig:
    """Configuration for parietal lobe parameters"""
    spatial_integration_factor: float = 0.85
    attention_modulation_factor: float = 0.9
    baseline_activity: float = 0.1
    max_activity: float = 1.0


class ParietalLobe:
    """
    Parietal Lobe implementation for spatial processing and attention coordination.
    
    The parietal lobe integrates spatial information from the occipital lobe
    and coordinates attention focus with the thalamus. It acts as a spatial
    coordinator that processes coordinate data and attention requests.
    """
    
    def __init__(self, config: Optional[ParietalConfig] = None):
        """Initialize the parietal lobe with configuration"""
        self.config = config or ParietalConfig()
        self.spatial_activity = self.config.baseline_activity
        self.attention_focus = 0.0
        self.integrated_coordinates = np.array([0.0, 0.0, 0.0])
        
        print("🧠 Parietal Lobe Initialized - Spatial Processing Active")
    
    def process_spatial_input(self, occipital_outputs: Dict[str, Any], 
                             neuromodulators: Dict[str, float]) -> Dict[str, Any]:
        """
        Process spatial information from occipital lobe outputs.
        
        Args:
            occipital_outputs: Output from occipital lobe processing
            neuromodulators: Current neuromodulator levels
            
        Returns:
            Dictionary containing spatial processing results
        """
        # Extract visual features from occipital outputs
        v1_features = occipital_outputs.get('v1_features', {})
        v1_activity = v1_features.get('output_activity', 0.0)
        
        # Spatial integration calculation
        # Integrate visual activity with spatial processing
        spatial_integration = (
            v1_activity * self.config.spatial_integration_factor
        )
        
        # Apply neuromodulator effects
        dopamine_level = neuromodulators.get('dopamine', 0.1)
        acetylcholine_level = neuromodulators.get('acetylcholine', 0.1)
        
        # Dopamine enhances spatial processing accuracy
        dopamine_modulation = 1.0 + (dopamine_level * 0.2)
        
        # Acetylcholine enhances attention focus
        attention_modulation = 1.0 + (acetylcholine_level * 0.3)
        
        # Calculate final spatial activity
        self.spatial_activity = min(
            self.config.max_activity,
            spatial_integration * dopamine_modulation
        )
        
        # Calculate attention focus
        self.attention_focus = min(
            1.0,
            self.spatial_activity * attention_modulation * self.config.attention_modulation_factor
        )
        
        # Generate spatial coordinates (simplified 3D coordinate system)
        # Based on visual activity and attention focus
        coordinate_base = self.spatial_activity * 10.0  # Scale up for coordinate system
        self.integrated_coordinates = np.array([
            coordinate_base * 0.5,  # X coordinate
            coordinate_base * 0.3,  # Y coordinate  
            coordinate_base * 0.2   # Z coordinate (depth)
        ])
        
        # Return spatial processing results
        return {
            'spatial_activity': self.spatial_activity,
            'attention_focus': self.attention_focus,
            'coordinates': self.integrated_coordinates,
            'integration_factor': self.config.spatial_integration_factor,
            'processing_accuracy': self.spatial_activity
        }
    
    def request_attention_focus(self, thalamus: Any, 
                               target_coordinates: Optional[np.ndarray] = None) -> Dict[str, Any]:
        """
        Request attention focus adjustment from thalamus.
        
        This is the key feedback mechanism where parietal lobe communicates
        with thalamus to adjust attention focus based on spatial processing needs.
        
        Args:
            thalamus: Thalamus object to request attention from
            target_coordinates: Optional target coordinates for attention focus
            
        Returns:
            Dictionary containing attention request results
        """
        # Determine attention request strength based on current processing needs
        attention_request_strength = self.attention_focus * 0.8
        
        # If specific coordinates provided, enhance request
        if target_coordinates is not None:
            coordinate_strength = np.linalg.norm(target_coordinates) * 0.1
            attention_request_strength = min(1.0, attention_request_strength + coordinate_strength)
        
        # Request attention focus from thalamus
        # This simulates the biological reality where parietal cortex
        # modulates thalamic attention gates
        attention_result = {
            'request_strength': attention_request_strength,
            'target_coordinates': target_coordinates,
            'current_focus': self.attention_focus,
            'thalamus_response': 'attention_modulated'  # Simulated response
        }
        
        # Print column-aligned monitoring
        print(f"Parietal Spatial: {self.spatial_activity:.6f}")
        
        return attention_result
    
    def get_spatial_outputs(self) -> Dict[str, Any]:
        """Get current spatial processing outputs"""
        return {
            'spatial_activity': self.spatial_activity,
            'attention_focus': self.attention_focus,
            'coordinates': self.integrated_coordinates,
            'processing_status': 'active'
        }
    
    def reset(self):
        """Reset parietal lobe to initial state"""
        self.spatial_activity = self.config.baseline_activity
        self.attention_focus = 0.0
        self.integrated_coordinates = np.array([0.0, 0.0, 0.0])
        print("🔄 Parietal Lobe Reset Complete")


def create_spatial_focused_parietal() -> ParietalLobe:
    """
    Create a parietal lobe configured for spatial processing and attention coordination.
    
    Returns:
        Configured ParietalLobe instance
    """
    config = ParietalConfig(
        spatial_integration_factor=0.85,  # High integration for spatial processing
        attention_modulation_factor=0.9,   # Strong attention modulation
        baseline_activity=0.1,             # Standard baseline
        max_activity=1.0                   # Standard maximum
    )
    
    return ParietalLobe(config)