#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Integration module for aNA v5.0 Dashboard

This module provides seamless integration between the neural dashboard
and the existing aNA v5.0 architecture, enabling real-time monitoring
of all brain structures and processing pipelines.

Architecture, concept and supervision: Benoit Theriault
Collaboration, research and code: Cline
"""

import time
import threading
from typing import Dict, Any, Optional, Callable
from dataclasses import dataclass

from scr.gui.dashboard import NeuralDashboard, create_dashboard

# Mock classes for brain structures (standalone version)
class MockThalamus:
    def get_activity(self):
        return 0.75
    def get_rtn_state(self):
        return 0.0

class MockOccipitalLobe:
    def __init__(self):
        self.cortical_layers = MockCorticalLayers()

class MockCorticalLayers:
    def get_layer_outputs(self):
        return {
            'layer4_output': 0.68,
            'layer23_output': 0.61,
            'layer5_output': 0.55,
            'precision_loss': 0.12,
            'layer1_attention': 1.25
        }

class MockFrontalLobe:
    def __init__(self):
        self.motor = MockMotor()

class MockMotor:
    def __init__(self):
        self.populations = {'layer5': MockLayer5()}

class MockLayer5:
    def get_average_activity(self):
        return 0.55

class MockParietalLobe:
    def get_activity(self):
        return 0.65

class MockTemporalLobe:
    def get_activity(self):
        return 0.70

class MockAmygdala:
    def get_activity(self):
        return 0.5
    def get_adrenaline_level(self):
        return 0.3

class MockHippocampus:
    def get_memory_signal(self):
        return 0.65
    def get_spatial_signal(self):
        return 0.65

class MockCerebellum:
    def get_motor_coordination_signal(self):
        return 0.80

class MockNeuromodulatorMatrix:
    def get_current_levels(self):
        return {
            'dopamine': 0.85,
            'acetylcholine': 0.72,
            'serotonin': 0.68,
            'norepinephrine': 0.45,
            'nitric_oxide': 0.35
        }

class MockInputGateway:
    def __init__(self):
        self.neuromodulators = MockNeuromodulatorMatrix()
        self.last_input_char = None

class MockOutputGateway:
    def __init__(self):
        self.last_output_char = None
        self.last_input_value = 0.5

# Type aliases for compatibility
Thalamus = MockThalamus
OccipitalLobe = MockOccipitalLobe
FrontalLobe = MockFrontalLobe
ParietalLobe = MockParietalLobe
TemporalLobe = MockTemporalLobe
Amygdala = MockAmygdala
Hippocampus = MockHippocampus
Cerebellum = MockCerebellum
InputGateway = MockInputGateway
OutputGateway = MockOutputGateway
NeuromodulatorType = str  # Simplified for standalone version


@dataclass
class IntegrationConfig:
    """Configuration for dashboard integration"""
    update_interval: float = 0.1  # 10 FPS update rate
    dashboard_refresh_rate: float = 0.1
    data_collection_interval: float = 0.05
    max_history_points: int = 100


class NeuralDataCollector:
    """
    Collects real-time data from all brain structures for dashboard visualization.
    
    This class acts as a bridge between the neural architecture and the dashboard,
    extracting relevant metrics and formatting them for visualization.
    """
    
    def __init__(self, config: Optional[IntegrationConfig] = None):
        self.config = config or IntegrationConfig()
        self.is_collecting = False
        self.collection_thread = None
        
        # Brain structure references
        self.thalamus: Optional[Thalamus] = None
        self.occipital: Optional[OccipitalLobe] = None
        self.frontal: Optional[FrontalLobe] = None
        self.parietal: Optional[ParietalLobe] = None
        self.temporal: Optional[TemporalLobe] = None
        self.amygdala: Optional[Amygdala] = None
        self.hippocampus: Optional[Hippocampus] = None
        self.cerebellum: Optional[Cerebellum] = None
        self.input_gateway: Optional[InputGateway] = None
        self.output_gateway: Optional[OutputGateway] = None
        
        # Data storage
        self.current_data: Dict[str, Any] = {}
        self.data_lock = threading.Lock()
    
    def connect_brain_structures(self, **structures):
        """Connect all brain structures for data collection"""
        self.thalamus = structures.get('thalamus')
        self.occipital = structures.get('occipital')
        self.frontal = structures.get('frontal')
        self.parietal = structures.get('parietal')
        self.temporal = structures.get('temporal')
        self.amygdala = structures.get('amygdala')
        self.hippocampus = structures.get('hippocampus')
        self.cerebellum = structures.get('cerebellum')
        self.input_gateway = structures.get('input_gateway')
        self.output_gateway = structures.get('output_gateway')
    
    def extract_thalamic_data(self) -> Dict[str, Any]:
        """Extract thalamic activity data"""
        if not self.thalamus:
            return {
                'thalamic_activity': 0.0,
                'thalamic_baseline': 0.15,
                'rtn_activity': 0.0
            }
        
        # Get total thalamic activity
        total_activity = self.thalamus.get_activity()
        
        # Get RTN (Reticular Thalamic Nucleus) activity
        rtn_activity = self.thalamus.get_rtn_state() if hasattr(self.thalamus, 'get_rtn_state') else 0.0
        
        return {
            'thalamic_activity': total_activity,
            'thalamic_baseline': 0.15,  # Biological baseline
            'rtn_activity': rtn_activity
        }
    
    def extract_cortical_data(self) -> Dict[str, Any]:
        """Extract cortical layer data from occipital and frontal lobes"""
        cortical_data = {
            'l4_output': 0.0,
            'l23_output': 0.0,
            'l5_output': 0.0,
            'precision_loss': 0.0,
            'attention_boost': 1.0
        }
        
        # Extract from occipital lobe if available
        if self.occipital and hasattr(self.occipital, 'cortical_layers'):
            occipital_layers = self.occipital.cortical_layers
            layer_outputs = occipital_layers.get_layer_outputs()
            
            cortical_data.update({
                'l4_output': layer_outputs.get('layer4_output', 0.0),
                'l23_output': layer_outputs.get('layer23_output', 0.0),
                'l5_output': layer_outputs.get('layer5_output', 0.0),
                'precision_loss': layer_outputs.get('precision_loss', 0.0),
                'attention_boost': layer_outputs.get('layer1_attention', 1.0)
            })
        
        # Extract from frontal lobe if available
        elif self.frontal and hasattr(self.frontal, 'motor'):
            frontal_motor = self.frontal.motor
            if hasattr(frontal_motor, 'populations'):
                layer5 = frontal_motor.populations.get('layer5')
                if layer5:
                    cortical_data['l5_output'] = layer5.get_average_activity()
        
        return cortical_data
    
    def extract_neuromodulator_data(self) -> Dict[str, float]:
        """Extract neuromodulator levels"""
        if not self.input_gateway or not hasattr(self.input_gateway, 'neuromodulators'):
            return {
                'dopamine': 0.1,
                'acetylcholine': 0.1,
                'serotonin': 0.1,
                'norepinephrine': 0.1,
                'no_gas': 0.1
            }
        
        # Get current neuromodulator levels
        modulator_levels = self.input_gateway.neuromodulators.get_current_levels()
        
        # Map to dashboard format
        dashboard_modulators = {
            'dopamine': modulator_levels.get('dopamine', 0.1),
            'acetylcholine': modulator_levels.get('acetylcholine', 0.1),
            'serotonin': modulator_levels.get('serotonin', 0.1),
            'norepinephrine': modulator_levels.get('norepinephrine', 0.1),
            'no_gas': modulator_levels.get('nitric_oxide', 0.1)
        }
        
        return dashboard_modulators
    
    def extract_system_data(self) -> Dict[str, Any]:
        """Extract system-wide data"""
        system_data = {
            'energy_level': 1.0,
            'stress_level': 0.0,
            'adrenaline_level': 0.0,
            'memory_strength': 0.0,
            'consolidation_rate': 0.0,
            'memory_traces': 0
        }
        
        # Extract from amygdala (stress and adrenaline)
        if self.amygdala:
            amygdala_activity = self.amygdala.get_activity()
            adrenaline_level = self.amygdala.get_adrenaline_level()
            
            system_data.update({
                'stress_level': amygdala_activity,
                'adrenaline_level': adrenaline_level
            })
        
        # Extract from hippocampus (memory)
        if self.hippocampus:
            memory_signal = self.hippocampus.get_memory_signal()
            spatial_signal = self.hippocampus.get_spatial_signal()
            
            system_data.update({
                'memory_strength': memory_signal,
                'consolidation_rate': spatial_signal,
                'memory_traces': len(getattr(self.hippocampus, 'dentate_gyrus', {}).get('fear_memories', {}))
            })
        
        # Extract from cerebellum (coordination)
        if self.cerebellum:
            coordination_signal = self.cerebellum.get_motor_coordination_signal()
            system_data['coordination_level'] = coordination_signal
        
        return system_data
    
    def extract_processing_data(self) -> Dict[str, Any]:
        """Extract current processing status"""
        processing_data = {
            'input_character': '?',
            'output_character': '?',
            'accuracy': 0.0,
            'processing_time_ms': 0.0
        }
        
        # Extract from input gateway
        if self.input_gateway:
            if hasattr(self.input_gateway, 'last_input_char'):
                processing_data['input_character'] = self.input_gateway.last_input_char or '?'
        
        # Extract from output gateway
        if self.output_gateway:
            if hasattr(self.output_gateway, 'last_output_char'):
                processing_data['output_character'] = self.output_gateway.last_output_char or '?'
            if hasattr(self.output_gateway, 'last_input_value'):
                # Calculate accuracy based on input/output comparison
                input_val = self.output_gateway.last_input_value
                # This is a simplified accuracy calculation
                processing_data['accuracy'] = max(0.0, 1.0 - abs(input_val - 0.5))
        
        return processing_data
    
    def collect_data(self) -> Dict[str, Any]:
        """Collect all neural data for dashboard"""
        with self.data_lock:
            # Collect data from all sources
            thalamic_data = self.extract_thalamic_data()
            cortical_data = self.extract_cortical_data()
            neuromodulator_data = self.extract_neuromodulator_data()
            system_data = self.extract_system_data()
            processing_data = self.extract_processing_data()
            
            # Combine all data
            self.current_data = {
                **thalamic_data,
                **cortical_data,
                **neuromodulator_data,
                **system_data,
                **processing_data
            }
            
            return self.current_data
    
    def start_collection(self):
        """Start background data collection"""
        if self.is_collecting:
            return
        
        self.is_collecting = True
        self.collection_thread = threading.Thread(target=self._collection_loop, daemon=True)
        self.collection_thread.start()
    
    def stop_collection(self):
        """Stop background data collection"""
        self.is_collecting = False
        if self.collection_thread and self.collection_thread.is_alive():
            self.collection_thread.join(timeout=1.0)
    
    def _collection_loop(self):
        """Background collection loop"""
        while self.is_collecting:
            self.collect_data()
            time.sleep(self.config.data_collection_interval)


class DashboardController:
    """
    Main controller for the neural dashboard integration.
    
    This class manages the connection between the aNA v5.0 system and
    the dashboard, handling data flow and user interaction.
    """
    
    def __init__(self, config: Optional[IntegrationConfig] = None):
        self.config = config or IntegrationConfig()
        
        # Initialize dashboard
        self.dashboard = create_dashboard()
        self.dashboard.config.refresh_rate = self.config.dashboard_refresh_rate
        
        # Initialize data collector
        self.data_collector = NeuralDataCollector(self.config)
        
        # Processing callbacks
        self.processing_callback: Optional[Callable] = None
        
        # State management
        self.is_running = False
    
    def connect_brain_system(self, controller):
        """Connect to the main aNA controller"""
        # Connect all brain structures
        self.data_collector.connect_brain_structures(
            thalamus=controller.thalamus,
            occipital=controller.occipital,
            frontal=controller.frontal,
            parietal=controller.parietal,
            temporal=controller.temporal,
            amygdala=controller.amygdala,
            hippocampus=controller.hippocampus,
            cerebellum=controller.cerebellum,
            input_gateway=controller.input_gateway,
            output_gateway=controller.output_gateway
        )
        
        # Set processing callback
        self.processing_callback = controller.process_character
    
    def process_input_char(self, char: str):
        """Process an input character through the neural pipeline"""
        if self.processing_callback:
            try:
                # Process the character
                result = self.processing_callback(char)
                
                # Update dashboard with processing result
                self.update_dashboard_with_result(result)
                
                # Add to dashboard buffers
                self.dashboard.add_input_char(char)
                self.dashboard.add_output_char(result.get('output_character', '?'))
                
                return result
            except Exception as e:
                print(f"Error processing character '{char}': {e}")
                return None
        return None
    
    def update_dashboard_with_result(self, result: Dict[str, Any]):
        """Update dashboard with processing result"""
        # Convert result to dashboard format
        dashboard_data = self._convert_result_to_dashboard_format(result)
        self.dashboard.update_data(dashboard_data)
    
    def _convert_result_to_dashboard_format(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Convert processing result to dashboard-compatible format"""
        dashboard_data = {
            'input_character': result.get('input_character', '?'),
            'output_character': result.get('output_character', '?'),
            'accuracy': result.get('precision', 0.0),
            'processing_time_ms': result.get('processing_time_ms', 0.0),
            'energy_level': result.get('energy_level', 1.0),
            'stress_level': result.get('adrenaline_level', 0.0) * 0.5,  # Scale adrenaline to stress
            'adrenaline_level': result.get('adrenaline_level', 0.0)
        }
        
        # Add neuromodulator data if available
        if 'neuromodulators' in result:
            dashboard_data.update(result['neuromodulators'])
        
        # Add brain activity data if available
        if 'brain_activity' in result:
            brain_activity = result['brain_activity']
            if 'thalamus' in brain_activity:
                dashboard_data['thalamic_activity'] = brain_activity['thalamus']
            if 'occipital' in brain_activity:
                occipital_data = brain_activity['occipital']
                if 'v1_features' in occipital_data:
                    dashboard_data['l4_output'] = occipital_data['v1_features'].get('output_activity', 0.0)
            if 'frontal' in brain_activity:
                frontal_data = brain_activity['frontal']
                dashboard_data['l5_output'] = frontal_data.get('final_output', 0.0)
        
        return dashboard_data
    
    def start_dashboard(self):
        """Start the dashboard with data collection"""
        self.is_running = True
        self.data_collector.start_collection()
        
        # Start dashboard in a separate thread to allow for input processing
        dashboard_thread = threading.Thread(target=self._dashboard_loop, daemon=True)
        dashboard_thread.start()
    
    def stop_dashboard(self):
        """Stop the dashboard and data collection"""
        self.is_running = False
        self.data_collector.stop_collection()
        self.dashboard.stop()
    
    def _dashboard_loop(self):
        """Main dashboard loop"""
        try:
            # Start the dashboard
            self.dashboard.run()
        except KeyboardInterrupt:
            self.stop_dashboard()
    
    def run_interactive_mode(self):
        """Run in interactive mode with character processing"""
        self.start_dashboard()
        
        print("\n[bold green]Interactive Mode Started[/bold green]")
        print("Type characters to process them through the neural pipeline")
        print("Dashboard will show real-time brain activity and processing results")
        print("Press Ctrl+C to exit\n")
        
        try:
            while self.is_running:
                # The dashboard handles input in its own thread
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("\n[bold yellow]Stopping interactive mode...[/bold yellow]")
            self.stop_dashboard()


def create_dashboard_controller() -> DashboardController:
    """Create a configured dashboard controller"""
    config = IntegrationConfig(
        update_interval=0.1,
        dashboard_refresh_rate=0.1,
        data_collection_interval=0.05,
        max_history_points=100
    )
    
    return DashboardController(config)


# Convenience function for easy integration
def integrate_dashboard_with_controller(main_controller) -> DashboardController:
    """
    Integrate dashboard with existing aNA controller
    
    Args:
        main_controller: The main aNA controller instance
        
    Returns:
        Configured dashboard controller
    """
    dashboard_controller = create_dashboard_controller()
    dashboard_controller.connect_brain_system(main_controller)
    
    return dashboard_controller


if __name__ == "__main__":
    # Demo integration
    print("Neural Dashboard Integration Demo")
    print("This module provides integration between aNA v5.0 and the neural dashboard")
    print("Use integrate_dashboard_with_controller() to connect to your main controller")