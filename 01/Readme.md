# Project 1: FPS Performance - Threading vs No Threading

## Objective
Demonstrate the performance difference between single-threaded and multi-threaded video frame processing using OpenCV.

## Key Concepts
- **Single-threaded approach**: Capture and display frames sequentially
- **Multi-threaded approach**: Frame capture and display happen in parallel
- **Frame Buffering**: Pre-load frames into memory while displaying previous frames
- **Performance Metric**: Compare FPS (Frames Per Second) between approaches

## Files
- `no_threading.py` - Single-threaded video capture with Gaussian blur + Canny edge detection
- `cap_multithreading.py` - Multi-threaded capture with processing and buffer visualization
- `gui_utils.py` - Utility functions for FPS calculation and frame-time tracking
- `comparison.py` - Automated comparison tool with detailed metrics

## Usage
1. Video file (`sample.mp4`) is in the `data/` directory
2. Run single-threaded version: `python no_threading.py`
3. Run multi-threaded version: `python cap_multithreading.py`
4. Run comparison: `python comparison.py`

## What's New in This Version

### 🔧 Heavy Processing Task
Both versions now apply:
- **Gaussian Blur (21x21 kernel)** - Smoothing filter
- **Canny Edge Detection** - Feature extraction

This realistic workload is where **multi-threading shows its advantage**.

### 📊 Key Metrics Displayed On-Screen
| Single-threaded | Multi-threaded |
|---|---|
| FPS counter | FPS counter |
| Frame drop count | Frame drop count |
| Version label | Buffer occupancy |
| | Version label |

### 📈 Expected Results with Heavy Processing

With 4K video + heavy processing:

**Without Processing (original):**
```
Single-threaded:  92 FPS (overhead is minimal, I/O is fast)
Multi-threaded:   65 FPS (buffering overhead > benefit)
Result: Single-threaded wins ❌
```

**With Heavy Processing (NEW):**
```
Single-threaded:  ~30-40 FPS (blur + edge detection blocks)
Multi-threaded:   ~40-55 FPS (capture during processing)
Result: Multi-threaded wins! ✓
```

### 🎯 Why It Works Now
1. **Single-threaded bottleneck**: Capture → Blur → EdgeDetect → Display (one-by-one)
2. **Multi-threaded advantage**: Capture thread fills buffer WHILE main thread processes previous frame
3. **Buffer fills up**: More frames ready = smoothness + no drops

Source:
https://www.youtube.com/watch?v=AREs0fKmcnY