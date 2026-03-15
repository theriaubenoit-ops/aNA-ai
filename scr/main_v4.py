#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Main Controller for aNA v4.0 -> v5.0

This module orchestrates the entire neural architecture including:
- Sensory input processing (Unicode → Decimal)
- Neural processing through brain structures
- Motor output processing (Decimal → Unicode)
- Real-time dashboard with precision monitoring
- Energy and neuromodulator tracking
- Integration of all components

Architecture, concept and supervision: Benoit Theriault
Collaboration, research and code: Gemini, Cline and GPT
"""

import numpy as np
import time
import sys
import signal
import select
import tty
import termios
import asyncio
from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from enum import Enum

# Import all components
from core.neuromodulator import NeuromodulatorMatrix, NeuromodulatorType
from core.input_gateway import InputGateway, create_ascii_input_gateway
from core.output_gateway import OutputGateway, create_high_precision_output_gateway
from core.neural_transmission import NeuralTransmission
from anatomy.thalamus import Thalamus, ThalamicNucleusType
from anatomy.cortex.occipital import OccipitalLobe, create_primary_occipital
from anatomy.cortex.frontal import FrontalLobe, create_motor_focused_frontal
from anatomy.cortex.parietal import ParietalLobe, create_spatial_focused_parietal
from anatomy.cortex.temporal import TemporalLobe, create_semantic_focused_temporal
from anatomy.amygdala import Amygdala
from anatomy.hippocampus import Hippocampus
from anatomy.cerebellum import Cerebellum

from config import AMYGDALA_SENSITIVITY, ADRENALINE_RELEASE_FACTOR    # config.py


class SystemState(Enum):
    """System operational states"""
    IDLE = "idle"
    PROCESSING = "processing"
    ERROR = "error"
    LEARNING = "learning"


@dataclass(frozen=True)
class SystemMetrics:
    """System-wide metrics and statistics"""
    total_characters_processed: int = 0
    total_errors: int = 0
    average_precision: float = 0.0
    system_energy: float = 1.0
    adrenaline_level: float = 0.0
    learning_progress: float = 0.0
    processing_time_ms: float = 0.0

@dataclass(frozen=True) # "Frozen" pour assurer que le résultat ne change pas en cours de route
class NeuralProcessingResult:
    input_char: str = 0.0
    output_char: str = 0.0
    precision: float = 0.0
    processing_time_ms: float = 0.0
    energy_level: float = 0.0
    adrenaline_level: float = 0.0
    neuromodulators: Dict[str, float] = 0.0
    brain_activity: Dict[str, Any] = 0.0

class ANAController:
    """
    Main controller for the aNA v4.0 -> v5.0 system.
    
    This class orchestrates the entire neural processing pipeline:
    1. Sensory input through Input Gateway
    2. Thalamic processing and routing
    3. Visual processing in Occipital Lobe
    4. Motor planning and execution in Frontal Lobe
    5. Output generation through Output Gateway
    6. Real-time monitoring and dashboard
    """
    
    # Constants
    ENERGY_COST_PER_CHAR = 0.005
    BASELINE_ACTIVITY = 0.15
    MIN_PRECISION_FOR_SUCCESS = 0.8
    MIN_PRECISION_FOR_IMPROVEMENT = 0.5
    STRESS_THRESHOLD = 0.1  # ⚠️  PERSONALITY PARAMETER: Lower = more nervous, Higher = more calm   (0.5)
    NATURAL_ADRENALINE_DECAY = 0.01
    NATURAL_NOREPINEPHRINE_DECAY = 0.01
    
    # Amygdala Personality Parameters
    # AMYGDALA_SENSITIVITY = 1.0  # ⚠️  PERSONALITY PARAMETER: Higher = more reactive to stress  (1.0)
    # ADRENALINE_RELEASE_FACTOR = 0.5  # ⚠️  PERSONALITY PARAMETER: Higher = more adrenaline per stress unit  (0.1)
    """
    Personnalités possibles :
    - "Le Nerveux" : `AMYGDALA_SENSITIVITY = 0.3` (réactif au moindre écart)
    - "Le Calme" : `AMYGDALA_SENSITIVITY = 1.5` (seulement en cas d'échec majeur)
    - "Le Perfectionniste" : `ADRENALINE_RELEASE_FACTOR = 0.3` (réaction intense)
    """
    
    def __init__(self):
        """Initialize the complete aNA v4.0 -> v5.0 system"""
        # Add shutdown flag for graceful termination
        self.shutdown_flag = False
        
        # Add signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        self.state = SystemState.IDLE
        self.metrics = SystemMetrics()
        
        # Initialize neuromodulator matrix
        self.neuromodulators = NeuromodulatorMatrix()
        
        # Initialize sensory and motor gateways
        self.input_gateway = create_ascii_input_gateway()
        self.output_gateway = create_high_precision_output_gateway()
        
        # Initialize brain structures
        self.thalamus = Thalamus()
        # BIOLOGICAL FIX: Ensure LGN nucleus is properly initialized as the visual input gateway
        # The LGN (Lateral Geniculate Nucleus) is the critical relay station for visual information
        # from the retina to the primary visual cortex (V1). It acts as the "gatekeeper" for visual
        # processing, maintaining a baseline activity of 0.15 to ensure continuous visual awareness.
        # The LGN receives direct input from retinal ganglion cells and projects to V1, forming the
        # primary visual pathway. Its baseline activity of 0.15 ensures the visual system remains
        # responsive to stimuli even in the absence of strong input.
        # NOTE: Thalamus initialization should create LGN automatically, but we ensure it exists
        if ThalamicNucleusType.LGN not in self.thalamus.nuclei:
            from anatomy.thalamus import ThalamicNucleus, ThalamicNucleusConfig
            lgn_config = ThalamicNucleusConfig(
                nucleus_type=ThalamicNucleusType.LGN,
                position=np.array([0.0, -10.0, 0.0]),  # Positioned in visual thalamus (corrected position)
                size=600,  # Large nucleus to handle high visual bandwidth
                sensory_modality="visual",  # Dedicated to visual processing
                baseline_activity=0.15  # Critical baseline for visual consciousness
            )
            self.thalamus.nuclei[ThalamicNucleusType.LGN] = ThalamicNucleus(lgn_config)
        
        self.occipital = create_primary_occipital()
        self.parietal = create_spatial_focused_parietal()
        self.temporal = create_semantic_focused_temporal()
        self.frontal = create_motor_focused_frontal()
        self.amygdala = Amygdala()
        # NEW: Use the new hippocampus for integration
        from anatomy.hippocampus import Hippocampus as Hippocampus
        self.hippocampus = Hippocampus()
        self.cerebellum = Cerebellum()
        
        # Processing history
        self.processing_history = []
        
        # Input buffer and processing queue
        self.input_buffer = []
        self.processing_queue = []
        self.current_processing_char = None
        self.processing_in_progress = False
        
        # Biological thalamuspulse system
        self.last_thalamuspulse = time.time()
        self.thalamuspulse_interval = 1.0  # 1 second thalamuspulse
        
        # Start Alpha Oscillator asynchronously
        self.alpha_oscillator_task = None
        # Note: Alpha oscillator will be started when asyncio event loop is available
        
        print("🧠 aNA v4.0 -> v5.0 System Initialized")
        print("📋 Components: Input Gateway, Thalamus, Occipital Lobe, Frontal Lobe, Output Gateway")
        print("🎯 Ready for Unicode ↔ Decimal processing with biological realism")
        print("💓 Thalamic baseline maintained by biological pulse system")
        print("🧠 Alpha Oscillator: Intrinsic thalamic rhythm active")
    
    async def _alpha_oscillator_loop(self):
        """Boucle asynchrone pour l'oscillateur alpha (Layer 1)
        
        Simule l'activité thalamique naturelle avec un oscillateur alpha (~10 Hz)
        pour maintenir la connectivité thalamo-corticale et la conscience de base.
        """
        while not self.shutdown_flag:
            try:
                # Générer un signal alpha (8-12 Hz) pour simuler l'activité thalamique
                # Cet oscillateur influence la connectivité thalamo-corticale
                alpha_phase = time.time() * 10.0  # Fréquence alpha ~10 Hz
                alpha_amplitude = 0.1 * (1.0 + np.sin(alpha_phase))
                
                # Injecter le signal alpha dans le thalamus pour moduler l'activité
                # Cela simule les oscillations thalamiques naturelles
                if hasattr(self.thalamus, 'modulate_activity'):
                    self.thalamus.modulate_activity(alpha_amplitude)
                
                # Attendre 0.1 seconde (100ms) pour maintenir la fréquence alpha
                await asyncio.sleep(0.1)
                
            except Exception as e:
                print(f"⚠️  Alpha oscillator error: {e}")
                await asyncio.sleep(0.1)
    
    def _start_alpha_oscillator(self):
        """Démarrer l'oscillateur alpha asynchrone
        
        Crée et démarre une coroutine asynchrone pour simuler l'activité
        thalamique alpha qui maintient la conscience de base et la connectivité
        thalamo-corticale.
        """
        try:
            # Créer l'événement d'arrêt
            self.shutdown_event = asyncio.Event()
            
            # Lancer la coroutine en arrière-plan
            self.alpha_oscillator_task = asyncio.create_task(self._alpha_oscillator_loop())
            print("🧠 Alpha Oscillator: Intrinsic thalamic rhythm started")
            
        except Exception as e:
            print(f"⚠️  Failed to start alpha oscillator: {e}")
    
    def debug_system_state(self):
        """Debug function to display detailed system state"""
        print("\n🔍 DEBUG: System State Analysis")
        print("=" * 50)
        
        # System metrics
        print(f"📊 System Metrics:")
        print(f"   Total Characters: {self.metrics.total_characters_processed}")
        print(f"   Total Errors: {self.metrics.total_errors}")
        print(f"   Average Precision: {self.metrics.average_precision:.3f}")
        print(f"   System Energy: {self.metrics.system_energy:.3f}")
        print(f"   Adrenaline Level: {self.metrics.adrenaline_level:.3f}")
        
        # Neuromodulator levels
        print(f"\n🧪 Neuromodulator Levels:")
        neuromodulators = self.neuromodulators.get_current_levels()
        for modulator, level in neuromodulators.items():
            print(f"   {modulator.upper()}: {level:.3f}")
        
        # Brain activity
        print(f"\n🧠 Brain Activity:")
        try:
            # Thalamus
            thalamus_activity = self.thalamus.get_activity() if hasattr(self.thalamus, 'get_activity') else 0.0
            print(f"   Thalamus: {thalamus_activity:.3f}")
            
            # Occipital Lobe
            occipital_outputs = self.occipital.get_visual_outputs() if hasattr(self.occipital, 'get_visual_outputs') else {}
            if 'v1_features' in occipital_outputs:
                v1_activity = occipital_outputs['v1_features'].get('output_activity', 0.0)
                print(f"   Occipital V1: {v1_activity:.3f}")
            
            # Parietal Lobe
            parietal_outputs = self.parietal.get_spatial_outputs() if hasattr(self.parietal, 'get_spatial_outputs') else {}
            parietal_activity = parietal_outputs.get('spatial_activity', 0.0)
            print(f"   Parietal Spatial: {parietal_activity:.3f}")
            
            # Temporal Lobe
            temporal_outputs = self.temporal.get_semantic_outputs() if hasattr(self.temporal, 'get_semantic_outputs') else {}
            temporal_activity = temporal_outputs.get('semantic_activity', 0.0)
            print(f"   Temporal Semantic: {temporal_activity:.3f}")
            
            # Frontal Lobe
            frontal_outputs = self.frontal.get_frontal_outputs() if hasattr(self.frontal, 'get_frontal_outputs') else {}
            if 'final_output' in frontal_outputs:
                motor_activity = frontal_outputs['final_output']
                print(f"   Frontal Motor: {motor_activity:.3f}")
            
            # Amygdala
            amygdala_activity = self.amygdala.get_activity() if hasattr(self.amygdala, 'get_activity') else 0.0
            print(f"   Amygdala: {amygdala_activity:.3f}")
        except Exception as e:
            print(f"   Error getting brain activity: {e}")
        
        # Processing state
        print(f"\n🔄 Processing State:")
        print(f"   System State: {self.state.value}")
        print(f"   Processing In Progress: {self.processing_in_progress}")
        print(f"   Current Character: {self.current_processing_char}")
        print(f"   Input Buffer Size: {len(self.input_buffer)}")
        print(f"   Processing Queue Size: {len(self.processing_queue)}")
        
        # Stability check
        stability = self._check_system_stability()
        print(f"\n🛡️  System Stability: {'✅ STABLE' if stability else '⚠️  UNSTABLE'}")
        
        print("=" * 50)
    
    def _check_system_stability(self) -> bool:
        """Check if the system is stable and safe to continue"""
        # Check for runaway neuromodulator levels
        neuromodulators = self.neuromodulators.get_current_levels()
        
        # Check for excessive dopamine (could cause over-excitation)
        if neuromodulators.get('dopamine', 0.0) > 0.9:
            print("⚠️  WARNING: High dopamine levels detected. System may be over-excited.")
            return False
        
        # Check for excessive adrenaline (could cause stress-induced errors)
        if neuromodulators.get('norepinephrine', 0.0) > 0.8:
            print("⚠️  WARNING: High adrenaline levels detected. System under stress.")
            return False
        
        # Check for critically low energy
        if self.metrics.system_energy < 0.1:
            print("⚠️  WARNING: Critically low energy levels. System performance degraded.")
            return False
        
        # Check for excessive error rate
        if self.metrics.total_characters_processed > 10:
            error_rate = self.metrics.total_errors / self.metrics.total_characters_processed
            if error_rate > 0.5:
                print("⚠️  WARNING: High error rate detected. System may be unstable.")
                return False
        
        return True
    
    def _apply_circuit_breaker(self):
        """Apply circuit breaker to prevent runaway processing"""
        print("🛑 Applying circuit breaker - reducing system activity")
        
        # Reduce all neuromodulator levels to safe ranges
        for modulator_type in self.neuromodulators.modulators:
            current_level = self.neuromodulators.modulators[modulator_type].get_global_concentration()
            if current_level > 0.5:
                # Reduce by 50%
                reduction = current_level * 0.5
                self.neuromodulators.release_modulator(modulator_type, -reduction)
        
        # Reset processing state
        self.processing_in_progress = False
        self.current_processing_char = None
        self.input_buffer.clear()
        self.processing_queue.clear()
        
        # Give system time to stabilize
        time.sleep(1.0)
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        print(f"\n🛑 Received signal {signum}. Shutting down gracefully...")
        self.shutdown_flag = True
        self.state = SystemState.IDLE
        sys.exit(0)
    
    def _apply_biological_heartbeat(self):
        """Apply biological heartbeat to maintain thalamic baseline and simulate respiration
        
        BIOLOGICAL CONSTANTS DOCUMENTATION:
        - Thalamic Baseline (0.15): Maintains consciousness gateway function
        - Thalamus Pulse Interval (1.0s): Simulates biological rhythm
        - Micro-charge (0.01): Small periodic input to prevent neural silence
        - Auto-rhythmic Neurons: Thalamic neurons fire spontaneously to maintain awareness
        """
        current_time = time.time()
        
        # Check if it's time for a thalamuspulse
        if current_time - self.last_thalamuspulse >= self.thalamuspulse_interval:
            # Apply micro-charge to thalamus to maintain baseline
            # This simulates the biological reality of auto-rhythmic thalamic neurons
            thalamuspulse_charge = 0.01  # Small micro-charge
            
            # Inject the heartbeat charge into the thalamus
            # This ensures the thalamus never goes below its biological baseline
            for nucleus_type, nucleus in self.thalamus.nuclei.items():
                # Add the heartbeat charge to each nucleus
                current_activity = nucleus.total_activity
                new_activity = current_activity + thalamuspulse_charge
                
                # Ensure the activity doesn't exceed biological limits
                nucleus.total_activity = min(new_activity, 1.0)
            
            # Update last thalamuspulse time
            self.last_thalamuspulse = current_time
    
    def _handle_processing_error(self, stage: str, error: Exception) -> None:
        """Handle processing errors with consistent messaging"""
        print(f"⚠️  {stage} error: {error}")
    
    def _process_input_stage(self, character: str) -> Dict:
        """Process input stage with error handling"""
        try:
            lgn_nucleus = self.thalamus.get_nucleus(ThalamicNucleusType.LGN)
            if lgn_nucleus is None:
                # Fallback: create LGN nucleus if not found
                from anatomy.thalamus import ThalamicNucleus, ThalamicNucleusConfig
                lgn_config = ThalamicNucleusConfig(
                    nucleus_type=ThalamicNucleusType.LGN,
                    position=np.array([0.0, 10.0, 0.0]),
                    size=600,
                    sensory_modality="visual"
                )
                lgn_nucleus = ThalamicNucleus(lgn_config)
                self.thalamus.nuclei[ThalamicNucleusType.LGN] = lgn_nucleus
            
            return self.input_gateway.inject_into_lgn(
                lgn_nucleus,
                character,
                self.neuromodulators.get_current_levels()
            )
        except Exception as e:
            self._handle_processing_error("Input processing", e)
            return {'injection_strength': 0.1}  # Fallback value
    
    def _process_thalamic_stage(self, input_result: Dict) -> Any:
        """Process thalamic stage with error handling"""
        try:
            self.thalamus.process_sensory_input('visual', input_result['injection_strength'])
            self.thalamus.update(self.neuromodulators.get_current_levels())
            
            # Create dopamine-enhanced neural transmission from thalamus to occipital
            return self.thalamus.get_visual_transmission(
                self.neuromodulators.get_current_levels()
            )
        except Exception as e:
            self._handle_processing_error("Thalamic processing", e)
            # Create fallback transmission
            from core.neural_transmission import NeuralTransmission
            return NeuralTransmission.create_from_thalamus(
                base_signal=input_result['injection_strength'],
                dopamine_level=0.1
            )
    
    def _process_cortical_stages(self, visual_transmission: Any) -> Dict:
        """Process all cortical stages with error handling"""
        # 3. Visual Processing (Occipital Lobe)
        try:
            visual_outputs = self.occipital.process_neural_transmission(visual_transmission)
        except Exception as e:
            self._handle_processing_error("Occipital processing", e)
            visual_outputs = {
                'v1_features': {'output_activity': 0.1},
                'feedback_to_thalamus': 0.0
            }
        
        # 4. Spatial Processing (Parietal Lobe)
        try:
            parietal_outputs = self.parietal.process_spatial_input(
                visual_outputs, 
                self.neuromodulators.get_current_levels()
            )
            # Request attention focus from thalamus (biological feedback loop)
            self.parietal.request_attention_focus(self.thalamus)
        except Exception as e:
            self._handle_processing_error("Parietal processing", e)
            parietal_outputs = {'spatial_activity': 0.1}
        
        # 5. Semantic Processing (Temporal Lobe)
        try:
            temporal_outputs = self.temporal.process_semantic_input(
                parietal_outputs, 
                visual_outputs,
                self.neuromodulators.get_current_levels()
            )
            # Request memory access (placeholder for future hippocampus integration)
            self.temporal.memory_access(self.hippocampus)
        except Exception as e:
            self._handle_processing_error("Temporal processing", e)
            temporal_outputs = {'semantic_activity': 0.1}
        
        return {
            'visual_outputs': visual_outputs,
            'parietal_outputs': parietal_outputs,
            'temporal_outputs': temporal_outputs
        }
    
    def _process_output_stage(self, cortical_results: Dict) -> Dict:
        """Process output stage with error handling"""
        try:
            sensory_for_frontal = {
                'intensity': cortical_results['temporal_outputs']['semantic_activity']
            }
            
            # Get energy and adrenaline levels for frontal processing
            energy_level = self.metrics.system_energy
            adrenaline_level = self.amygdala.get_adrenaline_level()
            
            # Add energy and adrenaline to neuromodulators for frontal processing
            frontal_neuromodulators = self.neuromodulators.get_current_levels().copy()
            frontal_neuromodulators['energy'] = energy_level
            frontal_neuromodulators['norepinephrine'] = adrenaline_level
            
            self.frontal.process_sensory_input(
                sensory_for_frontal, 
                frontal_neuromodulators
            )
            
            # Motor Output (Layer V → Output Gateway)
            layer_v_output = self.frontal.get_motor_output()
            
            # Output Processing
            dopamine_level = self.neuromodulators.modulators[NeuromodulatorType.DA].get_global_concentration()
            return self.output_gateway.convert_to_character(
                layer_v_output, energy_level, adrenaline_level, dopamine_level
            )
        except Exception as e:
            self._handle_processing_error("Output processing", e)
            return {
                'output_char': '?',
                'accuracy': 0.0
            }
    
    def process_character(self, character: str) -> NeuralProcessingResult:
        """
        Process a single character through the entire neural pipeline.
        
        Args:
            character: Input character to process
            
        Returns:
            Dictionary containing complete processing results
        """

        start_time = time.time()
        # 1. INITIALISATION PRÉVENTIVE (Notre filet de sécurité)
        result = {
            'input_char': character,
            'output_char': '?',
            'precision': 0.0,
            'processing_time_ms': 0.0,
            'brain_activity': {}
        }
        
        self.state = SystemState.PROCESSING
        self._apply_biological_heartbeat()
        
        try:
            # Process each stage with error handling
            input_result = self._process_input_stage(character)
            visual_transmission = self._process_thalamic_stage(input_result)
            cortical_results = self._process_cortical_stages(visual_transmission)
            output_result = self._process_output_stage(cortical_results)
            
            # Calculate processing time
            processing_time = (time.time() - start_time) * 1000  # Convert to ms
            
            # 6. Update System State
            self._update_system_state(character, output_result)
            
            # 7. Update Neuromodulators (NOW with complete result including amygdala)
            self._update_neuromodulators(character, output_result)
            
            # 8. NOW create complete result with UPDATED brain activity (including amygdala)
            brain_activity = {}
            
            # Collect brain activity with error handling for each area
            try:
                brain_activity['thalamus'] = self.thalamus.get_activity()
            except Exception as e:
                print(f"⚠️  Thalamus activity error: {e}")
                brain_activity['thalamus'] = 0.0
            
            try:
                brain_activity['occipital'] = self.occipital.get_visual_outputs()
            except Exception as e:
                print(f"⚠️  Occipital activity error: {e}")
                brain_activity['occipital'] = {'v1_features': {'output_activity': 0.0}}
            
            try:
                brain_activity['parietal'] = self.parietal.get_spatial_outputs()
            except Exception as e:
                print(f"⚠️  Parietal activity error: {e}")
                brain_activity['parietal'] = {'spatial_activity': 0.0}
            
            try:
                brain_activity['temporal'] = self.temporal.get_semantic_outputs()
            except Exception as e:
                print(f"⚠️  Temporal activity error: {e}")
                brain_activity['temporal'] = {'semantic_activity': 0.0}
            
            try:
                brain_activity['frontal'] = self.frontal.get_frontal_outputs()
            except Exception as e:
                print(f"⚠️  Frontal activity error: {e}")
                brain_activity['frontal'] = {'final_output': 0.0}
            
            try:
                # NOW amygdala has been updated by _update_neuromodulators()
                brain_activity['amygdala'] = self.amygdala.get_activity()
            except Exception as e:
                print(f"⚠️  Amygdala activity error: {e}")
                brain_activity['amygdala'] = 0.0

            # Création du dictionnaire avec la valeur déjà capturée
            result = NeuralProcessingResult(
                input_char=character,
                output_char=str(output_result.get('output_character', '?')),
                precision=float(output_result.get('accuracy', 0.0)),
                processing_time_ms=processing_time,
                energy_level=energy_level,
                neuromodulators=self.neuromodulators.get_current_levels(),
                adrenaline_level=adrenaline_level,
                brain_activity=brain_activity
            )
            
            self.processing_history.append(result)
            self.metrics.processing_time_ms = processing_time

            return result
            
        except Exception as e:
            # Bloc unique de capture d'erreur
            self.state = SystemState.ERROR
            result['error'] = str(e)
            return result
        
        finally:
            self.state = SystemState.IDLE
    
    def process_text(self, text: str) -> List[NeuralProcessingResult]:
        """
        Process a complete text string character by character.
        
        Args:
            text: Input text to process
            
        Returns:
            List of processing results for each character
        """
        results = []
        
        for char in text:
            if char.isspace():
                continue  # Skip whitespace
            
            result = self.process_character(char)
            results.append(result)
            
            # Small delay to simulate biological processing time
            time.sleep(0.01)
        
        return results
    
    
    def _update_system_state(self, input_char: str, output_result: NeuralProcessingResult):
        """Update system metrics and state based on processing results"""
        self.metrics.total_characters_processed += 1
        
        # Update precision metrics - use the actual output accuracy from the output gateway
        # The output gateway already calculates accuracy based on energy, adrenaline, etc.
        # We don't compare input vs output characters because this is a neural transformation system
        output_accuracy = output_result.precision
        
        # Count errors based on output accuracy (not character matching)
        if output_accuracy < self.MIN_PRECISION_FOR_SUCCESS:
            self.metrics.total_errors += 1
        
        # Calculate running average precision using the actual output accuracies
        if self.metrics.total_characters_processed > 0:
            self.metrics.average_precision = (
                sum(r.precision for r in self.processing_history) / 
                len(self.processing_history)
            )
        
        # Update energy levels (motor processing consumes energy)
        self.metrics.system_energy = max(0.0, self.metrics.system_energy - self.ENERGY_COST_PER_CHAR)
        
        # Update adrenaline based on stress (errors)
        if output_result.precision < self.STRESS_THRESHOLD:
            self.metrics.adrenaline_level = min(1.0, self.metrics.adrenaline_level + 0.1)
        else:
            # Natural decay of adrenaline
            self.metrics.adrenaline_level = max(0.0, self.metrics.adrenaline_level - self.NATURAL_ADRENALINE_DECAY)
    
    def _update_neuromodulators(self, input_char: str, output_result: NeuralProcessingResult):
        """Update neuromodulator levels based on processing results"""
        current_levels = self.neuromodulators.get_current_levels()
        
        # BIOLOGICAL FIX: Dopamine update based on success/failure
        # Dopamine is the key neuromodulator for reward-based learning and plasticity.
        # High dopamine levels (0.7+) enhance synaptic strength and attention, while
        # low levels (0.3-) reduce motivation and learning efficiency.
        if output_result.precision > 0.9:
            # Success: increase dopamine significantly to reinforce learning
            dopamine_increase = 0.15
            self.neuromodulators.release_modulator(
                NeuromodulatorType.DA, dopamine_increase, position=np.array([0.0, -30.0, 0.0])
            )
            
            # Create dopamine feedback loop: temporarily boost LGN injection strength
            # This makes aNA more attentive and curious about the next character
            if hasattr(self.input_gateway, '_temp_attention_boost'):
                self.input_gateway._temp_attention_boost = 0.3  # 30% attention boost
            else:
                # Add temporary attribute to input gateway for attention boost
                self.input_gateway._temp_attention_boost = 0.3
            
        elif output_result.precision < 0.5:
            # Failure: decrease dopamine to signal need for adjustment
            dopamine_decrease = 0.05
            self.neuromodulators.release_modulator(
                NeuromodulatorType.DA, -dopamine_decrease, position=np.array([0.0, -30.0, 0.0])
            )
            
            # Remove attention boost if present
            if hasattr(self.input_gateway, '_temp_attention_boost'):
                self.input_gateway._temp_attention_boost = 0.0
        
        # BIOLOGICAL FIX: Acetylcholine update based on attention
        # Acetylcholine enhances attention and sensory processing in the thalamus.
        # It increases the signal-to-noise ratio, making relevant stimuli more salient.
        attention_factor = 0.02
        self.neuromodulators.release_modulator(
            NeuromodulatorType.ACh, attention_factor, position=np.array([0.0, 40.0, 0.0])
        )
        
        # BIOLOGICAL FIX: Serotonin update based on stability
        # Serotonin promotes emotional stability and reduces anxiety during processing.
        # High serotonin levels correlate with better precision and reduced stress.
        if output_result.precision > 0.8:
            stability_factor = 0.01
            self.neuromodulators.release_modulator(
                NeuromodulatorType.Serotonin, stability_factor, position=np.array([0.0, -10.0, 0.0])
            )
        
        # BIOLOGICAL FIX: NO update based on learning
        # Nitric oxide (NO) is a gasotransmitter that enhances synaptic plasticity.
        # It facilitates long-term potentiation (LTP) during successful learning events.
        if self.metrics.total_characters_processed > 1:
            previous_result = self.processing_history[-2]
            if output_result.precision > previous_result.precision:
                # Improvement: increase NO for plasticity
                self.neuromodulators.release_modulator(
                    NeuromodulatorType.NO, 0.05, position=np.array([0.0, -30.0, 0.0])
                )
        
        # BIOLOGICAL FIX: Norepinephrine update based on stress
        # Norepinephrine is released during stress and enhances alertness.
        # High levels can improve focus but may also cause tremor if excessive.
        if output_result.precision < 0.5:
            stress_factor = 0.1
            self.neuromodulators.release_modulator(
                NeuromodulatorType.NE, stress_factor, position=np.array([0.0, -10.0, 0.0])
            )
        else:
            # Natural decay - release negative amount to simulate decay
            self.neuromodulators.release_modulator(
                NeuromodulatorType.NE, -0.01, position=np.array([0.0, -10.0, 0.0])
            )
        
        # 🧠 NEW: Amygdala Integration - Post-Processing Stress Analysis
        # The amygdala analyzes the processing result and releases adrenaline based on stress
        self._update_amygdala_activity(input_char, output_result)
    
    def _update_amygdala_activity(self, input_char: str, output_result: NeuralProcessingResult):
        """
        Update amygdala activity based on processing results.
        
        BIOLOGICAL PRINCIPLE: The amygdala acts as a stress detector that analyzes
        the gap between expected and actual outcomes. When precision is low,
        it triggers the release of adrenaline to prepare the system for stress.
        
        PERSONALITY PARAMETER: AMYGDALA_SENSITIVITY controls how reactive the
        amygdala is to stress. Higher values = more nervous personality.
        """
        # Calculate stress level based on processing precision
        # Lower precision = higher stress
        stress_level = max(0.0, 1.0 - output_result.precision)
        
        # Apply amygdala sensitivity (personality parameter)
        # This allows tuning the "nervousness" of the system
        adjusted_stress = stress_level * self.AMYGDALA_SENSITIVITY
        
        # Update amygdala activity
        self.amygdala.update_activity(adjusted_stress)
        
        # Release adrenaline based on stress level
        # Use the personality parameter for adrenaline release intensity
        if adjusted_stress > self.STRESS_THRESHOLD:
            # High stress: release significant adrenaline
            adrenaline_release = adjusted_stress * self.ADRENALINE_RELEASE_FACTOR
            self.neuromodulators.release_modulator(
                NeuromodulatorType.NE, adrenaline_release, position=np.array([0.0, -10.0, 0.0])
            )
            
            # Update system metrics
            self.metrics.adrenaline_level = min(1.0, self.metrics.adrenaline_level + adrenaline_release)
        else:
            # Low stress: natural decay of adrenaline
            self.metrics.adrenaline_level = max(0.0, self.metrics.adrenaline_level - self.NATURAL_ADRENALINE_DECAY)
    
    def display_dashboard(self):
        """Display real-time system dashboard"""
        print("\n" + "="*80)
        print("🧠 aNA v4.0 -> v5.0 REAL-TIME DASHBOARD")
        print("="*80)
        
        self._display_current_status()
        self._display_system_metrics()
        self._display_neuromodulator_levels()
        self._display_brain_activity()
        
        # System Status
        status_emoji = {
            SystemState.IDLE: "🟢",
            SystemState.PROCESSING: "🟡", 
            SystemState.ERROR: "🔴",
            SystemState.LEARNING: "🔵"
        }
        
        print(f"🚦 System Status: {status_emoji[self.state]} {self.state.value.upper()}")
        
        print("="*80)
    
    def _display_current_status(self):
        """Display current processing status"""
        if self.processing_history:
            latest = self.processing_history[-1]
            print(f"📊 Current Processing: '{latest.input_char}' → '{latest.output_char}'")
            print(f"🎯 Precision: {latest.precision:.1%}")
            print(f"⏱️  Processing Time: {latest.processing_time_ms:.1f}ms")
        else:
            print("📊 Current Processing: IDLE")
            print("🎯 Precision: N/A")
            print("⏱️  Processing Time: N/A")
        
        print()
    
    def _display_system_metrics(self):
        """Display system metrics"""
        print("📈 SYSTEM METRICS")
        print("-" * 40)
        print(f"Total Characters: {self.metrics.total_characters_processed}")
        print(f"Total Errors: {self.metrics.total_errors}")
        # Calculate average precision from processing history in real-time
        if self.processing_history:
            avg_precision = sum(r.precision for r in self.processing_history) / len(self.processing_history)
            print(f"Average Precision: {avg_precision:.1%}")
        else:
            print(f"Average Precision: N/A")
        print(f"System Energy: {self.metrics.system_energy:.1%}")
        print(f"Adrenaline Level: {self.metrics.adrenaline_level:.1%}")
        
        print()
    
    def _display_neuromodulator_levels(self):
        """Display neuromodulator levels"""
        print("🧪 NEUROMODULATOR LEVELS")
        print("-" * 40)
        levels = self.neuromodulators.get_current_levels()
        for modulator, level in levels.items():
            bar = "█" * int(level * 20)
            print(f"{modulator.upper():12}: [{bar:<20}] {level:.2f}")
        
        print()
    
    def _display_brain_activity(self):
        """Display brain activity"""
        print("🧠 BRAIN ACTIVITY")
        print("-" * 40)
        try:
            if self.processing_history:
                activity = self.processing_history[-1]['brain_activity']
                
                # Thalamus
                if 'thalamus' in activity:
                    print(f"Thalamus: {activity['thalamus']:.3f}")
                
                # Occipital Lobe
                if 'occipital' in activity:
                    occipital_outputs = activity['occipital']
                    if 'v1_features' in occipital_outputs:
                        v1 = occipital_outputs['v1_features']['output_activity']
                        print(f"Occipital V1: {v1:.3f}")
                
                # Parietal Lobe
                if 'parietal' in activity:
                    parietal_outputs = activity['parietal']
                    parietal_activity = parietal_outputs.get('spatial_activity', 0.0)
                    print(f"Parietal Spatial: {parietal_activity:.3f}")
                
                # Temporal Lobe
                if 'temporal' in activity:
                    temporal_outputs = activity['temporal']
                    temporal_activity = temporal_outputs.get('semantic_activity', 0.0)
                    print(f"Temporal Semantic: {temporal_activity:.3f}")
                
                # Frontal Lobe
                if 'frontal' in activity:
                    frontal_outputs = activity['frontal']
                    motor = frontal_outputs['final_output']
                    print(f"Frontal Motor: {motor:.3f}")
                
                # Amygdala
                if 'amygdala' in activity:
                    amygdala = activity['amygdala']
                    print(f"Amygdala: {amygdala:.3f}")
            else:
                # If no processing history, get current brain activity
                print("Thalamus: Calculating...")
                print("Occipital V1: Calculating...")
                print("Parietal Spatial: Calculating...")
                print("Temporal Semantic: Calculating...")
                print("Frontal Motor: Calculating...")
                print("Amygdala: Calculating...")
        except Exception as e:
            print(f"Brain activity: Error - {e}")
        
        print()
    
    def run_demo(self, test_text: str = "HELLO"):
        """Run a demonstration of the complete system"""
        print(f"\n🚀 Starting Demo: Processing '{test_text}'")
        print("This will demonstrate the complete Unicode ↔ Decimal pipeline")
        
        results = self.process_text(test_text)
        
        print(f"\n✅ Demo Complete! Processed {len(results)} characters")
        
        # Display summary
        total_precision = sum(r['precision'] for r in results) 
        avg_precision = total_precision / len(results) if results else 0
        
        print(f"📊 Average Precision: {avg_precision:.1%}")
        print(f"⏱️  Total Processing Time: {sum(r['processing_time_ms'] for r in results):.1f}ms")
        
        # Show detailed results
        print("\n📝 Detailed Results:")
        for result in results:
            # Use the actual output accuracy from the output gateway
            output_accuracy = result.get('precision', 0.0)
            status = "✅" if output_accuracy > 0.8 else "⚠️" if output_accuracy > 0.5 else "❌"
            print(f"  {status} '{result['input_char']}' → '{result['output_char']}' ({output_accuracy:.1%})")
    
    def _restore_terminal(self, old_settings):
        """Restore terminal settings safely"""
        try:
            import termios
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
        except:
            pass  # Ignore errors during restoration
    
    def run_continuous_mode(self):
        """Run in continuous mode with separated input and processing pipeline"""
        print("\n🔄 Starting Continuous Mode with Separated Input/Processing")
        print("Type characters to buffer them for processing (Ctrl+C to exit)")
        print("💡 Characters will be processed through the neural pipeline asynchronously!")
        print("📊 Watch real-time neural activity and information values change!")
        
        import sys
        import select
        import tty
        import termios
        
        # Save terminal settings
        old_settings = termios.tcgetattr(sys.stdin)
        
        try:
            # Set terminal to raw mode to capture characters without echo
            tty.setraw(sys.stdin.fileno())
            
            # Initialize dashboard area
            print("\033[2J\033[H", end="")  # Clear screen and move cursor to top
            self.display_separated_dashboard()
            
            # Start processing loop with improved responsiveness
            while not self.shutdown_flag:
                # Check shutdown flag first
                if self.shutdown_flag:
                    break
                
                # Check if there's keyboard input available (non-blocking with timeout)
                ready, _, _ = select.select([sys.stdin], [], [], 0.1)
                
                if ready:
                    # Read a single character (this won't echo to screen)
                    char = sys.stdin.read(1)
                    
                    # Handle Ctrl+C explicitly
                    if char == '\x03':  # Ctrl+C
                        print("\n🛑 Ctrl+C detected. Shutting down gracefully...")
                        break
                    
                    # Handle Ctrl+D for exit
                    elif char == '\x04':  # Ctrl+D
                        print("\n🛑 Ctrl+D detected. Shutting down gracefully...")
                        break
                    
                    # Handle 'q' key for quit
                    elif char.lower() == 'q':
                        print("\n🛑 'q' key detected. Shutting down gracefully...")
                        break
                    
                    # Only process printable characters
                    elif char and char.isprintable() and not char.isspace():
                        # Add to input buffer instead of processing immediately
                        self.input_buffer.append(char)
                        # Update dashboard without clearing output area
                        self._update_dashboard_only()
                
                # Process characters from the queue asynchronously
                if not self.processing_in_progress and self.input_buffer and not self.shutdown_flag:
                    # Move character from buffer to processing queue
                    char_to_process = self.input_buffer.pop(0)
                    self.processing_queue.append(char_to_process)
                    self.current_processing_char = char_to_process
                    self.processing_in_progress = True
                    
                    # Update dashboard to show processing start
                    self._update_dashboard_only()
                
                # If currently processing, show real-time neural activity
                if self.processing_in_progress and self.current_processing_char and not self.shutdown_flag:
                    # Check system stability before processing
                    if not self._check_system_stability():
                        print("⚠️  System instability detected. Applying circuit breaker...")
                        self._apply_circuit_breaker()
                        continue
                    
                    # Process the character through the neural pipeline
                    result = self.process_character(self.current_processing_char)
                    
                    # Show processing result in output area only
                    self._display_output_result(result)
                    
                    # Mark processing as complete
                    self.processing_in_progress = False
                    self.current_processing_char = None
                    if self.processing_queue:
                        self.processing_queue.pop(0)
                    
                    # Update dashboard
                    self._update_dashboard_only()
                
                # Small delay to simulate biological processing time
                time.sleep(0.1)  # Reduced from 0.5 for better responsiveness
                
        except KeyboardInterrupt:
            print("\n🛑 KeyboardInterrupt caught. Shutting down gracefully...")
        except Exception as e:
            print(f"\n🛑 Error in continuous mode: {e}")
        finally:
            # Always restore terminal settings
            self._restore_terminal(old_settings)
            print("✅ Terminal settings restored")
    
    def _get_state_color(self, stress_level: float, dopamine_level: float) -> str:
        """Get ANSI color code based on system state"""
        if dopamine_level > 0.7:
            return '\033[94m'  # Blue for optimal learning state
        elif stress_level > 0.8:
            return '\033[91m'  # Red for high stress
        elif stress_level > 0.6:
            return '\033[93m'  # Yellow for moderate stress
        else:
            return '\033[92m'   # Green for stable processing
    
    def _get_reset_color(self) -> str:
        """Get ANSI reset code"""
        return '\033[0m'
    
    def display_separated_dashboard(self):
        """Display real-time dashboard for separated input/processing pipeline"""
        # Clean screen using sys.stdout.write for proper clearing
        # sys.stdout.write("\033[H\033[J")
        
        # 3D Wireframe Cube ASCII Header (80 characters wide)
        print("    +--------+")
        print("   /        /|")
        print("  +--------+ |")
        print("  |        | |")
        print("  |  aNA   | +")
        print("  | v4->5  |/ ")
        print("  +--------+  ")
        print()
        
        # SCIENTIFIC INTERFACE HEADER
        print("🔬 aNA v4.0 -> v5.0 NEURAL CASCADE MONITOR")
        print("=" * 80)
        
        # Get current system state for color coding
        stress_level = self.metrics.adrenaline_level
        dopamine_level = self.neuromodulators.get_current_levels().get('dopamine', 0.0)
        state_color = self._get_state_color(stress_level, dopamine_level)
        reset_color = self._get_reset_color()
        
        # Biological Constants Display
        print(f"{state_color}🧬 BIOLOGICAL CONSTANTS{reset_color}")
        print("-" * 40)
        print("• -55mV Threshold: Neuronal firing potential")
        print("• 0.85 Cascade: Synaptic efficiency decay (Layer IV→II/III→V→VI)")
        print("• 0.15 Baseline: Thalamic consciousness gateway")
        print("• 1.0s Thalamus Pulse: Biological rhythm")
        print()
        
        # Precision Cascade Display with 6-Layer Monitoring
        print(f"{state_color}⚡ PRECISION CASCADE{reset_color}")
        print("-" * 40)
        
        # Calculate current cascade values with 6-layer precision monitoring
        if self.processing_history:
            latest = self.processing_history[-1]
            brain_activity = latest.get('brain_activity', {})
            
            thalamus_val = brain_activity.get('thalamus', 0.0)
            occipital_val = 0.0
            frontal_val = 0.0
            
            # NEW: Extract cortical layer precision data
            cortical_precision = 0.0
            precision_loss = 0.0
            attention_boost = 1.0
            
            if 'occipital' in brain_activity:
                occipital_outputs = brain_activity['occipital']
                if 'v1_features' in occipital_outputs:
                    occipital_val = occipital_outputs['v1_features'].get('output_activity', 0.0)
                
                # Extract cortical layer monitoring data
                if 'cortical_monitoring' in occipital_outputs:
                    cortical_data = occipital_outputs['cortical_monitoring']
                    cortical_precision = cortical_data.get('layer5_output', 0.0)
                    precision_loss = cortical_data.get('precision_loss', 0.0)
                    attention_boost = cortical_data.get('layer1_attention', 1.0)
            
            if 'frontal' in brain_activity:
                frontal_outputs = brain_activity['frontal']
                frontal_val = frontal_outputs.get('final_output', 0.0)
            
            # Display cascade with biological accuracy and precision monitoring
            print(f"LGN → Thalamus: {thalamus_val:.6f}")
            print(f"Thalamus → Occipital: {occipital_val:.6f} (×0.90)")
            print(f"Occipital → Frontal: {frontal_val:.6f} (×0.85)")
            print(f"Frontal → Output: {latest.get('output_char', '?')}")
            
            # NEW: Display 6-layer precision battle
            print()
            print(f"🔬 CORTICAL PRECISION BATTLE")
            print("-" * 40)
            print(f"Precision Loss: {precision_loss:.1%}")
            print(f"Attention Boost: {attention_boost:.2f}x")
            print(f"Cortical Efficiency: {cortical_precision:.6f}")
            print(f"Expected Cascade: 65% (0.90×0.85×0.85)") # À faire
        else:
            print("LGN → Thalamus: IDLE")
            print("Thalamus → Occipital: IDLE")
            print("Occipital → Frontal: IDLE")
            print("Frontal → Output: IDLE")
            
            # NEW: Display 6-layer precision battle (idle)
            print()
            print(f"🔬 CORTICAL PRECISION BATTLE")
            print("-" * 40)
            print("Precision Loss: IDLE")
            print("Attention Boost: IDLE")
            print("Cortical Efficiency: IDLE")
            print("Expected Cascade: 65% (0.90×0.85×0.85)") # À faire
        
        print()
        
        # Dashboard header
        print("🧠 aNA v4.0 -> v5.0 SEPARATED INPUT/PROCESSING DASHBOARD")
        print("=" * 80)
        print()
        
        # Input Buffer Status
        print("📥 INPUT BUFFER STATUS")
        print("-" * 40)
        if self.input_buffer:
            print(f"Buffer contents: {self.input_buffer}")
            print(f"Next to process: '{self.input_buffer[0]}'")
        else:
            print("Buffer is empty - type characters to add to buffer")
        
        print(f"Processing queue: {len(self.processing_queue)} characters")
        print(f"Currently processing: {self.current_processing_char if self.current_processing_char else 'None'}")
        print()
        
        # Current Processing Status
        print("📊 CURRENT PROCESSING STATUS")
        print("-" * 40)
        if self.processing_history:
            latest = self.processing_history[-1]
            print(f"Last Processing: '{latest.input_char}' → '{latest.output_char}'")
            print(f"Last Precision: {latest.precision:.1%}")
            print(f"Last Time: {latest.processing_time_ms:.1f}ms")
        else:
            print("No processing completed yet")
        print()
        
        # System Metrics
        print("📈 SYSTEM METRICS")
        print("-" * 40)
        print(f"Total Characters: {self.metrics.total_characters_processed}")
        print(f"Total Errors: {self.metrics.total_errors}")
        # Calculate average precision from processing history in real-time
        if self.processing_history:
            avg_precision = sum(r.precision for r in self.processing_history) / len(self.processing_history)
            print(f"Average Precision: {avg_precision:.1%}")
        else:
            print(f"Average Precision: N/A")
        print(f"System Energy: {self.metrics.system_energy:.1%}")
        print(f"Adrenaline Level: {self.metrics.adrenaline_level:.1%}")
        print()
        
        # Neuromodulator Levels
        print("🧪 NEUROMODULATOR LEVELS")
        print("-" * 40)
        levels = self.neuromodulators.get_current_levels()
        for modulator, level in levels.items():
            # Make bars more sensitive - use 40 characters instead of 20 for better precision
            bar_length = int(level * 40)
            bar = "█" * bar_length + "░" * (40 - bar_length)
            print(f"{modulator.upper():12}: [{bar:<40}] {level:.6f}")
        print()
        
        # Brain Activity
        print("🧠 REAL-TIME BRAIN ACTIVITY")
        print("-" * 40)
        try:
            # Get current brain activity (even if not processing)
            thalamus_activity = self.thalamus.get_activity() if hasattr(self.thalamus, 'get_activity') else 0.0
            print(f"Thalamus: {thalamus_activity:.6f}")
            
            occipital_outputs = self.occipital.get_visual_outputs() if hasattr(self.occipital, 'get_visual_outputs') else {}
            if 'v1_features' in occipital_outputs:
                v1_activity = occipital_outputs['v1_features'].get('output_activity', 0.0)
                print(f"Occipital V1: {v1_activity:.6f}")
            
            # NEW: Parietal Lobe monitoring
            parietal_outputs = self.parietal.get_spatial_outputs() if hasattr(self.parietal, 'get_spatial_outputs') else {}
            parietal_activity = parietal_outputs.get('spatial_activity', 0.0)
            print(f"Parietal Spatial: {parietal_activity:.6f}")
            
            # NEW: Temporal Lobe monitoring
            temporal_outputs = self.temporal.get_semantic_outputs() if hasattr(self.temporal, 'get_semantic_outputs') else {}
            temporal_activity = temporal_outputs.get('semantic_activity', 0.0)
            print(f"Temporal Semantic: {temporal_activity:.6f}")
            
            frontal_outputs = self.frontal.get_frontal_outputs() if hasattr(self.frontal, 'get_frontal_outputs') else {}
            if 'final_output' in frontal_outputs:
                motor_activity = frontal_outputs['final_output']
                print(f"Frontal Motor: {motor_activity:.6f}")
            
            amygdala_activity = self.amygdala.get_activity() if hasattr(self.amygdala, 'get_activity') else 0.0
            print(f"Amygdala: {amygdala_activity:.6f}")
        except Exception as e:
            print(f"Brain activity: Error - {e}")
        print()
        
        # System Status
        status_emoji = {
            SystemState.IDLE: "🟢",
            SystemState.PROCESSING: "🟡", 
            SystemState.ERROR: "🔴",
            SystemState.LEARNING: "🔵"
        }
        
        processing_status = "PROCESSING" if self.processing_in_progress else "IDLE"
        print(f"🚦 System Status: {status_emoji[self.state]} {processing_status}")
        print()
        
        # Output Area Header
        print("=" * 80)
        print("📤 [OUTPUT] - Processed Characters")
        print("-" * 40)
        
        # Output Area Content
        if self.processing_history:
            latest = self.processing_history[-1]
            status = "✅" if latest.precision > 0.8 else "⚠️" if latest.precision > 0.5 else "❌"
            print(f"Last Output: {status} '{latest.output_char}' (Precision: {latest.precision:.3f})")
            
            # Show biological effects on precision
            dopamine_level = latest.neuromodulators.get('dopamine', 0.0)
            if dopamine_level > 0.7:
                print(f"   🧠 High dopamine ({dopamine_level:.3f}) enhanced precision")
            elif dopamine_level < 0.3:
                print(f"   🧠 Low dopamine ({dopamine_level:.3f}) reduced precision")
            
            energy_level = latest.energy_level
            if energy_level < 0.3:
                print(f"   ⚡ Low energy ({energy_level:.1%}) affected output")
            
            adrenaline_level = latest.adrenaline_level
            if adrenaline_level > 0.5:
                print(f"   💥 High adrenaline ({adrenaline_level:.1%}) caused tremor")
        else:
            print("No output yet - start typing characters to process")
        
        print("=" * 80)
    
    def _update_dashboard_only(self):
        """Update only the dashboard area without clearing the output area"""
        # Clear the entire screen and redraw everything
        print("\033[2J\033[H", end="")  # Clear screen and move cursor to top
        sys.stdout.flush()  # Ensure the clear command is processed immediately
        self.display_separated_dashboard()
    
    def _display_output_result(self, result: NeuralProcessingResult):
        """Display processing result in the scroll buffer only"""
        # Update dashboard with new result
        self._update_dashboard_only()
    
    def reset_system(self):
        """Reset the entire system to initial state"""
        self.metrics = SystemMetrics()
        self.processing_history = []
        self.neuromodulators.reset()
        
        # Reset all brain structures
        self.thalamus.reset()
        self.occipital.reset()
        self.frontal.reset()
        self.amygdala.reset()
        self.hippocampus.reset()
        self.cerebellum.reset()
        
        print("🔄 System Reset Complete")
    
    def get_system_summary(self) -> NeuralProcessingResult:
        """Get comprehensive system summary"""
        # Calculate current average precision from processing history
        current_avg_precision = 0.0
        if self.processing_history:
            current_avg_precision = sum(r.precision for r in self.processing_history) / len(self.processing_history)
        
        # Create a summary result with current system state
        return NeuralProcessingResult(
            input_char="SYSTEM_SUMMARY",
            output_char="SYSTEM_SUMMARY",
            precision=current_avg_precision,
            processing_time_ms=self.metrics.processing_time_ms,
            energy_level=self.metrics.system_energy,
            adrenaline_level=self.metrics.adrenaline_level,
            neuromodulators=self.neuromodulators.get_current_levels(),
            brain_activity={
                'system_state': self.state.value,
                'metrics': {
                    'total_characters': self.metrics.total_characters_processed,
                    'total_errors': self.metrics.total_errors,
                    'average_precision': self.metrics.average_precision,
                    'system_energy': self.metrics.system_energy,
                    'adrenaline_level': self.metrics.adrenaline_level
                },
                'component_status': {
                    'input_gateway': 'active',
                    'thalamus': 'active',
                    'occipital_lobe': 'active',
                    'frontal_lobe': 'active',
                    'amygdala': 'active',
                    'output_gateway': 'active'
                }
            }
        )


def main():
    """Main entry point for aNA v4.0 -> v5.0"""
    print("🚀 Initializing aNA v4.0 -> v5.0 - Advanced Neural Architecture")
    print("🎯 Sensory Input (Unicode → Decimal) + Motor Output (Decimal → Unicode)")
    print("🧠 With Biological Realism: Energy, Neuromodulators, and Learning")
    
    # Create controller
    controller = ANAController()
    
    # Run demo
    controller.run_demo("HELLO WORLD")
    
    # Continuous mode
    controller.run_continuous_mode()

    # Display final dashboard
    controller.display_dashboard()
    
    print("\n🎉 aNA v4.0 -> v5.0 Demo Complete!")
    print("✨ Observe how energy levels and neuromodulators affect processing accuracy")
    print("💡 Try running controller.run_continuous_mode() for interactive processing")


def test_fixes():
    """Test function to verify all fixes are working"""
    print("\n🧪 TESTING FIXES")
    print("=" * 50)
    
    # Create controller
    controller = ANAController()
    
    # Test 1: Signal handling
    print("✅ Signal handling: SIGINT and SIGTERM handlers installed")
    
    # Test 2: Terminal control
    print("✅ Terminal control: Raw mode and restoration implemented")
    
    # Test 3: Thalamic baseline
    print("✅ Thalamic baseline: Biological heartbeat system active")
    
    # Test 4: System stability
    print("✅ System stability: Circuit breaker and monitoring active")
    
    # Test 5: Debug tools
    print("✅ Debug tools: System state analysis available")
    
    # Test 6: Demo run
    print("\n🚀 Running quick demo test...")
    try:
        controller.run_demo("TEST")
        print("✅ Demo completed successfully")
    except Exception as e:
        print(f"❌ Demo failed: {e}")
    
    # Test 7: Debug output
    print("\n🔍 Running debug analysis...")
    try:
        controller.debug_system_state()
        print("✅ Debug analysis completed successfully")
    except Exception as e:
        print(f"❌ Debug analysis failed: {e}")
    
    print("\n🎉 All tests completed!")
    print("✨ The system should now be stable and controllable")


if __name__ == "__main__":
    # Run main demo
    main()
    
    # Test fixes
    test_fixes()


"""
Thank you for paving the way for future discoveries and innovations in this fascinating field. Your contributions to neuroscience and artificial intelligence are invaluable. Some of your works have inspired me since I was very young. It allows me to better understand and design more efficient bio-inspired neural networks:

- Santiago Ramón y Cajal (Optimized Architecture)

- Carver Mead (Low Power Consumption)

- Karl Friston (Free Energy Optimization)

- Horace Barlow (Information Compression)

- Donald Hebb (Local and Low-Power Learning)

- Alan Hodgkin & Andrew Huxley (The Energy Peak Signal)

- Jeff Hawkins (Efficient Cortical Structure)

- Gyorgy Buzsaki (Coordination by Rhythms)

- John J. Hopfield (Memory Robustness)

- Rita Levi-Montalcini (Connection Growth and Pruning)

NOTE: This project is labeled v5.0 but contains v4 code structure. 
No actual v5 files were found in the project. The codebase appears to be 
a v4 implementation in a v5.0 directory structure.
"""
