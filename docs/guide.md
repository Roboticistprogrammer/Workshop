# How Multithread Helps

CapMultiThreading class works by constantly loading frames into a buffer while the system is busy displaying others.

Frame Buffering: Instead of waiting to grab a new frame when the display finishes, the frames are preloaded into a memory buffer.
Parallel Execution: The frame capture thread runs in parallel with the display process, allowing both to happen at the same time.
Reduced Latency: Since frames are preloaded, the program does not experience any downtime waiting for frames to be fetched from the video file, leading to faster performance.