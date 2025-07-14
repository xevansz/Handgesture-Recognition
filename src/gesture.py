import cv2
import os
import numpy as np
import json
import time
from cvzone.HandTrackingModule import HandDetector
from typing import List, Tuple, Optional, Dict
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class GestureController:
    """
    Hand gesture recognition controller for presentation navigation and annotation.
    """
    
    def __init__(self, config_file: str = "config/gesture_config.json"):
        """Initialize the gesture controller with configuration."""
        self.config = self._load_config(config_file)
        
        # Camera and display parameters
        self.width = self.config.get('width', 1280)
        self.height = self.config.get('height', 720)
        self.gesture_threshold = self.config.get('gesture_threshold', 600)
        self.folder_path = self.config.get('folder_path', 'data/slides/images')
        
        # Hand detection parameters
        self.detection_confidence = self.config.get('detection_confidence', 0.8)
        self.max_hands = self.config.get('max_hands', 1)
        
        # Gesture control parameters
        self.delay = self.config.get('delay', 7)
        self.annotation_color = tuple(self.config.get('annotation_color', [0, 0, 255]))
        self.annotation_thickness = self.config.get('annotation_thickness', 12)
        
        # Initialize components
        # The following methods are defined as private methods within this class:
        # - self._setup_camera(): Initializes the camera for capturing video frames.
        # - self._setup_hand_detector(): Sets up the hand detection module.
        # - self._load_presentation_images(): Loads images used for the presentation.
        self._setup_camera()
        self._setup_hand_detector()
        self._load_presentation_images()
        
        # State variables
        self.reset_state()
        
    def _load_config(self, config_file: str) -> Dict:
        """Load configuration from JSON file."""
        try:
            if os.path.exists(config_file):
                with open(config_file, 'r') as f:
                    config = json.load(f)
                logger.info(f"Loaded configuration from {config_file}")
                return config
            else:
                logger.error(f"Configuration file not found: {config_file}")
                raise FileNotFoundError(f"Configuration file not found: {config_file}")
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            raise RuntimeError(f"Failed to load configuration: {e}")
    
    def _setup_camera(self):
        """Initialize camera with error handling."""
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            logger.error("Failed to open camera. Trying alternative camera index...")
            self.cap = cv2.VideoCapture(1)
            if not self.cap.isOpened():
                raise RuntimeError("No camera available")
        
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        logger.info("Camera initialized successfully")
    
    def _setup_hand_detector(self):
        """Initialize hand detector."""
        try:
            self.detector = HandDetector(
                detectionCon=self.detection_confidence,
                maxHands=self.max_hands
            )
            logger.info("Hand detector initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize hand detector: {e}")
            raise
    
    def _load_presentation_images(self):
        """Load and validate presentation images."""
        if not os.path.exists(self.folder_path):
            logger.error(f"Presentation folder '{self.folder_path}' not found")
            raise FileNotFoundError(f"Folder '{self.folder_path}' not found")
        
        try:
            self.path_images = sorted(
                [f for f in os.listdir(self.folder_path) 
                 if f.lower().endswith(('.png', '.jpg', '.jpeg'))],
                key=len
            )
            if not self.path_images:
                logger.error(f"No image files found in '{self.folder_path}'")
                raise FileNotFoundError("No presentation images found")
            
            logger.info(f"Loaded {len(self.path_images)} presentation images")
        except Exception as e:
            logger.error(f"Error loading presentation images: {e}")
            raise
    
    def reset_state(self):
        """Reset all state variables."""
        self.button_pressed = False
        self.counter = 0
        self.img_number = 0
        self.annotations = [[]]
        self.annotation_number = -1
        self.annotation_start = False
        self.last_gesture_time = 0
        self.gesture_cooldown = 0.5  # seconds
        
        # Small image dimensions for overlay
        self.hs, self.ws = int(120 * 1), int(213 * 1)
    
    def _get_gesture_name(self, fingers: List[int]) -> Optional[str]:
        """Identify gesture based on finger configuration."""
        gestures = self.config.get('gestures', {})
        for gesture_name, finger_pattern in gestures.items():
            if fingers == finger_pattern:
                return gesture_name
        return None
    
    def _handle_gesture(self, gesture_name: str, hand_center: Tuple[int, int]):
        """Handle recognized gestures."""
        current_time = time.time()
        
        # Prevent rapid gesture triggering
        if current_time - self.last_gesture_time < self.gesture_cooldown:
            return
        
        cy = hand_center[1]
        
        if cy <= self.gesture_threshold:  # Hand is at face level
            if gesture_name == 'next_slide':
                self._next_slide()
            elif gesture_name == 'previous_slide':
                self._previous_slide()
            elif gesture_name == 'erase':
                self._erase_last_annotation()
        
        self.last_gesture_time = current_time
    
    def _next_slide(self):
        """Navigate to next slide."""
        if self.img_number < len(self.path_images) - 1:
            self.img_number += 1
            self._reset_annotations()
            logger.info(f"Next slide: {self.img_number + 1}/{len(self.path_images)}")
    
    def _previous_slide(self):
        """Navigate to previous slide."""
        if self.img_number > 0:
            self.img_number -= 1
            self._reset_annotations()
            logger.info(f"Previous slide: {self.img_number + 1}/{len(self.path_images)}")
    
    def _reset_annotations(self):
        """Reset annotations for new slide."""
        self.annotations = [[]]
        self.annotation_number = -1
        self.annotation_start = False
    
    def _erase_last_annotation(self):
        """Erase the last annotation."""
        if self.annotations:
            self.annotations.pop(-1)
            self.annotation_number -= 1
            self.button_pressed = True
            logger.info("Erased last annotation")
    
    def _handle_drawing(self, index_finger: Tuple[int, int], fingers: List[int]):
        """Handle drawing/annotation functionality."""
        if fingers == [0, 1, 0, 0, 0]:  # Index finger only
            if not self.annotation_start:
                self.annotation_start = True
                self.annotation_number += 1
                self.annotations.append([])
            
            self.annotations[self.annotation_number].append(index_finger)
        else:
            self.annotation_start = False
    
    def _handle_pointer(self, index_finger: Tuple[int, int], fingers: List[int]):
        """Handle pointer functionality."""
        if fingers == [0, 1, 1, 0, 0]:  # Two fingers
            return index_finger
        return None
    
    def _process_frame(self, img: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Process a single frame and return processed images."""
        # Flip image horizontally for mirror effect
        img = cv2.flip(img, 1)
        
        # Load current slide
        try:
            path_full_image = os.path.join(self.folder_path, self.path_images[self.img_number])
            img_current = cv2.imread(path_full_image)
            if img_current is None:
                logger.error(f"Failed to load image: {path_full_image}")
                return img, img
        except Exception as e:
            logger.error(f"Error loading slide: {e}")
            return img, img
        
        # Find hands
        hands, img = self.detector.findHands(img)
        
        # Draw gesture threshold line
        cv2.line(img, (0, self.gesture_threshold), (self.width, self.gesture_threshold), (0, 255, 0), 10)
        
        if hands and not self.button_pressed:
            hand = hands[0]
            cx, cy = hand["center"]
            lm_list = hand["lmList"]
            fingers = self.detector.fingersUp(hand)
            
            # Map index finger position to slide coordinates
            x_val = int(np.interp(lm_list[8][0], [self.width // 2, self.width], [0, self.width]))
            y_val = int(np.interp(lm_list[8][1], [150, self.height-150], [0, self.height]))
            index_finger = (x_val, y_val)
            
            # Identify and handle gestures
            gesture_name = self._get_gesture_name(fingers)
            if gesture_name:
                self._handle_gesture(gesture_name, (cx, cy))
            
            # Handle drawing
            self._handle_drawing(index_finger, fingers)
            
            # Handle pointer
            pointer_pos = self._handle_pointer(index_finger, fingers)
            if pointer_pos:
                cv2.circle(img_current, pointer_pos, 12, self.annotation_color, cv2.FILLED)
            
            # Draw annotation points
            if fingers == [0, 1, 0, 0, 0]:
                cv2.circle(img_current, index_finger, 12, self.annotation_color, cv2.FILLED)
        else:
            self.annotation_start = False
        
        # Handle button press delay
        if self.button_pressed:
            self.counter += 1
            if self.counter > self.delay:
                self.counter = 0
                self.button_pressed = False
        
        # Draw annotations
        self._draw_annotations(img_current)
        
        # Add camera overlay
        self._add_camera_overlay(img_current, img)
        
        return img_current, img
    
    def _draw_annotations(self, img_current: np.ndarray):
        """Draw all annotations on the current slide."""
        for annotation in self.annotations:
            for j in range(len(annotation)):
                if j != 0:
                    cv2.line(img_current, annotation[j - 1], annotation[j], 
                            (0, 0, 200), self.annotation_thickness)
    
    def _add_camera_overlay(self, img_current: np.ndarray, img: np.ndarray):
        """Add camera feed as overlay on slide."""
        h, w, _ = img_current.shape
        img_small = cv2.resize(img, (self.ws, self.hs))
        img_current[0:self.hs, w - self.ws: w] = img_small
    
    def run(self):
        """Main loop for gesture recognition."""
        logger.info("Starting gesture recognition...")
        logger.info("Press 'q' to quit, 'r' to reset annotations")
        
        try:
            while True:
                success, img = self.cap.read()
                if not success:
                    logger.error("Failed to read frame from camera")
                    break
                
                # Process frame
                img_current, img = self._process_frame(img)
                
                # Display images
                cv2.imshow("Slides", img_current)
                cv2.imshow("Camera Feed", img)
                
                # Handle key presses
                key = cv2.waitKey(1)
                if key == ord('q'):
                    logger.info("Quitting...")
                    break
                elif key == ord('r'):
                    self._reset_annotations()
                    logger.info("Reset annotations")
                elif key == ord('n'):
                    self._next_slide()
                elif key == ord('p'):
                    self._previous_slide()
        
        except KeyboardInterrupt:
            logger.info("Interrupted by user")
        except Exception as e:
            logger.error(f"Error in main loop: {e}")
        finally:
            self.cleanup()
    
    def stop_presentation(self):
        """Stop the presentation and clean up all resources (camera, windows)."""
        self.cleanup()
    
    def cleanup(self):
        """Clean up resources."""
        if hasattr(self, 'cap') and self.cap is not None:
            self.cap.release()
            self.cap = None
        try:
            cv2.destroyAllWindows()
        except Exception as e:
            logger.error(f"Error closing OpenCV windows: {e}")
        logger.info("Cleanup completed")

def main():
    """Main entry point."""
    try:
        controller = GestureController()
        controller.run()
    except Exception as e:
        logger.error(f"Failed to start gesture controller: {e}")
        print(f"Error: {e}")
        print("Please check that:")
        print("1. Camera is connected and working")
        print("2. 'data/slides/images' folder exists with presentation images")
        print("3. All dependencies are installed")

if __name__ == "__main__":
    main()