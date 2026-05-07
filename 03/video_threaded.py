#!/usr/bin/env python

'''
Multithreaded video processing sample.
Usage:
   video_threaded.py {<video device number>|<video file name>}

   Shows how python threading capabilities can be used
   to organize parallel captured frame processing pipeline
   for smoother playback.

Keyboard shortcuts:

   ESC - exit
   space - switch between multi and single threaded processing
'''

import os
import time

import numpy as np
import cv2 as cv

from multiprocessing.pool import ThreadPool
from collections import deque


def clock():
    """Simple wall-clock helper (seconds)."""

    return time.time()


class StatValue:
    """Running average helper for latency/frame interval stats."""

    def __init__(self):
        self.value = 0.0
        self.n = 0

    def update(self, v):
        self.n += 1
        if self.n == 1:
            self.value = float(v)
        else:
            # Incremental running average
            self.value += (float(v) - self.value) / self.n


def draw_str(img, pt, text):
    """Draw a small status string on the image."""

    cv.putText(img, text, pt, cv.FONT_HERSHEY_PLAIN, 1.0, (0, 255, 0), 1, cv.LINE_AA)


def create_capture(source):
    """Create an OpenCV VideoCapture from a camera index or file name.

    If a string that does not directly resolve to a file is given, this
    will also try to open it from the top-level `data/` folder of
    this workshop.
    """

    # Camera index
    if isinstance(source, int):
        cap = cv.VideoCapture(source)
    else:
        path = source
        if not os.path.isabs(path) and not os.path.exists(path):
            # Resolve relative to repository root data/ directory.
            repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            path = os.path.join(repo_root, "data", source)
        cap = cv.VideoCapture(path)

    if not cap.isOpened():
        raise RuntimeError(f"Could not open video source: {source}")

    return cap


class DummyTask:
    def __init__(self, data):
        self.data = data
    def ready(self):
        return True
    def get(self):
        return self.data

def main():
    import sys

    try:
        fn = sys.argv[1]
    except Exception:
        fn = "0"  # default to first camera

    # Interpret numeric arguments as camera indices, everything else as
    # a video file (resolved via create_capture).
    if isinstance(fn, str) and fn.isdigit():
        source = int(fn)
    else:
        source = fn

    try:
        cap = create_capture(source)
    except RuntimeError as e:
        print(e)
        return


    def process_frame(frame, t0):
        # some intensive computation...
        frame = cv.medianBlur(frame, 19)
        frame = cv.medianBlur(frame, 19)
        return frame, t0

    threadn = cv.getNumberOfCPUs()
    pool = ThreadPool(processes = threadn)
    pending = deque()

    threaded_mode = True

    latency = StatValue()
    frame_interval = StatValue()
    last_frame_time = clock()
    while True:
        while len(pending) > 0 and pending[0].ready():
            res, t0 = pending.popleft().get()
            latency.update(clock() - t0)
            draw_str(res, (20, 20), "threaded      :  " + str(threaded_mode))
            draw_str(res, (20, 40), "latency        :  %.1f ms" % (latency.value*1000))
            draw_str(res, (20, 60), "frame interval :  %.1f ms" % (frame_interval.value*1000))
            cv.imshow('threaded video', res)
        if len(pending) < threadn:
            _ret, frame = cap.read()
            t = clock()
            frame_interval.update(t - last_frame_time)
            last_frame_time = t
            if threaded_mode:
                task = pool.apply_async(process_frame, (frame.copy(), t))
            else:
                task = DummyTask(process_frame(frame, t))
            pending.append(task)
        ch = cv.waitKey(1)
        if ch == ord(' '):
            threaded_mode = not threaded_mode
        if ch == 27:
            break

    print('Done')


if __name__ == '__main__':
    print(__doc__)
    main()
    cv.destroyAllWindows()
