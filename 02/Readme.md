# Project 2 – ORB Feature Tracker

This project is a small, self-contained implementation of ORB-based object tracking inspired by the blog post "Detecting and tracking objects with ORB using OpenCV". It demonstrates how to detect binary keypoints on a target object and then track that object across frames in a video using feature matching.

The script orb_tracker.py:
- Opens the sample video orb-sample.mp4 from the data folder.
- Shows the first frame and lets you draw a bounding box around the object of interest.
- Extracts ORB keypoints and descriptors from the selected region to build a reference model.
- For each subsequent frame, detects ORB features, matches them to the reference, and visualises the matched points and an approximate bounding box for the tracked object while displaying the current FPS.

Run from the project root (with the virtual environment activated):

```bash
python 02/orb_tracker.py
```

Press ESC in the display window to stop the tracking.

