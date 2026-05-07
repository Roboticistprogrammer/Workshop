#!/usr/bin/env python3

import cv2
import time

class GUIUtils:
    """Utility class for GUI operations and FPS calculation"""
    
    def __init__(self):
        self.fps_start_time = time.time()
        self.fps_counter = 0
        self.current_fps = 0
        self.fps_list = []
        self.frame_times = []  # Track individual frame times for jitter analysis
        self.last_frame_time = time.time()
    
    def show_fps(self, frame):
        """Add FPS display to the frame"""
        current_time = time.time()
        frame_delta = current_time - self.last_frame_time
        self.last_frame_time = current_time
        self.frame_times.append(frame_delta)
        
        self.fps_counter += 1
        elapsed = current_time - self.fps_start_time
        
        # Update FPS every 30 frames
        if self.fps_counter % 30 == 0:
            self.current_fps = 30 / elapsed
            self.fps_list.append(self.current_fps)
            self.fps_start_time = current_time
        
        # Display FPS on frame
        cv2.putText(
            frame,
            f"FPS: {self.current_fps:.2f}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )
        
        return frame
    
    def get_average_fps(self):
        """Calculate and return average FPS"""
        if not self.fps_list:
            return 0
        return sum(self.fps_list) / len(self.fps_list)
    
    def get_frame_jitter(self):
        """Get standard deviation of frame times (consistency metric)"""
        if not self.frame_times or len(self.frame_times) < 2:
            return 0
        
        import statistics
        return statistics.stdev(self.frame_times)