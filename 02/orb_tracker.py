"""ORB-based object tracking demo.

This script follows the high-level idea described in the
"Detecting and tracking objects with ORB using OpenCV" article,
adapted to work with the local orb-sample.mp4 video.

Workflow (interactive):
1. The first frame of the video is shown.
2. You draw a bounding box around the target object.
3. ORB keypoints/descriptors from that region become the reference.
4. For each new frame, ORB features are matched against the reference
   and the matched points are visualised along with an approximate box.
"""

from __future__ import annotations

import cv2
import numpy as np

from utils import (
	FpsCounter,
	create_matcher,
	create_orb_detector,
	create_video_capture,
	draw_fps,
)


def select_roi(frame):
	"""Let the user select a rectangular ROI on the given frame.

	Returns (x, y, w, h) in pixel coordinates. If the user cancels,
	returns None.
	"""

	roi = cv2.selectROI("Select object", frame, fromCenter=False, showCrosshair=True)
	cv2.destroyWindow("Select object")
	if roi == (0, 0, 0, 0):
		return None
	return roi


def compute_reference_features(frame_bgr, roi, orb):
	"""Extract ORB keypoints/descriptors from the selected ROI.

	The ROI is specified as (x, y, w, h) in the original frame.
	"""

	x, y, w, h = roi
	x2, y2 = x + w, y + h

	roi_bgr = frame_bgr[y:y2, x:x2]
	roi_gray = cv2.cvtColor(roi_bgr, cv2.COLOR_BGR2GRAY)

	keypoints, descriptors = orb.detectAndCompute(roi_gray, None)

	# Shift keypoints back into full-frame coordinates so that matches
	# directly give us positions in the current frame.
	shifted_keypoints = []
	for kp in keypoints:
		kp_shifted = cv2.KeyPoint(kp.pt[0] + x, kp.pt[1] + y, kp.size, kp.angle, kp.response, kp.octave, kp.class_id)
		shifted_keypoints.append(kp_shifted)

	return shifted_keypoints, descriptors


def draw_matches_as_points(frame_bgr, keypoints_ref, keypoints_cur, matches):
	"""Draw matched keypoints on the current frame and an approximate box."""

	if not matches:
		return

	pts = []
	for m in matches:
		pt = keypoints_cur[m.trainIdx].pt
		pts.append(pt)
		cv2.circle(frame_bgr, (int(pt[0]), int(pt[1])), 3, (0, 0, 255), -1)

	# Draw a rough bounding box around the matched points to indicate the object.
	pts_np = np.array(pts, dtype=np.float32)
	x_min, y_min = np.min(pts_np, axis=0)
	x_max, y_max = np.max(pts_np, axis=0)
	cv2.rectangle(
		frame_bgr,
		(int(x_min), int(y_min)),
		(int(x_max), int(y_max)),
		(255, 0, 0),
		2,
	)


def resize_frame(frame, max_width: int = 960, max_height: int = 540):

	"""Resize a frame so it fits comfortably on screen, keeping aspect ratio.

	If the frame is already smaller than the limits, it is returned unchanged.
	The tracking is then performed on this resized version.
	"""

	h, w = frame.shape[:2]
	scale = min(max_width / w, max_height / h, 1.0)
	if scale >= 1.0:
		return frame
	new_size = (int(w * scale), int(h * scale))
	return cv2.resize(frame, new_size, interpolation=cv2.INTER_AREA)


def main():
	video = create_video_capture("orb-sample.mp4")

	ok, first_frame = video.read()
	if not ok:
		print("Could not read first frame from orb-sample.mp4")
		video.release()
		return

	# Work with a resized version of the frames so the window fits on screen
	# and interaction with the ROI selector is more convenient.
	first_frame = resize_frame(first_frame)

	print("Select ROI on the first frame, then press ENTER or SPACE to confirm.")
	print("Press 'c' in the ROI window to cancel selection.")

	roi = select_roi(first_frame.copy())
	if roi is None:
		print("ROI selection cancelled; exiting.")
		video.release()
		return

	orb = create_orb_detector()
	matcher = create_matcher()

	keypoints_ref, descriptors_ref = compute_reference_features(first_frame, roi, orb)
	if descriptors_ref is None or len(keypoints_ref) == 0:
		print("No ORB features found in the selected region.")
		video.release()
		return

	# Restart the video from the beginning for the actual tracking loop.
	video.release()
	video = create_video_capture("orb-sample.mp4")

	fps_counter = FpsCounter()
	frame_index = 0

	while True:
		ok, frame = video.read()
		if not ok:
			break

		frame = resize_frame(frame)
		frame_index += 1
		# Print occasionally so you can confirm in the terminal
		# that frames are being processed.
		if frame_index % 30 == 0:
			print(f"Processed {frame_index} frames...")

		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		keypoints_cur, descriptors_cur = orb.detectAndCompute(gray, None)

		if descriptors_cur is not None and len(keypoints_cur) > 0:
			matches = matcher.match(descriptors_ref, descriptors_cur)
			# Sort matches by distance so that we focus on the best ones.
			matches = sorted(matches, key=lambda m: m.distance)
			# Keep only a subset for visual clarity.
			matches = matches[:200]
			draw_matches_as_points(frame, keypoints_ref, keypoints_cur, matches)

		fps = fps_counter.update()
		draw_fps(frame, fps)

		cv2.imshow("ORB object tracking", frame)
		key = cv2.waitKey(1) & 0xFF
		if key == 27:  # ESC
			break

	video.release()
	cv2.destroyAllWindows()


if __name__ == "__main__":
	main()
