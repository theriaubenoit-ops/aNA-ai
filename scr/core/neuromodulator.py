#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Neuromodulator Matrix - The Chemical Layer of aNA v4

This module implements the neuromodulator system with 5 key chemicals:
- NO (Nitric Oxide): Volumetric retrograde signaling for local cluster strengthening
- Acetylcholine (ACh): Sensory sensitivity and focus modulation
- Dopamine (DA): Reward, plasticity, and learning signal
- Serotonin (5-HT): Homeostatic balance and epilepsy prevention
- Norepinephrine (Adrenaline): Hyper-alertness and flashbulb memory

Architecture, concept and supervision: Benoit Theriault
Collaboration, research and code: Gemini
"""

import numpy as np
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
import math


class NeuromodulatorType(Enum):
    """Types of neuromodulators in the system"""
    NO = "no_gas"              # Nitric Oxide
    ACH = "acetylcholine"      # Acetylcholine  
    DA = "dopamine"           # Dopamine
    SEROTONIN = "serotonin"   # Serotonin (5-HT)
    NE = "norepinephrine"     # Norepinephrine (Adrenaline)


@dataclass
class NeuromodulatorConfig:
    """Configuration parameters for neuromodulator behavior"""
    # General properties
    diffusion_rate: float = 0.1
    decay_rate: float = 0.05
    baseline_level: float = 0.1
    
    # NO-specific properties
    no_diffusion_radius: float = 100.0
    no_retrograde_strength: float = 0.5
    
    # ACh-specific properties
    ach_sensory_gain: float = 0.3
    ach_attention_threshold: float = 0.2
    
    # Dopamine-specific properties
    da_plasticity_multiplier: float = 2.0
    da_reward_threshold: float = 0.3
    
    # Serotonin-specific properties
    serotonin_stabilization_strength: float = 0.2
    epilepsy_prevention_threshold: float = 0.8
    
    # Norepinephrine-specific properties
    ne_alertness_multiplier: float = 0.4
    ne_flashbulb_threshold: float = 0.6
    ne_concentration_factor: float = 0.3


class Neuromodulator:
    """
    A single neuromodulator with spatial diffusion and temporal dynamics.
    
    Each neuromodulator has:
    - Concentration levels that change over time
    - Spatial diffusion patterns
    - Specific effects on neuronal activity
    - Source and sink mechanisms
    """
    
    def __init__(self, modulator_type: NeuromodulatorType, config: NeuromodulatorConfig):
        """
        Initialize a neuromodulator.
        
        Args:
            modulator_type: Type of neuromodulator
            config: Configuration parameters
        """
        self.type = modulator_type
        self.config = config
        
        # State variables
        self.concentration = self.config.baseline_level
        self.spatial_concentration = {}  # {position_tuple: concentration}
        self.sources = []  # List of active sources
        self.sinks = []    # List of active sinks
        
        # Temporal dynamics
        self.last_update_time = 0
        self.accumulated_release = 0.0
    
    def add_source(self, position: np.ndarray, strength: float, duration: int = -1):
        """
        Add a source of neuromodulator release.
        
        Args:
            position: 3D position of the source
            strength: Release strength
            duration: Duration in time steps (-1 for continuous)
        """
        source = {
            'position': tuple(position),
            'strength': strength,
            'duration': duration,
            'remaining_duration': duration,
            'active': True
        }
        self.sources.append(source)
    
    def add_sink(self, position: np.ndarray, absorption_rate: float):
        """
        Add a sink that absorbs neuromodulator.
        
        Args:
            position: 3D position of the sink
            absorption_rate: Rate of absorption
        """
        sink = {
            'position': tuple(position),
            'absorption_rate': absorption_rate
        }
        self.sinks.append(sink)
    
    def release(self, amount: float):
        """Release a specific amount of neuromodulator"""
        self.accumulated_release += amount
    
    def update(self, time_step: int, neuron_positions: Optional[np.ndarray] = None):
        """
        Update neuromodulator concentration and spatial distribution.
        
        Args:
            time_step: Current simulation time step
            neuron_positions: Positions of neurons for spatial calculations
        """
        # Update temporal dynamics
        self._update_temporal_dynamics(time_step)
        
        # Update spatial distribution if positions are provided
        if neuron_positions is not None:
            self._update_spatial_distribution(neuron_positions)
    
    def _update_temporal_dynamics(self, time_step: int):
        """Update concentration over time"""
        # Apply decay
        self.concentration *= (1.0 - self.config.decay_rate)
        
        # Add accumulated release
        self.concentration += self.accumulated_release
        self.accumulated_release = 0.0
        
        # Clamp concentration
        self.concentration = max(0.0, min(1.0, self.concentration))
        
        # Update sources
        for source in self.sources[:]:  # Copy list to allow modification
            if source['active']:
                if source['remaining_duration'] > 0:
                    source['remaining_duration'] -= 1
                    if source['remaining_duration'] <= 0:
                        source['active'] = False
        
        # Remove inactive sources
        self.sources = [s for s in self.sources if s['active']]
    
    def _update_spatial_distribution(self, neuron_positions: np.ndarray):
        """Update spatial concentration distribution"""
        # Clear previous spatial concentrations
        self.spatial_concentration = {}
        
        # Calculate spatial effects from sources
        for source in self.sources:
            source_pos = np.array(source['position'])
            source_strength = source['strength']
            
            # Calculate distances to all neurons
            distances = np.linalg.norm(neuron_positions - source_pos, axis=1)
            
            # Apply diffusion model
            if self.type == NeuromodulatorType.NO:
                # NO has volumetric diffusion
                radius = self.config.no_diffusion_radius
                effect = self._calculate_no_diffusion(distances, radius, source_strength)
            else:
                # Other neuromodulators have gradient diffusion
                effect = self._calculate_gradient_diffusion(distances, source_strength)
            
            # Update spatial concentrations
            for i, pos in enumerate(neuron_positions):
                pos_key = tuple(pos)
                if pos_key not in self.spatial_concentration:
                    self.spatial_concentration[pos_key] = 0.0
                self.spatial_concentration[pos_key] += effect[i]
        
        # Apply sink effects
        for sink in self.sinks:
            sink_pos = np.array(sink['position'])
            absorption_rate = sink['absorption_rate']
            
            distances = np.linalg.norm(neuron_positions - sink_pos, axis=1)
            
            # Calculate absorption effect
            absorption_effect = np.exp(-distances / 50.0) * absorption_rate
            
            for i, pos in enumerate(neuron_positions):
                pos_key = tuple(pos)
                if pos_key in self.spatial_concentration:
                    self.spatial_concentration[pos_key] *= (1.0 - absorption_effect[i])
    
    def _calculate_no_diffusion(self, distances: np.ndarray, radius: float, strength: float) -> np.ndarray:
        """Calculate NO volumetric diffusion"""
        # NO diffuses in a spherical volume
        in_radius = distances <= radius
        effect = np.zeros_like(distances, dtype=float)
        
        # Strong effect within radius, exponential decay outside
        effect[in_radius] = strength * (1.0 - distances[in_radius] / radius)
        effect[~in_radius] = strength * np.exp(-(distances[~in_radius] - radius) / 20.0)
        
        return effect
    
    def _calculate_gradient_diffusion(self, distances: np.ndarray, strength: float) -> np.ndarray:
        """Calculate gradient-based diffusion for other neuromodulators"""
        # Exponential decay with distance
        return strength * np.exp(-distances / 30.0)
    
    def get_concentration_at(self, position: np.ndarray) -> float:
        """Get concentration at a specific position"""
        pos_key = tuple(position)
        return self.spatial_concentration.get(pos_key, self.concentration)
    
    def get_global_concentration(self) -> float:
        """Get average global concentration"""
        return self.concentration
    
    def get_effects(self) -> Dict[str, float]:
        """Get the effects of this neuromodulator on neuronal activity"""
        base_effect = self.concentration
        
        effects = {}
        
        if self.type == NeuromodulatorType.NO:
            effects = {
                'synaptic_strengthening': base_effect * self.config.no_retrograde_strength,
                'local_clustering': base_effect * 0.5,
                'blood_flow': base_effect * 0.3
            }
        
        elif self.type == NeuromodulatorType.ACH:
            effects = {
                'sensory_sensitivity': base_effect * self.config.ach_sensory_gain,
                'attention_focus': base_effect * 0.4,
                'learning_readiness': base_effect * 0.3
            }
        
        elif self.type == NeuromodulatorType.DA:
            effects = {
                'plasticity_multiplier': 1.0 + (base_effect * self.config.da_plasticity_multiplier),
                'reward_signal': base_effect * 0.6,
                'motivation': base_effect * 0.4
            }
        
        elif self.type == NeuromodulatorType.SEROTONIN:
            effects = {
                'stabilization': base_effect * self.config.serotonin_stabilization_strength,
                'epilepsy_prevention': base_effect * self.config.epilepsy_prevention_threshold,
                'mood_regulation': base_effect * 0.3
            }
        
        elif self.type == NeuromodulatorType.NE:
            effects = {
                'alertness': base_effect * self.config.ne_alertness_multiplier,
                'concentration': base_effect * self.config.ne_concentration_factor,
                'flashbulb_memory': base_effect * self.config.ne_flashbulb_threshold,
                'stress_response': base_effect * 0.5
            }
        
        return effects


class NeuromodulatorMatrix:
    """
    The complete neuromodulator system managing all 5 chemicals.
    
    This class:
    - Manages the 5 neuromodulators as a matrix
    - Handles their interactions and cross-effects
    - Provides unified interface for neuronal integration
    - Implements feedback loops and homeostatic regulation
    """
    
    def __init__(self, config: Optional[NeuromodulatorConfig] = None):
        """
        Initialize the neuromodulator matrix.
        
        Args:
            config: Configuration for all neuromodulators
        """
        self.config = config or NeuromodulatorConfig()
        
        # Initialize all neuromodulators
        self.modulators = {
            NeuromodulatorType.NO: Neuromodulator(NeuromodulatorType.NO, self.config),
            NeuromodulatorType.ACH: Neuromodulator(NeuromodulatorType.ACH, self.config),
            NeuromodulatorType.DA: Neuromodulator(NeuromodulatorType.DA, self.config),
            NeuromodulatorType.SEROTONIN: Neuromodulator(NeuromodulatorType.SEROTONIN, self.config),
            NeuromodulatorType.NE: Neuromodulator(NeuromodulatorType.NE, self.config)
        }
        
        # System state
        self.time_step = 0
        self.neuron_positions = None
        
        # Feedback regulation
        self.homeostatic_regulation = True
        self.cross_modulation = True
    
    def set_neuron_positions(self, positions: np.ndarray):
        """Set the positions of all neurons for spatial calculations"""
        self.neuron_positions = positions
    
    def update(self, time_step: int):
        """Update all neuromodulators"""
        self.time_step = time_step
        
        for modulator in self.modulators.values():
            modulator.update(time_step, self.neuron_positions)
        
        # Apply cross-modulation effects
        if self.cross_modulation:
            self._apply_cross_modulation()
        
        # Apply homeostatic regulation
        if self.homeostatic_regulation:
            self._apply_homeostatic_regulation()
    
    def _apply_cross_modulation(self):
        """Apply cross-effects between different neuromodulators"""
        # Get current concentrations
        concentrations = {t: m.get_global_concentration() for t, m in self.modulators.items()}
        
        # Dopamine enhances NO effects
        da_level = concentrations[NeuromodulatorType.DA]
        self.modulators[NeuromodulatorType.NO].config.no_retrograde_strength = 0.5 + (da_level * 0.3)
        
        # Serotonin modulates ACh effects
        serotonin_level = concentrations[NeuromodulatorType.SEROTONIN]
        self.modulators[NeuromodulatorType.ACH].config.ach_sensory_gain = 0.3 + (serotonin_level * 0.2)
        
        # Norepinephrine enhances DA effects during stress
        ne_level = concentrations[NeuromodulatorType.NE]
        if ne_level > 0.5:  # High stress
            self.modulators[NeuromodulatorType.DA].config.da_plasticity_multiplier = 2.5
        else:
            self.modulators[NeuromodulatorType.DA].config.da_plasticity_multiplier = 2.0
        
        # ACh and NE have competitive effects on attention
        ach_level = concentrations[NeuromodulatorType.ACH]
        if ach_level > 0.3 and ne_level > 0.3:
            # High levels of both reduce overall effectiveness
            self.modulators[NeuromodulatorType.ACH].config.ach_sensory_gain *= 0.8
            self.modulators[NeuromodulatorType.NE].config.ne_alertness_multiplier *= 0.8
    
    def _apply_homeostatic_regulation(self):
        """Apply homeostatic regulation to prevent runaway excitation"""
        # Get average activity levels
        avg_concentrations = np.mean([m.get_global_concentration() for m in self.modulators.values()])
        
        # If overall activity is too high, increase serotonin
        if avg_concentrations > 0.7:
            self.modulators[NeuromodulatorType.SEROTONIN].release(0.1)
        
        # If overall activity is too low, increase ACh and NE
        elif avg_concentrations < 0.2:
            self.modulators[NeuromodulatorType.ACH].release(0.05)
            self.modulators[NeuromodulatorType.NE].release(0.05)
    
    def release_modulator(self, modulator_type: NeuromodulatorType, amount: float, position: Optional[np.ndarray] = None):
        """Release a specific neuromodulator"""
        if position is not None:
            self.modulators[modulator_type].add_source(position, amount)
        else:
            self.modulators[modulator_type].release(amount)
    
    def get_modulator_effects(self, position: Optional[np.ndarray] = None) -> Dict[str, float]:
        """
        Get the combined effects of all neuromodulators at a position.
        
        Args:
            position: Optional 3D position for spatial effects
            
        Returns:
            Dictionary of combined neuromodulator effects
        """
        combined_effects = {
            'synaptic_strengthening': 0.0,
            'sensory_sensitivity': 0.0,
            'plasticity_multiplier': 1.0,
            'stabilization': 0.0,
            'alertness': 0.0,
            'concentration': 0.0,
            'flashbulb_memory': 0.0,
            'learning_readiness': 0.0,
            'stress_response': 0.0
        }
        
        for modulator in self.modulators.values():
            if position is not None:
                # Get spatial effects
                local_concentration = modulator.get_concentration_at(position)
                effects = modulator.get_effects()
                
                # Scale effects by local concentration
                for key, value in effects.items():
                    if key in combined_effects:
                        if 'multiplier' in key:
                            combined_effects[key] *= value
                        else:
                            combined_effects[key] += value * local_concentration
            else:
                # Get global effects
                effects = modulator.get_effects()
                for key, value in effects.items():
                    if key in combined_effects:
                        if 'multiplier' in key:
                            combined_effects[key] *= value
                        else:
                            combined_effects[key] += value
        
        return combined_effects
    
    def get_state(self) -> Dict[str, Any]:
        """Get current state of all neuromodulators"""
        state = {}
        for mod_type, modulator in self.modulators.items():
            state[mod_type.value] = {
                'concentration': modulator.get_global_concentration(),
                'num_sources': len(modulator.sources),
                'num_sinks': len(modulator.sinks),
                'effects': modulator.get_effects()
            }
        return state
    
    def trigger_reward_response(self, position: Optional[np.ndarray] = None, intensity: float = 1.0):
        """Trigger a reward response with dopamine release"""
        da_amount = 0.3 * intensity
        if position is not None:
            # Localized reward
            self.release_modulator(NeuromodulatorType.DA, da_amount, position)
            # Also release NO for local strengthening
            self.release_modulator(NeuromodulatorType.NO, 0.2 * intensity, position)
        else:
            # Global reward
            self.release_modulator(NeuromodulatorType.DA, da_amount)
    
    def trigger_stress_response(self, position: Optional[np.ndarray] = None, intensity: float = 1.0):
        """Trigger a stress response with norepinephrine release"""
        ne_amount = 0.4 * intensity
        if position is not None:
            self.release_modulator(NeuromodulatorType.NE, ne_amount, position)
        else:
            self.release_modulator(NeuromodulatorType.NE, ne_amount)
    
    def trigger_focus_response(self, position: Optional[np.ndarray] = None, intensity: float = 1.0):
        """Trigger a focus response with acetylcholine release"""
        ach_amount = 0.2 * intensity
        if position is not None:
            self.release_modulator(NeuromodulatorType.ACH, ach_amount, position)
        else:
            self.release_modulator(NeuromodulatorType.ACH, ach_amount)
    
    def trigger_memory_consolidation(self, position: Optional[np.ndarray] = None, intensity: float = 1.0):
        """Trigger memory consolidation with coordinated neuromodulator release"""
        # Release NO for local strengthening
        self.release_modulator(NeuromodulatorType.NO, 0.3 * intensity, position)
        
        # Release dopamine for plasticity
        self.release_modulator(NeuromodulatorType.DA, 0.2 * intensity, position)
        
        # Release norepinephrine for alertness
        self.release_modulator(NeuromodulatorType.NE, 0.1 * intensity, position)
    
    def reset(self):
        """Reset all neuromodulators to baseline"""
        for modulator in self.modulators.values():
            modulator.concentration = self.config.baseline_level
            modulator.sources = []
            modulator.sinks = []
            modulator.accumulated_release = 0.0
            modulator.spatial_concentration = {}
    
    def get_current_levels(self) -> Dict[str, float]:
        """Get current neuromodulator levels (alias for get_neuromodulator_levels)"""
        return {
            'dopamine': self.modulators[NeuromodulatorType.DA].get_global_concentration(),
            'serotonin': self.modulators[NeuromodulatorType.SEROTONIN].get_global_concentration(),
            'norepinephrine': self.modulators[NeuromodulatorType.NE].get_global_concentration(),
            'acetylcholine': self.modulators[NeuromodulatorType.ACH].get_global_concentration(),
            'nitric_oxide': self.modulators[NeuromodulatorType.NO].get_global_concentration()
        }
