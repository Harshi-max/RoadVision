# Experimental C++ Camera Pipeline

This is a lightweight, independent OpenCV-based camera pipeline that demonstrates lower-level engineering patterns without modifying the working Python application.

Features:
- camera or video input
- frame buffering
- preprocessing hooks
- FPS and latency measurement
- frame skipping
- thread-safe producer-consumer flow

Build:
```bash
cmake -S cpp_camera -B cpp_camera/build
cmake --build cpp_camera/build
```

Run:
```bash
./cpp_camera/build/roadvision_cpp_camera --source 0
```
