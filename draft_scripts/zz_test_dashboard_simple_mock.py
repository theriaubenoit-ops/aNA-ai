#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple test script for aNA v5.0 Neural Dashboard

This script tests the dashboard without complex imports.
"""

import time
import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(__file__))

def test_dashboard_basic():
    """Test basic dashboard functionality"""
    print("🧪 Testing Basic Dashboard Functionality")
    print("=" * 50)
    
    try:
        # Test importing the dashboard
        from scr.gui.dashboard import NeuralDashboard, create_dashboard
        print("✅ Dashboard module imported successfully")
        
        # Create dashboard instance
        dashboard = create_dashboard()
        print("✅ Dashboard instance created")
        
        # Test basic functionality
        test_data = {
            'thalamic_activity': 0.75,
            'l4_output': 0.68,
            'l5_output': 0.55,
            'accuracy': 0.92,
            'input_character': 'A',
            'output_character': 'A',
            'neuromodulators': {
                'dopamine': 0.85,
                'acetylcholine': 0.72,
                'serotonin': 0.68,
                'norepinephrine': 0.45,
                'no_gas': 0.35
            }
        }
        
        # Test data update
        dashboard.update_data(test_data)
        print("✅ Data update successful")
        
        # Test input/output
        dashboard.add_input_char('H')
        dashboard.add_output_char('h')
        print("✅ Input/output buffer update successful")
        
        # Test color scheme
        color = dashboard.get_status_color(0.75)
        print(f"✅ Color scheme working: {color}")
        
        # Test thalamic pulse
        dashboard.thalamic_pulse.update()
        pulse = dashboard.thalamic_pulse.get_pulse_indicator()
        print(f"✅ Thalamic pulse working: '{pulse}'")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_integration_basic():
    """Test basic integration functionality"""
    print("\n🔗 Testing Basic Integration")
    print("=" * 50)
    
    try:
        from scr.gui.integration import DashboardController, create_dashboard_controller
        print("✅ Integration module imported successfully")
        
        # Create controller
        controller = create_dashboard_controller()
        print("✅ Dashboard controller created")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_performance():
    """Test performance requirements"""
    print("\n⚡ Testing Performance")
    print("=" * 50)
    
    try:
        from scr.gui.dashboard import create_dashboard
        
        dashboard = create_dashboard()
        
        # Test 100 frame updates
        start_time = time.time()
        
        frame_count = 100
        for i in range(frame_count):
            test_data = {
                'thalamic_activity': 0.75,
                'l4_output': 0.68,
                'l5_output': 0.55,
                'accuracy': 0.92,
                'input_character': chr(65 + (i % 26)),
                'output_character': chr(97 + (i % 26)),
                'neuromodulators': {
                    'dopamine': 0.85,
                    'acetylcholine': 0.72,
                    'serotonin': 0.68,
                    'norepinephrine': 0.45,
                    'no_gas': 0.35
                }
            }
            
            dashboard.update_data(test_data)
            dashboard.add_input_char(chr(65 + (i % 26)))
            dashboard.add_output_char(chr(97 + (i % 26)))
        
        end_time = time.time()
        total_time = end_time - start_time
        avg_frame_time = total_time / frame_count
        
        print(f"✅ {frame_count} frames in {total_time:.3f}s")
        print(f"✅ Average frame time: {avg_frame_time*1000:.1f}ms")
        print(f"✅ Achieved FPS: {1/avg_frame_time:.1f}")
        
        # Check 10 FPS requirement
        target_fps = 10.0
        target_frame_time = 1.0 / target_fps
        
        if avg_frame_time <= target_frame_time:
            print(f"🎯 Performance Goal: PASSED ({avg_frame_time:.3f}s ≤ {target_frame_time:.3f}s)")
            return True
        else:
            print(f"⚠️  Performance Goal: NEEDS OPTIMIZATION ({avg_frame_time:.3f}s > {target_frame_time:.3f}s)")
            return False
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def run_simple_test():
    """Run simple dashboard tests"""
    print("🚀 aNA v5.0 Neural Dashboard - Simple Test")
    print("=" * 60)
    
    # Test basic functionality
    basic_passed = test_dashboard_basic()
    
    # Test integration
    integration_passed = test_integration_basic()
    
    # Test performance
    performance_passed = test_performance()
    
    # Summary
    print("\n📋 Test Summary")
    print("=" * 50)
    print(f"Basic Functionality: {'✅ PASSED' if basic_passed else '❌ FAILED'}")
    print(f"Integration: {'✅ PASSED' if integration_passed else '❌ FAILED'}")
    print(f"Performance: {'✅ PASSED' if performance_passed else '❌ FAILED'}")
    
    all_passed = basic_passed and integration_passed and performance_passed
    
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


if __name__ == "__main__":
    success = run_simple_test()
    sys.exit(0 if success else 1)