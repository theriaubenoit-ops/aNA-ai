#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Input Gateway for aNA v4.0

This module handles sensory input processing by converting Unicode characters
to normalized decimal values and injecting them into the LGN (Lateral Geniculate Nucleus)
of the Thalamus for visual processing.

Key features:
- Unicode character to decimal conversion
- Normalization to 0.0-1.0 range
- Direct injection into LGN for retinotopic mapping
- Error handling for invalid inputs
- Integration with existing Thalamus structure
"""

import numpy as np
from typing import Union, Optional, Dict, Any
from dataclasses import dataclass


@dataclass
class InputConfig:
    """Configuration for input processing"""
    unicode_normalization_factor: float = 1_000_000.0  # Normalize by full Unicode range
    lgn_injection_strength: float = 1.0  # Multiplier for LGN injection
    spatial_spread: float = 2.0  # Spatial spread in LGN mapping
    noise_level: float = 0.01  # Add noise for biological realism


class InputGateway:
    """
    Gateway for converting sensory input (Unicode characters) to neural signals.
    
    This class bridges symbolic processing with neural dynamics by:
    1. Converting characters to Unicode code points
    2. Normalizing to appropriate neural activation ranges
    3. Injecting signals into the LGN for visual processing
    4. Providing feedback on input processing status
    """
    
    def __init__(self, config: Optional[InputConfig] = None):
        """
        Initialize the input gateway.
        
        Args:
            config: Input processing configuration
        """
        self.config = config or InputConfig()
        self.last_input_char = None
        self.last_input_code = 0
        self.last_normalized_value = 0.0
        self.processing_history = []
    
    def process_character(self, character: str) -> Dict[str, Any]:
        """
        Process a single character and convert to neural input.
        
        Args:
            character: Input character (should be single character)
            
        Returns:
            Dictionary containing processing results
        """
        if not character or len(character) != 1:
            raise ValueError("Input must be a single character")
        
        # Get Unicode code point
        try:
            unicode_code = ord(character)
        except TypeError:
            raise ValueError(f"Cannot convert '{character}' to Unicode code point")
        
        # Normalize to 0.0-1.0 range
        normalized_value = unicode_code / self.config.unicode_normalization_factor
        
        # Add biological noise
        noise = np.random.normal(0, self.config.noise_level)
        noisy_value = max(0.0, min(1.0, normalized_value + noise))
        
        # Store processing information
        self.last_input_char = character
        self.last_input_code = unicode_code
        self.last_normalized_value = noisy_value
        
        # Create processing result
        result = {
            'input_character': character,
            'unicode_code': unicode_code,
            'normalized_value': normalized_value,
            'noisy_value': noisy_value,
            'injection_strength': noisy_value * self.config.lgn_injection_strength,
            'processing_time': len(self.processing_history) + 1
        }
        
        self.processing_history.append(result)
        
        return result
    
    def inject_into_lgn(self, lgn_nucleus, character: str, neuromodulators: Dict[str, float]):
        """
        Inject processed character input into LGN for visual processing.
        
        Args:
            lgn_nucleus: LGN nucleus from Thalamus to inject into
            character: Input character to process
            neuromodulators: Current neuromodulator levels
        """
        # Process the character
        processing_result = self.process_character(character)
        
        # Get injection parameters
        injection_strength = processing_result['injection_strength']
        
        # Apply neuromodulatory effects
        modulated_strength = self._apply_neuromodulatory_effects(injection_strength, neuromodulators)
        
        # Inject into LGN - use process_input instead of receive_sensory_input
        lgn_nucleus.process_input(modulated_strength, neuromodulators)
        
        return {
            'character': character,
            'injection_strength': injection_strength,
            'modulated_strength': modulated_strength,
            'lgn_response': lgn_nucleus.get_activity()
        }
    
    def _apply_neuromodulatory_effects(self, base_strength: float, neuromodulators: Dict[str, float]) -> float:
        """Apply neuromodulator effects to input strength"""
        # Acetylcholine enhances sensory processing
        ach_effect = 1.0 + (neuromodulators.get('acetylcholine', 0.0) * 0.5)
        
        # Norepinephrine increases alertness and signal clarity
        norepinephrine_effect = 1.0 + (neuromodulators.get('norepinephrine', 0.0) * 0.3)
        
        # Dopamine can enhance or suppress based on level
        dopamine_level = neuromodulators.get('dopamine', 0.0)
        dopamine_effect = 1.0 + (dopamine_level * 0.2) if dopamine_level < 0.5 else 1.0 - (dopamine_level * 0.1)
        
        # Serotonin stabilizes input processing
        serotonin_effect = 1.0 - (neuromodulators.get('serotonin', 0.0) * 0.1)
        
        # NO gas can enhance local processing
        no_effect = 1.0 + (neuromodulators.get('no_gas', 0.0) * 0.1)
        
        total_modulation = (ach_effect * norepinephrine_effect * dopamine_effect * 
                          serotonin_effect * no_effect)
        
        return base_strength * total_modulation
    
    def batch_process(self, text: str, lgn_nucleus, neuromodulators: Dict[str, float]) -> list:
        """
        Process a sequence of characters.
        
        Args:
            text: String to process character by character
            lgn_nucleus: LGN nucleus for injection
            neuromodulators: Current neuromodulator levels
            
        Returns:
            List of processing results for each character
        """
        results = []
        
        for char in text:
            if char.isspace():
                # Skip whitespace but maintain timing
                continue
            
            try:
                result = self.inject_into_lgn(lgn_nucleus, char, neuromodulators)
                results.append(result)
            except Exception as e:
                # Log error but continue processing
                results.append({
                    'character': char,
                    'error': str(e),
                    'injection_strength': 0.0,
                    'modulated_strength': 0.0
                })
        
        return results
    
    def get_processing_summary(self) -> Dict[str, Any]:
        """Get summary of recent processing activity"""
        if not self.processing_history:
            return {
                'total_characters': 0,
                'average_strength': 0.0,
                'last_input': None
            }
        
        total_chars = len(self.processing_history)
        avg_strength = np.mean([r['injection_strength'] for r in self.processing_history])
        
        return {
            'total_characters': total_chars,
            'average_strength': avg_strength,
            'last_input': self.processing_history[-1] if self.processing_history else None,
            'recent_history': self.processing_history[-10:]  # Last 10 inputs
        }
    
    def reset(self):
        """Reset processing history and state"""
        self.last_input_char = None
        self.last_input_code = 0
        self.last_normalized_value = 0.0
        self.processing_history = []


class SensoryInputValidator:
    """Validator for sensory input quality and range"""
    
    @staticmethod
    def validate_character_range(character: str) -> bool:
        """Validate that character is within reasonable Unicode range"""
        if not character or len(character) != 1:
            return False
        
        try:
            code = ord(character)
            # Accept printable ASCII and common Unicode characters
            return 32 <= code <= 1114111  # Full Unicode range
        except:
            return False
    
    @staticmethod
    def get_character_category(character: str) -> str:
        """Categorize character type for processing"""
        if not character or len(character) != 1:
            return "invalid"
        
        code = ord(character)
        
        if 32 <= code <= 126:  # ASCII printable
            if character.isalpha():
                return "letter"
            elif character.isdigit():
                return "digit"
            else:
                return "symbol"
        elif 128 <= code <= 255:  # Extended ASCII
            return "extended"
        elif code > 255:  # Unicode
            return "unicode"
        else:
            return "control"
    
    @staticmethod
    def calculate_processing_complexity(character: str) -> float:
        """Calculate relative complexity of character processing"""
        category = SensoryInputValidator.get_character_category(character)
        
        complexity_map = {
            'letter': 1.0,
            'digit': 0.8,
            'symbol': 1.2,
            'extended': 1.5,
            'unicode': 2.0,
            'invalid': 0.0
        }
        
        return complexity_map.get(category, 0.0)


# Convenience functions for common input scenarios
def create_ascii_input_gateway() -> InputGateway:
    """Create input gateway optimized for ASCII characters"""
    config = InputConfig(
        unicode_normalization_factor=128.0,  # ASCII range
        lgn_injection_strength=2.0,  # Stronger for ASCII
        noise_level=0.005  # Less noise for clean input
    )
    return InputGateway(config)


def create_unicode_input_gateway() -> InputGateway:
    """Create input gateway for full Unicode range"""
    config = InputConfig(
        unicode_normalization_factor=1_000_000.0,  # Full Unicode
        lgn_injection_strength=1.0,
        noise_level=0.01
    )
    return InputGateway(config)


def create_high_precision_gateway() -> InputGateway:
    """Create high-precision input gateway with minimal noise"""
    config = InputConfig(
        unicode_normalization_factor=1_000_000.0,
        lgn_injection_strength=1.5,
        noise_level=0.001,  # Very low noise
        spatial_spread=1.0  # Tighter spatial mapping
    )
    return InputGateway(config)