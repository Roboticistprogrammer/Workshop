#!/usr/bin/env python3

import subprocess
import time

print("=" * 70)
print("FPS Comparison: Single-threaded vs Multi-threaded")
print("=" * 70)
print("\nNOTE: Both versions run only the first 5 seconds of the video")
print("      and perform the same heavy processing (blur + edge detection).\n")

# Run single-threaded version
print("[1/2] Running single-threaded version...")
print("    (Watch the window, then check 'Average FPS' in the terminal.)\n")
subprocess.run(['python3', 'no_threading.py'])

time.sleep(1)

# Run multi-threaded version
print("\n[2/2] Running multi-threaded version...")
print("    (Watch the window, then check 'Average FPS' in the terminal.)\n")
subprocess.run(['python3', 'cap_multithreading.py'])

print("\n" + "=" * 70)
print("Comparison complete. Compare the 'Average FPS' lines above.")
print("Multi-threaded should be equal or higher when heavy processing dominates.")
print("=" * 70)