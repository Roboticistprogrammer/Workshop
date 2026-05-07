#!/usr/bin/env python3

import cv2
import threading
import time
from collections import deque
from gui_utils import GUIUtils

class CapMultiThreading:
    """Multi-threaded video capture with frame buffering"""

    def __init__(self, video_path, max_frames, buffer_size=60):
        self.cap = cv2.VideoCapture(video_path)
        self.max_frames = max_frames
        self.buffer = deque(maxlen=buffer_size)
        self.running = True
        self.lock = threading.Lock()
        self.frames_captured = 0
        self.frames_displayed = 0

    def capture_frames(self):
        """Thread function to continuously capture frames"""
        while self.running and self.frames_captured < self.max_frames:
            ret, frame = self.cap.read()
            if not ret:
                break

            with self.lock:
                self.buffer.append(frame)
                self.frames_captured += 1

        # Signal that capture is finished
        self.running = False
    
    def get_frame(self):
        """Get the next frame from buffer"""
        with self.lock:
            if self.buffer:
                frame = self.buffer.popleft()
                self.frames_displayed += 1
                return frame
        
        # Sleep to avoid busy-waiting
        time.sleep(0.001)
        return None
    
    def get_buffer_occupancy(self):
        """Get current buffer size"""
        with self.lock:
            return len(self.buffer)
    
    def get_buffer_maxlen(self):
        """Get max buffer size"""
        return self.buffer.maxlen
    
    def start(self):
        """Start the capture thread"""
        capture_thread = threading.Thread(target=self.capture_frames, daemon=True)
        capture_thread.start()
    
    def stop(self):
        """Stop the capture thread"""
        self.running = False
        self.cap.release()

# Main execution
if __name__ == "__main__":
    # Get video properties (fallback to 30 FPS if unknown)
    cap_temp = cv2.VideoCapture('../data/sample.mp4')
    fps = cap_temp.get(cv2.CAP_PROP_FPS)
    if fps <= 0:
        fps = 30.0
    max_frames = int(fps * 5)  # Only first 5 seconds
    cap_temp.release()

    multi_cap = CapMultiThreading('../data/sample.mp4', max_frames, buffer_size=60)
    multi_cap.start()

    gu = GUIUtils()

    while True:
        frame = multi_cap.get_frame()
        if frame is None:
            # If capture is finished and buffer is empty, exit
            if not multi_cap.running and multi_cap.get_buffer_occupancy() == 0:
                break
            continue

        # Heavy processing: Gaussian blur + Canny edge detection
        frame_blurred = cv2.GaussianBlur(frame, (21, 21), 0)
        edges = cv2.Canny(frame_blurred, 50, 150)
        frame = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

        # Add FPS info and label
        frame = gu.show_fps(frame)
        cv2.putText(frame, "Multi-threaded", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow('Multi-threaded - With Buffering', frame)
        if cv2.waitKey(1) == 27:  # Exit when 'ESC' key is pressed
            break

    multi_cap.stop()
    cv2.destroyAllWindows()
    print(f"Average FPS: {gu.get_average_fps():.2f}")