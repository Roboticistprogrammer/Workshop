#!/usr/bin/env python3

import cv2
from gui_utils import GUIUtils

# Create a capture object to load the video
cap = cv2.VideoCapture('../data/sample.mp4')

# Get video properties (fallback to 30 FPS if unknown)
fps = cap.get(cv2.CAP_PROP_FPS)
if fps <= 0:
    fps = 30.0
frames_to_process = int(fps * 5)  # Only first 5 seconds

# Initialize FPS calculation
gu = GUIUtils()
frame_count = 0

while frame_count < frames_to_process:
    ret, frame = cap.read()  # Capture frame
    if not ret:
        break  # End video when no frames are left

    # Heavy processing: Gaussian blur + Canny edge detection
    frame_blurred = cv2.GaussianBlur(frame, (21, 21), 0)
    edges = cv2.Canny(frame_blurred, 50, 150)
    frame = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

    # Add FPS info and label
    frame = gu.show_fps(frame)
    cv2.putText(frame, "Single-threaded", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow('No Threading - Single-threaded', frame)
    if cv2.waitKey(1) == 27:  # Exit when 'ESC' key is pressed
        break

    frame_count += 1

cap.release()
cv2.destroyAllWindows()
print(f"Average FPS: {gu.get_average_fps():.2f}")