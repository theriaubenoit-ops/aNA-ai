#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Enhanced Thalamus implementation for aNA v4

This module implements the Thalamus with all major sensory nuclei and the 
Reticular Thalamic Nucleus (RTN) for sensory processing and gating.
"""

import numpy as np
import asyncio
import time
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

from .neuron import Neuron, NeuronConfig, NeuronPopulation
from core.neural_transmission import NeuralTransmission, TransmissionBridge


class ThalamicNucleusType(Enum):
    """Types of thalamic nuclei"""
    VPM = "VPM"  # Ventral Posteromedial - taste, facial sensation
    VPL = "VPL"  # Ventral Posterolateral - body sensation
    LGN = "LGN"  # Lateral Geniculate Nucleus - vision
    MGN = "MGN"  # Medial Geniculate Nucleus - hearing
    PULVINAR = "PULVINAR"  # Visual attention and integration
    MD = "MD"    # Mediodorsal - prefrontal connections
    RTN = "RTN"  # Reticular Thalamic Nucleus - inhibitory gating


@dataclass
class ThalamicNucleusConfig:
    """Configuration for a thalamic nucleus"""
    nucleus_type: ThalamicNucleusType
    position: np.ndarray
    size: int
    connectivity_radius: float = 50.0
    firing_threshold: float = -55.0
    baseline_activity: float = 0.1
    sensory_modality: str = "multimodal"


class ThalamicNucleus:
    """A thalamic nucleus containing a population of neurons"""
    
    def __init__(self, config: ThalamicNucleusConfig):
        self.config = config
        self.neurons = []
        self.active_neurons = 0
        self.total_activity = 0.0
        
        # Initialize neurons in a spherical cluster
        self._initialize_neurons()
    
    def _initialize_neurons(self):
        """Initialize neurons in a spherical cluster"""
        center = self.config.position
        radius = (self.config.size * 3 / (4 * np.pi)) ** (1/3)
        
        for i in range(self.config.size):
            # Generate random position within sphere
            r = radius * (i / self.config.size) ** (1/3)
            theta = np.random.uniform(0, 2 * np.pi)
            phi = np.random.uniform(0, np.pi)
            
            x = center[0] + r * np.sin(phi) * np.cos(theta)
            y = center[1] + r * np.sin(phi) * np.sin(theta)
            z = center[2] + r * np.cos(phi)
            
            position = np.array([x, y, z])
            neuron_config = NeuronConfig(
                layer_id=0,  # Thalamic neurons
                threshold_potential=self.config.firing_threshold
            )
            neuron = Neuron(position, neuron_config)
            self.neurons.append(neuron)
    
    def process_input(self, input_signal: float, neuromodulators: Dict[str, float]):
        """Process sensory input through the nucleus"""
        # BASELINE RHYTHM: Thalamus is always active (gateway to consciousness)
        # Minimum baseline activity is 0.15, even without sensory input
        baseline_activity = 0.15
        
        # Calculate thalamic output with baseline
        # Formula: (Input + Baseline) × 0.95, clamped to biological limits
        raw_output = (input_signal + baseline_activity) * 0.95
        
        # MANAGE SATURATION: If result exceeds 1.0, clamp to 1.0
        # This maintains biological realism while preventing overflow
        thalamic_output = min(raw_output, 1.0)
        
        # Apply neuromodulatory effects
        modulated_output = thalamic_output
        
        # Acetylcholine increases sensitivity
        if 'acetylcholine' in neuromodulators:
            modulated_output *= (1.0 + neuromodulators['acetylcholine'] * 0.2)  # Reduced modulation
        
        # Serotonin modulates activity
        if 'serotonin' in neuromodulators:
            modulated_output *= (1.0 - neuromodulators['serotonin'] * 0.1)  # Reduced modulation
        
        # Ensure output never goes below baseline
        modulated_output = max(modulated_output, baseline_activity)
        
        # Apply to all neurons
        for neuron in self.neurons:
            # Convert to membrane potential input
            membrane_input = modulated_output * 50.0  # Scale to appropriate range
            
            neuron.receive_input(membrane_input, neuromodulators)
            neuron.update(0, neuromodulators)
        
        # Calculate activity metrics - use the processed output directly
        self.active_neurons = sum(1 for n in self.neurons if n.is_firing)
        # CRITICAL: Use the thalamic output as total activity, not neuron membrane potentials
        self.total_activity = modulated_output
    
    def get_output(self) -> float:
        """Get the output signal from this nucleus"""
        if len(self.neurons) == 0:
            return 0.0
        
        # Output is proportional to number of firing neurons
        firing_ratio = self.active_neurons / len(self.neurons)
        return firing_ratio * 100.0  # Scale to meaningful output range
    
    def get_position(self) -> np.ndarray:
        """Get the center position of this nucleus"""
        return self.config.position
    
    def get_size(self) -> int:
        """Get the number of neurons in this nucleus"""
        return len(self.neurons)
    
    def receive_sensory_input(self, input_strength: float):
        """Receive sensory input (used by InputGateway)"""
        # This method is called by InputGateway to inject sensory input
        # The actual processing happens in process_input method
        pass
    
    def get_activity(self) -> float:
        """Get current activity level of this nucleus"""
        return self.total_activity


class ReticularThalamicNucleus:
    """Reticular Thalamic Nucleus for inhibitory gating"""
    
    def __init__(self, position: np.ndarray, size: int = 200):
        self.position = position
        self.size = size
        self.neurons = []
        self.gating_strength = 0.5  # Default gating (inhibition)
        
        self._initialize_neurons()
    
    def _initialize_neurons(self):
        """Initialize GABAergic inhibitory neurons"""
        center = self.position
        radius = (self.size * 3 / (4 * np.pi)) ** (1/3)
        
        for i in range(self.size):
            # Generate random position within shell
            r = radius * (0.5 + 0.5 * (i / self.size))  # Shell structure
            theta = np.random.uniform(0, 2 * np.pi)
            phi = np.random.uniform(0, np.pi)
            
            x = center[0] + r * np.sin(phi) * np.cos(theta)
            y = center[1] + r * np.sin(phi) * np.sin(theta)
            z = center[2] + r * np.cos(phi)
            
            position = np.array([x, y, z])
            # RTN neurons have different properties
            config = NeuronConfig(
                layer_id=0,
                threshold_potential=-50.0,  # Lower threshold for inhibitory neurons
                base_energy_consumption=0.008,  # Lower energy consumption
                firing_energy_cost=0.08
            )
            neuron = Neuron(position, config)
            self.neurons.append(neuron)
    
    def process_input(self, cortical_feedback: float, neuromodulators: Dict[str, float]):
        """Process cortical feedback and modulate gating"""
        # Cortical feedback excites RTN (disinhibition)
        for neuron in self.neurons:
            input_signal = cortical_feedback
            
            # Norepinephrine increases RTN activity (more inhibition)
            if 'norepinephrine' in neuromodulators:
                input_signal *= (1.0 + neuromodulators['norepinephrine'] * 0.3)
            
            # Acetylcholine decreases RTN activity (less inhibition)
            if 'acetylcholine' in neuromodulators:
                input_signal *= (1.0 - neuromodulators['acetylcholine'] * 0.2)
            
            neuron.receive_input(input_signal, neuromodulators)
            neuron.update(0, neuromodulators)
        
        # Calculate gating strength based on RTN activity
        active_ratio = sum(1 for n in self.neurons if n.is_firing) / len(self.neurons)
        
        # RTN activity increases inhibition (gating)
        self.gating_strength = 0.1 + active_ratio * 0.9
    
    def apply_gating(self, signal: float) -> float:
        """Apply inhibitory gating to a signal"""
        # Gating reduces signal transmission
        return signal * (1.0 - self.gating_strength)
    
    def get_gating_state(self) -> float:
        """Get current gating state (0.0 = no gating, 1.0 = complete gating)"""
        return self.gating_strength


class Thalamus:
    """Enhanced Thalamus with all sensory nuclei and RTN"""
    
    def __init__(self, position: np.ndarray = np.array([0.0, -20.0, 0.0])):
        self.position = position
        self.nuclei: Dict[ThalamicNucleusType, ThalamicNucleus] = {}
        self.rtn = None
        self.sensory_inputs: Dict[str, float] = {}
        
        # Alpha Oscillator properties
        self.alpha_oscillator_active = False
        self.alpha_start_time = 0.0
        self.alpha_frequency = 10.0  # Hz (Alpha rhythm: 8-12 Hz)
        self.alpha_amplitude = 0.4   # Oscillation amplitude
        self.alpha_baseline = 0.15   # Biological baseline
        self.alpha_current_phase = 0.0
        
        self._initialize_nuclei()
    
    def _initialize_nuclei(self):
        """Initialize all thalamic nuclei"""
        # Base position for thalamus
        base_pos = self.position
        
        # VPM (Ventral Posteromedial) - taste, facial sensation
        vpm_config = ThalamicNucleusConfig(
            nucleus_type=ThalamicNucleusType.VPM,
            position=base_pos + np.array([-5.0, 0.0, 5.0]),
            size=500,
            sensory_modality="gustatory"
        )
        self.nuclei[ThalamicNucleusType.VPM] = ThalamicNucleus(vpm_config)
        
        # VPL (Ventral Posterolateral) - body sensation
        vpl_config = ThalamicNucleusConfig(
            nucleus_type=ThalamicNucleusType.VPL,
            position=base_pos + np.array([5.0, 0.0, 5.0]),
            size=800,
            sensory_modality="somatosensory"
        )
        self.nuclei[ThalamicNucleusType.VPL] = ThalamicNucleus(vpl_config)
        
        # LGN (Lateral Geniculate Nucleus) - vision
        lgn_config = ThalamicNucleusConfig(
            nucleus_type=ThalamicNucleusType.LGN,
            position=base_pos + np.array([0.0, 10.0, 0.0]),
            size=600,
            sensory_modality="visual"
        )
        self.nuclei[ThalamicNucleusType.LGN] = ThalamicNucleus(lgn_config)
        
        # MGN (Medial Geniculate Nucleus) - hearing
        mgn_config = ThalamicNucleusConfig(
            nucleus_type=ThalamicNucleusType.MGN,
            position=base_pos + np.array([0.0, -10.0, 0.0]),
            size=400,
            sensory_modality="auditory"
        )
        self.nuclei[ThalamicNucleusType.MGN] = ThalamicNucleus(mgn_config)
        
        # Pulvinar - visual attention and integration
        pulvinar_config = ThalamicNucleusConfig(
            nucleus_type=ThalamicNucleusType.PULVINAR,
            position=base_pos + np.array([0.0, 0.0, 10.0]),
            size=300,
            sensory_modality="multimodal"
        )
        self.nuclei[ThalamicNucleusType.PULVINAR] = ThalamicNucleus(pulvinar_config)
        
        # MD (Mediodorsal) - prefrontal connections
        md_config = ThalamicNucleusConfig(
            nucleus_type=ThalamicNucleusType.MD,
            position=base_pos + np.array([0.0, 0.0, -10.0]),
            size=200,
            sensory_modality="cognitive"
        )
        self.nuclei[ThalamicNucleusType.MD] = ThalamicNucleus(md_config)
        
        # RTN (Reticular Thalamic Nucleus) - inhibitory shell
        rtn_position = base_pos + np.array([0.0, 0.0, 0.0])
        self.rtn = ReticularThalamicNucleus(rtn_position, size=200)
    
    def process_sensory_input(self, modality: str, signal: float):
        """Process sensory input of a specific modality"""
        self.sensory_inputs[modality] = signal
    
    def update(self, neuromodulators: Dict[str, float], cortical_feedback: float = 0.0):
        """Update thalamic processing with unified sensory-autonomous integration"""
        # 1. Update RTN (priority for gating control)
        self.rtn.process_input(cortical_feedback, neuromodulators)
        
        # 2. Calculate autonomy weight based on sensory load
        # When sensory input is high, autonomous activity is reduced
        sensory_load = sum(self.sensory_inputs.values())
        autonomy_weight = max(0.0, 1.0 - (sensory_load * 2.0))  # Sensory dominance factor
        alpha_activity = self.get_alpha_rhythm_activity()
        
        # 3. Unified processing for all nuclei
        for nucleus_type, nucleus in self.nuclei.items():
            # A. Raw sensory input for this modality
            sensory_signal = self.sensory_inputs.get(nucleus.config.sensory_modality, 0.0)
            
            # B. Dynamic mixing: Alpha activity is reduced when sensory signal is strong
            # This creates a push-pull mechanism between external input and internal rhythm
            input_signal = sensory_signal + (alpha_activity * autonomy_weight)
            
            # C. Add baseline and ensure minimum threshold
            input_signal += nucleus.config.baseline_activity
            input_signal = max(input_signal, 0.1)  # Minimum activity threshold
            
            # D. Process through nucleus and apply RTN gating
            nucleus.process_input(input_signal, neuromodulators)
            gated_output = self.rtn.apply_gating(nucleus.get_output())
            nucleus.total_activity = gated_output
    
    def get_outputs(self) -> Dict[ThalamicNucleusType, float]:
        """Get outputs from all nuclei"""
        outputs = {}
        for nucleus_type, nucleus in self.nuclei.items():
            outputs[nucleus_type] = nucleus.get_output()
        return outputs
    
    def get_rtn_state(self) -> float:
        """Get RTN gating state"""
        return self.rtn.get_gating_state()
    
    def get_total_activity(self) -> float:
        """Get total thalamic activity"""
        return sum(nucleus.total_activity for nucleus in self.nuclei.values())
    
    def get_activity(self) -> float:
        """Get current thalamic activity level (alias for get_total_activity)"""
        # CRITICAL FIX: Ensure thalamic baseline is always maintained
        # The floor is now sacred: minimum 0.15 (biological baseline)
        actual_activity = self.get_total_activity()
        return max(actual_activity, 0.15)
    
    def get_nucleus(self, nucleus_type: ThalamicNucleusType):
        """Get a specific thalamic nucleus"""
        return self.nuclei.get(nucleus_type, None)
    
    def get_visual_transmission(self, neuromodulators: Dict[str, float]) -> NeuralTransmission:
        """Get dopamine-enhanced visual transmission for occipital lobe"""
        lgn_nucleus = self.nuclei.get(ThalamicNucleusType.LGN)
        if lgn_nucleus is None:
            return NeuralTransmission.create_from_thalamus(0.0, 0.0)
        
        # Get the processed output from LGN
        lgn_output = lgn_nucleus.get_output()
        
        # Normalize LGN output from 0-100 range to 0-1 range for transmission
        normalized_output = lgn_output / 100.0
        
        # Ensure minimum output for processing
        normalized_output = max(normalized_output, 0.1)  # Minimum activity level
        
        # Create dopamine-enhanced transmission
        return TransmissionBridge.thalamus_to_occipital(normalized_output, neuromodulators)
    
    def reset(self):
        """Reset all nuclei and RTN"""
        for nucleus in self.nuclei.values():
            for neuron in nucleus.neurons:
                neuron.reset()
        
        if self.rtn:
            for neuron in self.rtn.neurons:
                neuron.reset()
            self.rtn.gating_strength = 0.5
    
    # Alpha Oscillator Methods
    async def start_alpha_oscillator(self):
        """Start the intrinsic alpha rhythm oscillator"""
        if self.alpha_oscillator_active:
            return
        
        self.alpha_oscillator_active = True
        self.alpha_start_time = time.time()
        self.alpha_current_phase = 0.0
        
        print("🧠 Alpha Oscillator: Starting intrinsic thalamic rhythm...")
        
        try:
            while self.alpha_oscillator_active:
                # Calculate alpha oscillation
                current_time = time.time()
                elapsed = current_time - self.alpha_start_time
                
                # Alpha rhythm: 8-12 Hz, we use 10 Hz as target
                # Formula: baseline + amplitude * sin(2π * frequency * time)
                oscillation = self.alpha_baseline + self.alpha_amplitude * np.sin(2 * np.pi * self.alpha_frequency * elapsed)
                
                # Ensure biological bounds (0.1 to 0.9)
                oscillation = max(0.1, min(0.9, oscillation))
                
                # Update thalamic activity with alpha rhythm
                self.alpha_current_phase = elapsed
                
                # Small delay for 10Hz oscillation (100ms)
                await asyncio.sleep(0.1)
                
        except asyncio.CancelledError:
            print("🧠 Alpha Oscillator: Stopping gracefully...")
            self.alpha_oscillator_active = False
            raise
    
    def stop_alpha_oscillator(self):
        """Stop the alpha oscillator"""
        self.alpha_oscillator_active = False
        print("🧠 Alpha Oscillator: Stopped")
    
    def get_alpha_rhythm_activity(self) -> float:
        """Get current alpha rhythm activity level"""
        if not self.alpha_oscillator_active:
            return self.alpha_baseline
        
        # Calculate current alpha activity
        current_time = time.time()
        elapsed = current_time - self.alpha_start_time
        oscillation = self.alpha_baseline + self.alpha_amplitude * np.sin(2 * np.pi * self.alpha_frequency * elapsed)
        
        # Ensure biological bounds
        return max(0.1, min(0.9, oscillation))
    
    def get_alpha_rhythm_state(self) -> Dict[str, float]:
        """Get detailed alpha rhythm state for dashboard"""
        return {
            'active': self.alpha_oscillator_active,
            'frequency_hz': self.alpha_frequency,
            'amplitude': self.alpha_amplitude,
            'baseline': self.alpha_baseline,
            'current_activity': self.get_alpha_rhythm_activity(),
            'phase_seconds': self.alpha_current_phase,
            'total_activity': self.get_activity()
        }


# Convenience functions for common thalamic operations
def create_sensory_thalamus(position: np.ndarray = None) -> Thalamus:
    """Create a thalamus optimized for sensory processing"""
    if position is None:
        position = np.array([0.0, -20.0, 0.0])
    
    thalamus = Thalamus(position)
    
    # Enhance sensory nuclei
    thalamus.nuclei[ThalamicNucleusType.VPL].config.size = 1000  # Enhanced body sensation
    thalamus.nuclei[ThalamicNucleusType.LGN].config.size = 800   # Enhanced vision
    thalamus.nuclei[ThalamicNucleusType.MGN].config.size = 600   # Enhanced hearing
    
    return thalamus


def create_cognitive_thalamus(position: np.ndarray = None) -> Thalamus:
    """Create a thalamus optimized for cognitive processing"""
    if position is None:
        position = np.array([0.0, -20.0, 0.0])
    
    thalamus = Thalamus(position)
    
    # Enhance cognitive nuclei
    thalamus.nuclei[ThalamicNucleusType.MD].config.size = 500    # Enhanced prefrontal connections
    thalamus.nuclei[ThalamicNucleusType.PULVINAR].config.size = 600  # Enhanced attention
    
    return thalamus