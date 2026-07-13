"""
Eye Tracker Module - KozbenSal
Detects and tracks eye movements using computer vision.
Port from EyeWriter C++ to Python.
"""

import cv2
import numpy as np
import mediapipe as mp
from typing import Optional, Tuple, List


class EyeTracker:
    """
    Main eye tracking class.
    Detects eye position, pupil, and calculates gaze direction.
    """

    def __init__(self, camera_id: int = 1):
        """
        Initialize eye tracker.

        Args:
            camera_id: Camera device ID (default 0 for built-in webcam)
        """
        self.camera_id = camera_id
        self.cap: Optional[cv2.VideoCapture] = None

        # MediaPipe Face Mesh for eye tracking
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

        # Tracking state
        self.eye_found = False
        self.pupil_found = False
        self.current_frame: Optional[np.ndarray] = None
        self.gray_frame: Optional[np.ndarray] = None

        # Eye landmarks indices (MediaPipe Face Mesh)
        # Left eye: 468-473 (iris), Right eye: 473-478 (iris)
        self.LEFT_IRIS = [468, 469, 470, 471, 472]
        self.RIGHT_IRIS = [473, 474, 475, 476, 477]

        # Eye contours
        self.LEFT_EYE = [33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161, 246]
        self.RIGHT_EYE = [362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385, 384, 398]

        # Current eye position
        self.left_eye_center: Optional[Tuple[float, float]] = None
        self.right_eye_center: Optional[Tuple[float, float]] = None
        self.gaze_point: Optional[Tuple[float, float]] = None

        # Pupil detection via CV
        self.left_pupil: Optional[Tuple[int, int]] = None
        self.right_pupil: Optional[Tuple[int, int]] = None

        # Smoothing
        self.smooth_factor = 0.7
        self.smoothed_gaze: Optional[np.ndarray] = None

        # Blink detection
        self.blink_threshold = 0.21  # EAR threshold for blink detection
        self.blink_consecutive_frames = 2  # Frames needed to confirm blink
        self.blink_counter = 0
        self.is_blinking = False
        self.blink_detected = False
        self.prev_blink_state = False

    def start(self) -> bool:
        """Start video capture."""
        # Use DirectShow backend on Windows for better compatibility
        self.cap = cv2.VideoCapture(self.camera_id, cv2.CAP_DSHOW)
        if not self.cap.isOpened():
            print(f"Error: Could not open camera {self.camera_id}")
            return False

        # Set camera properties for better performance
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cap.set(cv2.CAP_PROP_FPS, 30)

        print(f"Camera {self.camera_id} opened successfully")
        return True

    def stop(self):
        """Stop video capture and release resources."""
        if self.cap:
            self.cap.release()
        self.face_mesh.close()

    def _calculate_eye_aspect_ratio(self, eye_landmarks: List[Tuple[int, int]]) -> float:
        """
        Calculate Eye Aspect Ratio (EAR) for blink detection.

        Args:
            eye_landmarks: List of (x, y) coordinates for eye contour points

        Returns:
            EAR value (lower = more closed eye)
        """
        if len(eye_landmarks) < 6:
            return 1.0

        # Convert to numpy array
        points = np.array(eye_landmarks)

        # Vertical distances (height of eye)
        vertical_1 = np.linalg.norm(points[1] - points[5])
        vertical_2 = np.linalg.norm(points[2] - points[4])

        # Horizontal distance (width of eye)
        horizontal = np.linalg.norm(points[0] - points[3])

        # EAR formula
        if horizontal == 0:
            return 1.0

        ear = (vertical_1 + vertical_2) / (2.0 * horizontal)
        return ear

    def _detect_pupil_in_region(self, eye_region: np.ndarray, eye_coords: List[Tuple[int, int]]) -> Optional[Tuple[int, int]]:
        """
        Detect pupil in eye region using traditional CV methods.

        Args:
            eye_region: Cropped eye image
            eye_coords: Eye contour coordinates in original frame

        Returns:
            (x, y) pupil center in original frame coordinates, or None
        """
        if eye_region is None or eye_region.size == 0:
            return None

        # Get bounding box of eye
        eye_points = np.array(eye_coords)
        x_min, y_min = eye_points.min(axis=0)
        x_max, y_max = eye_points.max(axis=0)

        # Convert to grayscale if needed
        if len(eye_region.shape) == 3:
            gray_eye = cv2.cvtColor(eye_region, cv2.COLOR_BGR2GRAY)
        else:
            gray_eye = eye_region

        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray_eye, (7, 7), 2)

        # Apply threshold to get dark regions (pupil)
        _, threshold = cv2.threshold(blurred, 50, 255, cv2.THRESH_BINARY_INV)

        # Find contours
        contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if not contours:
            return None

        # Find the largest contour (likely the pupil)
        largest_contour = max(contours, key=cv2.contourArea)

        # Get moments to find center
        M = cv2.moments(largest_contour)
        if M["m00"] == 0:
            return None

        # Calculate center in eye region coordinates
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])

        # Convert back to original frame coordinates
        pupil_x = x_min + cx
        pupil_y = y_min + cy

        return (pupil_x, pupil_y)

    def update(self) -> bool:
        """
        Update tracking by processing next frame.

        Returns:
            True if frame was successfully processed
        """
        if not self.cap:
            return False

        ret, frame = self.cap.read()
        if not ret:
            return False

        self.current_frame = frame
        self.gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Flip frame horizontally for mirror view
        self.current_frame = cv2.flip(self.current_frame, 1)

        # Convert to RGB for MediaPipe
        rgb_frame = cv2.cvtColor(self.current_frame, cv2.COLOR_BGR2RGB)

        # Process frame with MediaPipe
        results = self.face_mesh.process(rgb_frame)

        self.eye_found = False
        self.pupil_found = False

        if results.multi_face_landmarks:
            face_landmarks = results.multi_face_landmarks[0]
            h, w = self.current_frame.shape[:2]

            # Get iris landmarks
            left_iris_coords = []
            right_iris_coords = []

            for idx in self.LEFT_IRIS:
                landmark = face_landmarks.landmark[idx]
                x, y = int(landmark.x * w), int(landmark.y * h)
                left_iris_coords.append((x, y))

            for idx in self.RIGHT_IRIS:
                landmark = face_landmarks.landmark[idx]
                x, y = int(landmark.x * w), int(landmark.y * h)
                right_iris_coords.append((x, y))

            # Get eye contours for blink detection
            left_eye_coords = []
            right_eye_coords = []

            for idx in self.LEFT_EYE:
                landmark = face_landmarks.landmark[idx]
                x, y = int(landmark.x * w), int(landmark.y * h)
                left_eye_coords.append((x, y))

            for idx in self.RIGHT_EYE:
                landmark = face_landmarks.landmark[idx]
                x, y = int(landmark.x * w), int(landmark.y * h)
                right_eye_coords.append((x, y))

            # Calculate EAR for both eyes
            left_ear = self._calculate_eye_aspect_ratio(left_eye_coords[:6])
            right_ear = self._calculate_eye_aspect_ratio(right_eye_coords[:6])
            avg_ear = (left_ear + right_ear) / 2.0

            # Detect blink
            self.blink_detected = False
            if avg_ear < self.blink_threshold:
                self.blink_counter += 1
                if self.blink_counter >= self.blink_consecutive_frames:
                    self.is_blinking = True
            else:
                if self.is_blinking and self.blink_counter >= self.blink_consecutive_frames:
                    # Blink just ended - trigger event
                    if not self.prev_blink_state:
                        self.blink_detected = True
                self.is_blinking = False
                self.blink_counter = 0

            self.prev_blink_state = self.is_blinking

            # Extract eye regions for pupil detection
            if left_eye_coords:
                eye_points = np.array(left_eye_coords)
                x_min, y_min = eye_points.min(axis=0)
                x_max, y_max = eye_points.max(axis=0)

                # Add padding
                padding = 10
                x_min = max(0, x_min - padding)
                y_min = max(0, y_min - padding)
                x_max = min(w, x_max + padding)
                y_max = min(h, y_max + padding)

                left_eye_region = self.current_frame[y_min:y_max, x_min:x_max]
                self.left_pupil = self._detect_pupil_in_region(left_eye_region, left_eye_coords)

            if right_eye_coords:
                eye_points = np.array(right_eye_coords)
                x_min, y_min = eye_points.min(axis=0)
                x_max, y_max = eye_points.max(axis=0)

                # Add padding
                padding = 10
                x_min = max(0, x_min - padding)
                y_min = max(0, y_min - padding)
                x_max = min(w, x_max + padding)
                y_max = min(h, y_max + padding)

                right_eye_region = self.current_frame[y_min:y_max, x_min:x_max]
                self.right_pupil = self._detect_pupil_in_region(right_eye_region, right_eye_coords)

            # Calculate eye centers - prefer CV-detected pupils over MediaPipe iris
            if self.left_pupil is not None:
                self.left_eye_center = np.array(self.left_pupil, dtype=float)
                self.eye_found = True
                self.pupil_found = True
            elif left_iris_coords:
                self.left_eye_center = np.mean(left_iris_coords, axis=0)
                self.eye_found = True
                self.pupil_found = True

            if self.right_pupil is not None:
                self.right_eye_center = np.array(self.right_pupil, dtype=float)
                self.eye_found = True
                self.pupil_found = True
            elif right_iris_coords:
                self.right_eye_center = np.mean(right_iris_coords, axis=0)
                self.eye_found = True
                self.pupil_found = True

            # Calculate average gaze point (between both eyes)
            if self.left_eye_center is not None and self.right_eye_center is not None:
                gaze = (self.left_eye_center + self.right_eye_center) / 2

                # Apply smoothing
                if self.smoothed_gaze is None:
                    self.smoothed_gaze = gaze
                else:
                    self.smoothed_gaze = (self.smooth_factor * self.smoothed_gaze +
                                         (1 - self.smooth_factor) * gaze)

                self.gaze_point = tuple(self.smoothed_gaze.astype(int))

        return True

    def get_gaze_point(self) -> Optional[Tuple[int, int]]:
        """
        Get current smoothed gaze point in camera coordinates.

        Returns:
            (x, y) tuple or None if no eyes detected
        """
        return self.gaze_point

    def is_blink_detected(self) -> bool:
        """
        Check if a blink was detected in the last frame.

        Returns:
            True if blink event occurred
        """
        return self.blink_detected

    def get_eye_centers(self) -> Tuple[Optional[Tuple[float, float]], Optional[Tuple[float, float]]]:
        """
        Get raw eye center positions.

        Returns:
            Tuple of (left_eye_center, right_eye_center)
        """
        return self.left_eye_center, self.right_eye_center

    def draw_debug(self, frame: np.ndarray) -> np.ndarray:
        """
        Draw debug visualization on frame.

        Args:
            frame: Input frame

        Returns:
            Frame with debug overlay
        """
        debug_frame = frame.copy()

        # Draw eye centers (MediaPipe iris)
        if self.left_eye_center is not None:
            cv2.circle(debug_frame, tuple(self.left_eye_center.astype(int)), 3, (0, 255, 0), -1)
            cv2.putText(debug_frame, "L", tuple(self.left_eye_center.astype(int)),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

        if self.right_eye_center is not None:
            cv2.circle(debug_frame, tuple(self.right_eye_center.astype(int)), 3, (0, 255, 0), -1)
            cv2.putText(debug_frame, "R", tuple(self.right_eye_center.astype(int)),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

        # Draw CV-detected pupils (if different from eye centers)
        if self.left_pupil is not None:
            cv2.circle(debug_frame, self.left_pupil, 5, (255, 0, 255), 2)

        if self.right_pupil is not None:
            cv2.circle(debug_frame, self.right_pupil, 5, (255, 0, 255), 2)

        # Draw gaze point
        if self.gaze_point is not None:
            cv2.circle(debug_frame, self.gaze_point, 5, (0, 0, 255), 2)
            cv2.line(debug_frame, self.gaze_point,
                    (self.gaze_point[0], self.gaze_point[1] + 30), (0, 0, 255), 2)

        # Status text
        status = "Eye: " + ("YES" if self.eye_found else "NO")
        status += " | Pupil: " + ("YES" if self.pupil_found else "NO")
        status += " | Blink: " + ("YES" if self.is_blinking else "NO")
        cv2.putText(debug_frame, status, (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        # Pupil detection method
        pupil_method = "CV" if (self.left_pupil is not None or self.right_pupil is not None) else "MediaPipe"
        cv2.putText(debug_frame, f"Method: {pupil_method}", (10, 60),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

        return debug_frame

    def get_frame(self) -> Optional[np.ndarray]:
        """Get current frame."""
        return self.current_frame


if __name__ == "__main__":
    # Test eye tracker
    tracker = EyeTracker()

    if not tracker.start():
        print("Failed to start tracker")
        exit(1)

    print("Eye tracker started. Press 'q' to quit.")

    try:
        while True:
            if tracker.update():
                frame = tracker.get_frame()
                if frame is not None:
                    debug_frame = tracker.draw_debug(frame)
                    cv2.imshow("Eye Tracker Debug", debug_frame)

                    gaze = tracker.get_gaze_point()
                    if gaze:
                        print(f"Gaze: {gaze}")

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    finally:
        tracker.stop()
        cv2.destroyAllWindows()
