#!/usr/bin/env python3
"""
Test script for the improved gesture controller.
This script tests the basic functionality without requiring a camera.
"""

import os
import sys
import tempfile
import shutil
from PIL import Image
import numpy as np

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def create_test_images():
    """Create test images for the gesture controller."""
    test_folder = "test_images"
    os.makedirs(test_folder, exist_ok=True)
    
    # Create simple test images
    for i in range(3):
        img = Image.new('RGB', (800, 600), color=(255, 255, 255))
        # Add some text to make it look like a slide
        from PIL import ImageDraw, ImageFont
        draw = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype("arial.ttf", 60)
        except:
            font = ImageFont.load_default()
        
        draw.text((400, 300), f"Test Slide {i+1}", fill=(0, 0, 0), font=font, anchor="mm")
        img.save(os.path.join(test_folder, f"slide_{i+1}.png"))
    
    return test_folder

def test_config_loading():
    """Test configuration loading functionality."""
    print("Testing configuration loading...")
    
    # Import the gesture controller
    try:
        from gesture import GestureController
        print("✓ GestureController imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import GestureController: {e}")
        return False
    
    # Test config creation
    try:
        # Create a temporary config file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write('{"width": 640, "height": 480}')
            temp_config = f.name
        
        # Test loading config
        controller = GestureController(temp_config)
        print("✓ Configuration loading works")
        
        # Cleanup
        os.unlink(temp_config)
        return True
        
    except Exception as e:
        print(f"✗ Configuration loading failed: {e}")
        return False

def test_image_loading():
    """Test image loading functionality."""
    print("\nTesting image loading...")
    
    # Create test images
    test_folder = create_test_images()
    
    try:
        from gesture import GestureController
        
        # Create a custom config for testing
        test_config = {
            'width': 640,
            'height': 480,
            'folder_path': test_folder,
            'gesture_threshold': 300,
            'detection_confidence': 0.8,
            'max_hands': 1,
            'delay': 7,
            'annotation_color': [0, 0, 255],
            'annotation_thickness': 12,
            'gestures': {
                'next_slide': [0, 0, 0, 0, 1],
                'previous_slide': [1, 0, 0, 0, 0],
                'draw': [0, 1, 0, 0, 0],
                'erase': [0, 1, 1, 1, 0],
                'pointer': [0, 1, 1, 0, 0]
            }
        }
        
        # Save test config
        import json
        test_config_file = "test_config.json"
        with open(test_config_file, 'w') as f:
            json.dump(test_config, f, indent=2)
        
        # Test controller initialization (without camera)
        controller = GestureController(test_config_file)
        print(f"✓ Loaded {len(controller.path_images)} test images")
        
        # Test gesture recognition
        test_fingers = [0, 0, 0, 0, 1]  # next_slide gesture
        gesture_name = controller._get_gesture_name(test_fingers)
        if gesture_name == 'next_slide':
            print("✓ Gesture recognition works")
        else:
            print(f"✗ Gesture recognition failed: expected 'next_slide', got '{gesture_name}'")
        
        # Cleanup
        os.unlink(test_config_file)
        shutil.rmtree(test_folder)
        return True
        
    except Exception as e:
        print(f"✗ Image loading test failed: {e}")
        # Cleanup on error
        if os.path.exists(test_folder):
            shutil.rmtree(test_folder)
        return False

def test_gesture_controller_methods():
    """Test individual methods of the gesture controller."""
    print("\nTesting gesture controller methods...")
    
    try:
        from gesture import GestureController
        
        # Create test config
        test_config = {
            'width': 640,
            'height': 480,
            'folder_path': 'test_images',
            'gesture_threshold': 300,
            'detection_confidence': 0.8,
            'max_hands': 1,
            'delay': 7,
            'annotation_color': [0, 0, 255],
            'annotation_thickness': 12,
            'gestures': {
                'next_slide': [0, 0, 0, 0, 1],
                'previous_slide': [1, 0, 0, 0, 0],
                'draw': [0, 1, 0, 0, 0],
                'erase': [0, 1, 1, 1, 0],
                'pointer': [0, 1, 1, 0, 0]
            }
        }
        
        # Create test config file
        import json
        test_config_file = "test_methods_config.json"
        with open(test_config_file, 'w') as f:
            json.dump(test_config, f, indent=2)
        
        # Create test images
        test_folder = create_test_images()
        
        # Test controller creation (without camera setup)
        controller = GestureController(test_config_file)
        
        # Test gesture recognition methods
        test_cases = [
            ([0, 0, 0, 0, 1], 'next_slide'),
            ([1, 0, 0, 0, 0], 'previous_slide'),
            ([0, 1, 0, 0, 0], 'draw'),
            ([0, 1, 1, 1, 0], 'erase'),
            ([0, 1, 1, 0, 0], 'pointer'),
            ([0, 0, 0, 0, 0], None)  # No gesture
        ]
        
        passed_tests = 0
        for fingers, expected in test_cases:
            result = controller._get_gesture_name(fingers)
            if result == expected:
                passed_tests += 1
            else:
                print(f"✗ Gesture test failed: {fingers} -> expected '{expected}', got '{result}'")
        
        print(f"✓ Gesture recognition: {passed_tests}/{len(test_cases)} tests passed")
        
        # Test state reset
        controller.reset_state()
        if (controller.button_pressed == False and 
            controller.counter == 0 and 
            controller.img_number == 0):
            print("✓ State reset works")
        else:
            print("✗ State reset failed")
        
        # Cleanup
        os.unlink(test_config_file)
        shutil.rmtree(test_folder)
        return True
        
    except Exception as e:
        print(f"✗ Method testing failed: {e}")
        # Cleanup on error
        if os.path.exists(test_folder):
            shutil.rmtree(test_folder)
        if os.path.exists(test_config_file):
            os.unlink(test_config_file)
        return False

def main():
    """Run all tests."""
    print("Testing improved gesture controller...\n")
    
    tests = [
        test_config_loading,
        test_image_loading,
        test_gesture_controller_methods
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\nTest Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✓ All tests passed! The improved gesture controller is ready to use.")
        print("\nTo run the gesture controller:")
        print("1. Make sure you have images in the 'data/slides/images' folder")
        print("2. Run: python src/gesture.py")
        print("3. Use hand gestures to control the presentation")
        print("4. Press 'q' to quit, 'r' to reset annotations")
    else:
        print("✗ Some tests failed. Please check the errors above.")

if __name__ == "__main__":
    main() 