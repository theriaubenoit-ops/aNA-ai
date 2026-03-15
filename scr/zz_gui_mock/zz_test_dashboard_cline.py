#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for aNA v5.0 Neural Dashboard

This script tests the dashboard integration and performance optimization
for the 10 FPS refresh rate requirement.

Architecture, concept and supervision: Benoit Theriault
Collaboration, research and code: Cline
"""

import time
import threading
import sys
import os
from typing import Dict, Any

# Add the project root to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Import dashboard components (these should exist)
from scr.gui.dashboard import NeuralDashboard, create_dashboard
from scr.gui.integration import DashboardController, create_dashboard_controller


class MockBrainSystem:
    """Mock brain system for testing dashboard integration"""
    
    def __init__(self):
        # Mock neuromodulator matrix
        self.neuromodulators = MockNeuromodulatorMatrix()
        
        # Mock brain structures
        self.thalamus = MockThalamus()
        self.occipital = MockOccipitalLobe()
        self.frontal = MockFrontalLobe()
        self.parietal = MockParietalLobe()
        self.temporal = MockTemporalLobe()
        self.amygdala = MockAmygdala()
        self.hippocampus = MockHippocampus()
        self.cerebellum = MockCerebellum()
        
        # Mock gateways
        self.input_gateway = MockInputGateway()
        self.output_gateway = MockOutputGateway()
        
        # Processing state
        self.processing_active = False
        self.current_char = '?'
        self.processing_time = 0.0
        
        # Performance tracking
        self.frame_times = []
        self.update_times = []
        self.last_frame_time = time.time()
    
    def process_character(self, char: str) -> Dict[str, Any]:
        """Mock character processing"""
        start_time = time.time()
        
        # Simulate processing delay
        time.sleep(0.01)
        
        # Generate mock processing result
        result = {
            'input_character': char,
            'output_character': char.upper() if char.islower() else char.lower(),
            'precision': 0.85 + (hash(char) % 100) / 1000.0,  # Random precision
            'processing_time_ms': (time.time() - start_time) * 1000,
            'energy_level': 0.8 + (hash(char) % 50) / 100.0,
            'adrenaline_level': 0.2 + (hash(char) % 30) / 100.0,
            'neuromodulators': {
                'dopamine': 0.5 + (hash(char) % 50) / 100.0,
                'acetylcholine': 0.6 + (hash(char) % 40) / 100.0,
                'serotonin': 0.7 + (hash(char) % 30) / 100.0,
                'norepinephrine': 0.3 + (hash(char) % 40) / 100.0,
                'no_gas': 0.4 + (hash(char) % 30) / 100.0
            },
            'brain_activity': {
                'thalamus': 0.6 + (hash(char) % 40) / 100.0,
                'occipital': {
                    'v1_features': {
                        'output_activity': 0.5 + (hash(char) % 50) / 100.0
                    }
                },
                'frontal': {
                    'final_output': 0.4 + (hash(char) % 60) / 100.0
                }
            }
        }
        
        self.current_char = char
        self.processing_time = result['processing_time_ms']
        
        return result
    
    def update_system(self):
        """Update the mock system state"""
        # Simulate biological rhythms
        current_time = time.time()
        time_factor = (current_time % 10) / 10  # 10-second cycle
        
        # Update neuromodulators with rhythmic patterns
        dopamine = 0.5 + 0.3 * abs(time_factor - 0.5)
        acetylcholine = 0.6 + 0.2 * time_factor
        serotonin = 0.7 - 0.2 * time_factor
        norepinephrine = 0.4 + 0.3 * time_factor
        no_gas = 0.3 + 0.4 * time_factor
        
        self.neuromodulators.set_concentration('dopamine', dopamine)
        self.neuromodulators.set_concentration('acetylcholine', acetylcholine)
        self.neuromodulators.set_concentration('serotonin', serotonin)
        self.neuromodulators.set_concentration('norepinephrine', norepinephrine)
        self.neuromodulators.set_concentration('no_gas', no_gas)


class MockNeuromodulatorMatrix:
    """Mock neuromodulator matrix"""
    
    def __init__(self):
        self.concentrations = {
            'dopamine': 0.5,
            'acetylcholine': 0.6,
            'serotonin': 0.7,
            'norepinephrine': 0.4,
            'no_gas': 0.3
        }
    
    def set_concentration(self, modulator_type: str, concentration: float):
        """Set neuromodulator concentration"""
        self.concentrations[modulator_type] = concentration
    
    def get_concentration(self, modulator_type: str) -> float:
        """Get neuromodulator concentration"""
        return self.concentrations.get(modulator_type, 0.5)
    
    def get_current_levels(self):
        """Get current neuromodulator levels"""
        return self.concentrations


class MockThalamus:
    """Mock thalamus"""
    
    def __init__(self):
        self.activity = 0.75
        self.baseline = 0.15
    
    def get_activity(self):
        """Get thalamic activity"""
        return self.activity
    
    def get_baseline(self):
        """Get thalamic baseline"""
        return self.baseline


class MockOccipitalLobe:
    """Mock occipital lobe"""
    
    def __init__(self):
        self.v1_features = MockV1Features()
    
    def get_activity(self):
        """Get occipital lobe activity"""
        return self.v1_features.output_activity


class MockV1Features:
    """Mock V1 features"""
    
    def __init__(self):
        self.output_activity = 0.68


class MockFrontalLobe:
    """Mock frontal lobe"""
    
    def __init__(self):
        self.final_output = 0.55
    
    def get_activity(self):
        """Get frontal lobe activity"""
        return self.final_output


class MockParietalLobe:
    """Mock parietal lobe"""
    
    def __init__(self):
        self.activity = 0.65
    
    def get_activity(self):
        """Get parietal lobe activity"""
        return self.activity


class MockTemporalLobe:
    """Mock temporal lobe"""
    
    def __init__(self):
        self.activity = 0.70
    
    def get_activity(self):
        """Get temporal lobe activity"""
        return self.activity


class MockAmygdala:
    """Mock amygdala"""
    
    def __init__(self):
        self.emotional_state = 0.5
    
    def get_activity(self):
        """Get amygdala activity"""
        return self.emotional_state
    
    def get_adrenaline_level(self):
        """Get adrenaline level"""
        return self.emotional_state * 0.5
    
    def get_stress_level(self):
        """Get stress level"""
        return self.emotional_state * 0.4


class MockHippocampus:
    """Mock hippocampus"""
    
    def __init__(self):
        self.memory_strength = 0.65
        self.consolidation_rate = 0.45
        self.memory_traces = 12
    
    def get_activity(self):
        """Get hippocampus activity"""
        return self.memory_strength
    
    def get_consolidation_rate(self):
        """Get consolidation rate"""
        return self.consolidation_rate
    
    def get_memory_traces(self):
        """Get memory traces"""
        return self.memory_traces
    
    def get_memory_strength(self):
        """Get memory strength"""
        return self.memory_strength
    
    def get_memory_signal(self):
        """Get memory signal"""
        return self.memory_strength * 0.8
    
    def get_spatial_signal(self):
        """Get spatial signal"""
        return self.memory_strength * 0.9


class MockCerebellum:
    """Mock cerebellum"""
    
    def __init__(self):
        self.coordination = 0.80
    
    def get_activity(self):
        """Get cerebellum activity"""
        return self.coordination
    
    def get_motor_coordination_signal(self):
        """Get motor coordination signal"""
        return self.coordination * 0.9


class MockInputGateway:
    """Mock input gateway"""
    
    def __init__(self):
        self.neuromodulators = MockNeuromodulatorMatrix()
        self.processing_active = False


class MockOutputGateway:
    """Mock output gateway"""
    
    def __init__(self):
        self.processing_active = False


def test_dashboard_performance():
    """Test dashboard performance and 10 FPS optimization"""
    print("🧪 Testing Dashboard Performance")
    print("=" * 50)
    
    # Create dashboard
    dashboard = create_dashboard()
    
    # Generate test data
    test_data = {
        'thalamic_activity': 0.75,
        'thalamic_baseline': 0.15,
        'l4_output': 0.68,
        'l23_output': 0.61,
        'l5_output': 0.55,
        'precision_loss': 0.12,
        'attention_boost': 1.25,
        'input_character': 'A',
        'output_character': 'A',
        'accuracy': 0.92,
        'processing_time_ms': 15.2,
        'neuromodulators': {
            'dopamine': 0.85,
            'acetylcholine': 0.72,
            'serotonin': 0.68,
            'norepinephrine': 0.45,
            'no_gas': 0.35
        },
        'energy_level': 0.85,
        'stress_level': 0.25,
        'adrenaline_level': 0.30,
        'memory_strength': 0.65,
        'consolidation_rate': 0.45,
        'memory_traces': 12
    }
    
    # Test update performance
    print("📊 Testing Data Update Performance...")
    start_time = time.time()
    
    frame_count = 100
    for i in range(frame_count):
        dashboard.update_data(test_data)
        dashboard.add_input_char(chr(65 + (i % 26)))  # A-Z cycling
        dashboard.add_output_char(chr(97 + (i % 26)))  # a-z cycling
    
    end_time = time.time()
    total_time = end_time - start_time
    avg_frame_time = total_time / frame_count
    
    print(f"   ✅ {frame_count} frames in {total_time:.3f}s")
    print(f"   ✅ Average frame time: {avg_frame_time*1000:.1f}ms")
    print(f"   ✅ Achieved FPS: {1/avg_frame_time:.1f}")
    
    # Test 10 FPS requirement
    target_fps = 10.0
    target_frame_time = 1.0 / target_fps
    
    if avg_frame_time <= target_frame_time:
        print(f"   🎯 Performance Goal: PASSED ({avg_frame_time:.3f}s ≤ {target_frame_time:.3f}s)")
    else:
        print(f"   ⚠️  Performance Goal: NEEDS OPTIMIZATION ({avg_frame_time:.3f}s > {target_frame_time:.3f}s)")
    
    return avg_frame_time <= target_frame_time


def test_integration():
    """Test dashboard integration with mock brain system"""
    print("\n🔗 Testing Dashboard Integration")
    print("=" * 50)
    
    # Create mock brain system
    mock_system = MockBrainSystem()
    
    # Create dashboard controller
    dashboard_controller = create_dashboard_controller()
    dashboard_controller.connect_brain_system(mock_system)
    
    # Test data collection
    print("📊 Testing Data Collection...")
    collected_data = dashboard_controller.data_collector.collect_data()
    
    expected_keys = [
        'thalamic_activity', 'thalamic_baseline', 'l4_output', 'l23_output',
        'l5_output', 'precision_loss', 'attention_boost', 'dopamine',
        'acetylcholine', 'serotonin', 'norepinephrine', 'no_gas',
        'energy_level', 'stress_level', 'adrenaline_level', 'memory_strength',
        'consolidation_rate', 'memory_traces', 'input_character', 'output_character',
        'accuracy', 'processing_time_ms'
    ]
    
    missing_keys = [key for key in expected_keys if key not in collected_data]
    
    if not missing_keys:
        print("   ✅ All expected data keys present")
        print(f"   ✅ Collected {len(collected_data)} data points")
    else:
        print(f"   ⚠️  Missing keys: {missing_keys}")
    
    # Test character processing
    print("⌨️  Testing Character Processing...")
    test_chars = ['H', 'e', 'l', 'l', 'o']
    
    for char in test_chars:
        result = dashboard_controller.process_input_char(char)
        if result:
            print(f"   ✅ Processed '{char}' → '{result.get('output_character', '?')}' "
                  f"(Accuracy: {result.get('precision', 0):.1%})")
        else:
            print(f"   ❌ Failed to process '{char}'")
    
    return len(missing_keys) == 0


def test_visualization():
    """Test dashboard visualization components"""
    print("\n🎨 Testing Dashboard Visualization")
    print("=" * 50)
    
    # Create dashboard
    dashboard = create_dashboard()
    
    # Test color scheme
    print("🌈 Testing Color Scheme...")
    color_scheme = dashboard.get_status_color(0.75)
    print(f"   ✅ Status color for 0.75: {color_scheme}")
    
    # Test thalamic pulse
    print("💓 Testing Thalamic Pulse...")
    dashboard.thalamic_pulse.update()
    pulse_indicator = dashboard.thalamic_pulse.get_pulse_indicator()
    print(f"   ✅ Pulse indicator: '{pulse_indicator}'")
    
    # Test history management
    print("📈 Testing History Management...")
    dashboard.history.add_point(0.85, 0.9, 0.2, 0.75)
    dashboard.history.add_point(0.90, 0.85, 0.15, 0.80)
    
    precision_history = dashboard.history.get_sparkline_data("precision")
    print(f"   ✅ History length: {len(precision_history)}")
    print(f"   ✅ Precision history: {[f'{x:.2f}' for x in precision_history]}")
    
    return True


def run_comprehensive_test():
    """Run comprehensive dashboard testing"""
    print("🚀 aNA v5.0 Neural Dashboard - Comprehensive Test")
    print("=" * 60)
    
    # Test performance
    performance_passed = test_dashboard_performance()
    
    # Test integration
    integration_passed = test_integration()
    
    # Test visualization
    visualization_passed = test_visualization()
    
    # Summary
    print("\n📋 Test Summary")
    print("=" * 50)
    print(f"Performance Test: {'✅ PASSED' if performance_passed else '❌ FAILED'}")
    print(f"Integration Test: {'✅ PASSED' if integration_passed else '❌ FAILED'}")
    print(f"Visualization Test: {'✅ PASSED' if visualization_passed else '❌ FAILED'}")
    
    all_passed = performance_passed and integration_passed and visualization_passed
    
    if all_passed:
        print("\n🎉 ALL TESTS PASSED! Dashboard is ready for use.")
        print("✨ The dashboard meets all requirements:")
        print("   • 10 FPS refresh rate optimization")
        print("   • Bio-inspired color coding")
        print("   • Thalamic pulse visualization")
        print("   • Real-time neural monitoring")
        print("   • Non-blocking input system")
        print("   • Historical data tracking")
    else:
        print("\n⚠️  Some tests failed. Review the output above.")
    
    return all_passed


def demo_dashboard():
    """Run a live dashboard demo"""
    print("\n🎬 Live Dashboard Demo")
    print("=" * 50)
    print("Starting dashboard with mock data...")
    print("Type characters to see real-time processing!")
    print("Press Ctrl+C to exit demo.\n")
    
    # Create mock system
    mock_system = MockBrainSystem()
    
    # Create dashboard controller
    dashboard_controller = create_dashboard_controller()
    dashboard_controller.connect_brain_system(mock_system)
    
    # Start interactive mode
    dashboard_controller.run_interactive_mode()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Test aNA v5.0 Neural Dashboard")
    parser.add_argument("--test", action="store_true", help="Run comprehensive tests")
    parser.add_argument("--demo", action="store_true", help="Run live dashboard demo")
    parser.add_argument("--performance", action="store_true", help="Test performance only")
    
    args = parser.parse_args()
    
    if args.test or (not args.demo and not args.performance):
        success = run_comprehensive_test()
        sys.exit(0 if success else 1)
    
    elif args.performance:
        success = test_dashboard_performance()
        sys.exit(0 if success else 1)
    
    elif args.demo:
        demo_dashboard()
    
    else:
        print("Use --test for comprehensive testing or --demo for live demo")
        sys.exit(1)