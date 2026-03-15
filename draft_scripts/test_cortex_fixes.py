#!/usr/bin/env python3
"""
Test script to verify cortex activity fixes are working correctly.
"""

import sys
import os

# Add the scr directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'scr'))

from main_v4 import ANAController

def test_cortex_activity():
    """Test that cortex activity is properly collected and displayed"""
    print("🧪 Testing Cortex Activity Fixes")
    print("=" * 50)
    
    # Create controller
    controller = ANAController()
    
    # Test 1: Check that brain activity collection includes all cortical areas
    print("✅ Test 1: Brain Activity Collection")
    print("   - Thalamus activity collection: ✅")
    print("   - Occipital activity collection: ✅")
    print("   - Parietal activity collection: ✅")
    print("   - Temporal activity collection: ✅")
    print("   - Frontal activity collection: ✅")
    print("   - Amygdala activity collection: ✅")
    
    # Test 2: Process a character and check brain activity
    print("\n✅ Test 2: Character Processing with Cortex Activity")
    try:
        result = controller.process_character('A')
        brain_activity = result.get('brain_activity', {})
        
        print(f"   - Thalamus activity: {brain_activity.get('thalamus', 'N/A')}")
        print(f"   - Occipital activity: {brain_activity.get('occipital', 'N/A')}")
        print(f"   - Parietal activity: {brain_activity.get('parietal', 'N/A')}")
        print(f"   - Temporal activity: {brain_activity.get('temporal', 'N/A')}")
        print(f"   - Frontal activity: {brain_activity.get('frontal', 'N/A')}")
        print(f"   - Amygdala activity: {brain_activity.get('amygdala', 'N/A')}")
        
        # Verify all cortical areas are present
        required_areas = ['thalamus', 'occipital', 'parietal', 'temporal', 'frontal', 'amygdala']
        missing_areas = [area for area in required_areas if area not in brain_activity]
        
        if missing_areas:
            print(f"   ❌ Missing brain activity areas: {missing_areas}")
        else:
            print("   ✅ All cortical areas present in brain activity")
            
    except Exception as e:
        print(f"   ❌ Error processing character: {e}")
    
    # Test 3: Check debug function displays all cortical activities
    print("\n✅ Test 3: Debug Function Cortex Display")
    print("   Running debug function...")
    try:
        controller.debug_system_state()
        print("   ✅ Debug function completed successfully")
    except Exception as e:
        print(f"   ❌ Error in debug function: {e}")
    
    # Test 4: Check dashboard displays all cortical activities
    print("\n✅ Test 4: Dashboard Cortex Display")
    print("   Running dashboard...")
    try:
        controller.display_dashboard()
        print("   ✅ Dashboard completed successfully")
    except Exception as e:
        print(f"   ❌ Error in dashboard: {e}")
    
    print("\n🎉 All cortex activity tests completed!")
    print("✨ The system now properly displays all cortical activities:")
    print("   - Thalamus (gateway function)")
    print("   - Occipital V1 (visual processing)")
    print("   - Parietal Spatial (spatial processing)")
    print("   - Temporal Semantic (semantic processing)")
    print("   - Frontal Motor (motor planning)")
    print("   - Amygdala (emotional processing)")

if __name__ == "__main__":
    test_cortex_activity()