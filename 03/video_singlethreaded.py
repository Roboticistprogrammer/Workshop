#!/usr/bin/env python

"""Single-threaded video processing sample.

This script mirrors the processing pipeline of video_threaded.py but runs all
work on the main thread. Use it to compare latency and frame interval
statistics with the multithreaded version.

Usage:
    python video_singlethreaded.py {<video device number>|<video file name>}

Keyboard shortcuts:
    ESC  - exit
"""

import sys

import cv2 as cv

from video_threaded import clock, StatValue, draw_str, create_capture


def process_frame(frame, t0):
    """Heavy per-frame processing (same as in video_threaded)."""

    frame = cv.medianBlur(frame, 19)
    frame = cv.medianBlur(frame, 19)
    return frame, t0


def _parse_source(argv):
    """Parse command-line arguments into a video source.

    Matches the behavior of video_threaded.main: numeric args are treated as
    camera indices, everything else as filenames resolved via create_capture.
    """

    try:
        fn = argv[1]
    except Exception:
        fn = "0"  # default to first camera

    if isinstance(fn, str) and fn.isdigit():
        return int(fn)
    return fn


def main(argv=None):
    if argv is None:
        argv = sys.argv

    source = _parse_source(argv)

    try:
        cap = create_capture(source)
    except RuntimeError as e:
        print(e)
        return

    latency = StatValue()
    frame_interval = StatValue()
    last_frame_time = clock()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        t = clock()
        frame_interval.update(t - last_frame_time)
        last_frame_time = t

        # All processing happens on the main thread here.
        res, t0 = process_frame(frame, t)
        latency.update(clock() - t0)

        draw_str(res, (20, 20), "threaded      :  False")
        draw_str(res, (20, 40), "latency        :  %.1f ms" % (latency.value * 1000))
        draw_str(res, (20, 60), "frame interval :  %.1f ms" % (frame_interval.value * 1000))

        cv.imshow("single-threaded video", res)
        ch = cv.waitKey(1)
        if ch == 27:  # ESC
            break

    cap.release()
    cv.destroyAllWindows()


if __name__ == "__main__":
    print(__doc__)
    main()
