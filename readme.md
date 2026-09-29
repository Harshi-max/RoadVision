# 🤟 SignBridge — Real-Time Sign Language & Assistive Gesture Recognition

> **Real-time computer vision for hand-gesture recognition, ASL alphabet recognition, and accessibility-focused interaction using OpenCV and MediaPipe.**

SignBridge is a computer-vision application that processes live webcam video, detects hands and their 21 landmarks, recognizes hand gestures/signs, and converts stable gestures into text or configurable accessibility actions.

The project extends a real-time hand-gesture recognition workflow with image preprocessing, normalized landmark features, temporal smoothing, confidence/stability handling, two-hand support, optional text-to-speech, and performance profiling.

---

<img src="Screenshot 2026-08-26 154942.png" alt="Pothole Detection & Tracking using YOLO">
<img src="Screenshot 2026-08-26 153843.png" alt="Pothole Detection & Tracking using YOLO">

---

## 📌 Overview

Communication and computer interaction can become difficult when conventional keyboard, mouse, or speech interfaces are not suitable.

SignBridge explores how **real-time computer vision** can make webcam-based interaction more accessible by recognizing hand poses and signs directly from video.

The application can:

1. Capture frames from a webcam
2. Apply optional image preprocessing
3. Detect one or more hands using MediaPipe
4. Extract 21 landmarks per detected hand
5. Normalize geometric features
6. Recognize supported gestures or ASL alphabet signs
7. Apply temporal smoothing and stability filtering
8. Build a text buffer from recognized signs
9. Trigger configurable accessibility actions
10. Provide optional text-to-speech
11. Measure FPS, latency, and processing-stage timing

---

# 🎯 Project Goals

The primary goals are:

- Build a real-time webcam computer-vision pipeline
- Detect hand landmarks reliably
- Recognize static hand gestures
- Support ASL alphabet recognition
- Reduce recognition flicker using temporal filtering
- Support accessibility-oriented gesture controls
- Process video frames efficiently
- Measure real-time FPS and latency
- Provide a modular and reproducible Python implementation
- Demonstrate practical image-processing and computer-vision engineering

---

# 🧠 System Architecture

The application follows an end-to-end real-time vision pipeline:

```text
                         USER
                          │
                          ▼
                  ┌───────────────┐
                  │    Webcam     │
                  └───────┬───────┘
                          │
                          ▼
                  ┌───────────────┐
                  │ OpenCV Camera │
                  │ Frame Capture │
                  └───────┬───────┘
                          │
                          ▼
                  ┌───────────────┐
                  │  Preprocessing│
                  │ Resize / CLAHE│
                  │ Blur / Sharp. │
                  └───────┬───────┘
                          │
                          ▼
                  ┌───────────────┐
                  │    MediaPipe  │
                  │  Hand Detect. │
                  └───────┬───────┘
                          │
                          ▼
                  ┌───────────────┐
                  │ 21 Landmarks  │
                  │ per Hand      │
                  └───────┬───────┘
                          │
                          ▼
                  ┌───────────────┐
                  │ Feature       │
                  │ Extraction    │
                  └───────┬───────┘
                          │
                          ▼
              ┌─────────────────────────┐
              │ Gesture / ASL Recognition│
              └────────────┬────────────┘
                           │
                           ▼
                  ┌────────────────┐
                  │ Temporal       │
                  │ Smoothing      │
                  └───────┬────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │ Stable Result /  │
                 │ Confidence Check │
                 └────────┬─────────┘
                          │
              ┌───────────┼────────────┐
              ▼           ▼            ▼
          Text Buffer    TTS      Accessibility
                                      Actions

             ┌──────────────────────────┐
             │ Performance Monitoring   │
             │ FPS / Latency / Profiling│
             └──────────────────────────┘
```

---

# 🔬 Computer Vision Pipeline

The core processing workflow is:

```text
Webcam Frame
     │
     ▼
Frame Capture
     │
     ▼
Optional Preprocessing
     │
     ▼
Hand Detection
     │
     ▼
21-Point Landmark Extraction
     │
     ▼
Feature Normalization
     │
     ▼
Gesture / ASL Recognition
     │
     ▼
Confidence / Stability Filtering
     │
     ▼
Temporal Smoothing
     │
     ▼
Text / Accessibility Action
     │
     ▼
Visualization + Performance Metrics
```

Each stage has a specific responsibility:

- **OpenCV** → camera capture, frame processing, rendering, screenshots
- **MediaPipe** → hand detection and landmark extraction
- **Feature extraction** → normalized geometric hand features
- **Gesture recognition** → maps hand features to supported gestures/signs
- **Temporal smoothing** → reduces frame-to-frame prediction noise
- **Accessibility layer** → maps stable gestures to actions
- **TTS** → optionally converts completed text into speech
- **Performance monitor** → measures FPS, latency, and processing stages

---

# 🧩 Core Components

## 1. Real-Time Camera Capture

OpenCV is used to capture webcam frames.

Typical responsibilities include:

- Opening the selected camera
- Configuring resolution
- Reading frames
- Tracking frame count
- Timestamping frames
- Releasing camera resources
- Handling camera initialization failures

Conceptually:

```text
Webcam
   │
   ▼
OpenCV VideoCapture
   │
   ├── Read Frame
   ├── Timestamp
   ├── Process
   └── Release
```

The implementation should report measured FPS rather than assuming that the requested camera FPS is achieved.

---

# 🖼️ 2. Image Preprocessing

An optional preprocessing stage can be enabled before hand detection.

Supported operations can include:

- Resize
- Brightness adjustment
- Contrast adjustment
- Gaussian blur
- CLAHE
- Sharpening

The goal is to provide a controlled way to study how image-processing operations affect real-time hand detection.

Example:

```text
Raw Frame
    │
    ├── Resize
    ├── Contrast
    ├── CLAHE
    ├── Blur
    └── Sharpen
         │
         ▼
Processed Frame
```

Preprocessing should remain configurable because aggressive processing can increase latency.

---

# ✋ 3. Hand Detection

MediaPipe is used to detect hands and extract their landmarks.

For each detected hand, the system can expose:

- 21 landmark points
- Normalized coordinates
- Pixel coordinates
- Hand bounding box
- Left/right hand information where available
- Detection/tracking state

Conceptually:

```text
Camera Frame
     │
     ▼
MediaPipe
     │
     ├── Hand 1
     │     └── 21 Landmarks
     │
     └── Hand 2
           └── 21 Landmarks
```

The number of supported hands and confidence thresholds should be configurable.

---

# 📐 4. Feature Extraction

Raw pixel coordinates can vary significantly with camera distance and hand position.

SignBridge therefore uses normalized geometric features where practical.

Features can include:

- Fingertip coordinates
- Joint coordinates
- Finger angles
- Landmark distances
- Palm size
- Thumb-index distance
- Relative finger positions
- Normalized hand geometry

Conceptually:

```text
21 Landmarks
     │
     ▼
Geometric Features
     │
     ▼
Normalization
     │
     ▼
Gesture Representation
```

This makes the recognition logic less dependent on the absolute position and scale of the hand in the frame.

---

# 🤟 5. Gesture Recognition

The system supports the existing gesture-recognition workflow and can extend it with configurable thresholds.

For each frame, the recognizer may produce:

```text
Gesture
Confidence / Heuristic Score
Hand State
```

Supported gestures should remain based on the actual implemented recognition rules.

When the system cannot confidently identify a gesture, it should return:

```text
UNKNOWN
```

rather than forcing an incorrect action.

---

# 🔤 6. ASL Alphabet Recognition

SignBridge supports **static ASL alphabet recognition**.

The workflow is:

```text
Hand
 │
 ▼
Landmarks
 │
 ▼
Feature Extraction
 │
 ▼
ASL Recognition
 │
 ▼
Stable Character
 │
 ▼
Text Buffer
```

Example:

```text
A → H → E → L → L → O
```

becomes:

```text
HELLO
```

The application should support practical text-buffer operations such as:

- Character insertion
- Space
- Clear
- Backspace where implemented
- Stable-character filtering
- Character cooldown

### Important limitation

This project should be described as **static ASL alphabet/sign recognition**, not complete American Sign Language translation.

Full sign-language translation requires substantially more temporal, linguistic, and contextual modeling.

---

# 🔄 7. Temporal Smoothing

Real-time gesture recognition can fluctuate between neighboring predictions.

For example:

```text
Frame 1 → PEACE
Frame 2 → PEACE
Frame 3 → UNKNOWN
Frame 4 → PEACE
Frame 5 → PEACE
```

Instead of immediately triggering an action, SignBridge uses temporal stability.

Conceptually:

```text
Frame Predictions
      │
      ▼
History Buffer
      │
      ▼
Majority / Stability Check
      │
      ▼
Stable Gesture
```

Configurable parameters can include:

- History length
- Minimum stable frames
- Cooldown duration

This reduces accidental repeated actions and visual flickering.

---

# 🎯 8. Confidence and Stability Filtering

A gesture should not immediately trigger a system action simply because it appeared in one frame.

The application can combine:

- Recognition result
- Confidence/heuristic score
- Consecutive stable frames
- Cooldown state

Example:

```text
Gesture: THUMBS_UP
Score: 0.91
Stable Frames: 5
Cooldown: Ready

→ Action Allowed
```

If the underlying recognizer does not provide a true probabilistic confidence value, the displayed score should be documented as a heuristic rather than model probability.

---

# ✋✋ 9. Two-Hand Support

The system can support detection of two simultaneous hands.

When two hands are detected:

```text
Frame
 │
 ├── Left Hand
 │     └── 21 Landmarks
 │
 └── Right Hand
       └── 21 Landmarks
```

The application can visualize:

- Separate hand landmarks
- Bounding boxes
- Hand labels where available
- Individual hand states

Two-hand gestures should only be added where they can be implemented and tested reliably.

---

# ♿ 10. Accessibility Interaction

SignBridge includes an accessibility-oriented action layer.

The idea is:

```text
Hand Gesture
     │
     ▼
Stable Recognition
     │
     ▼
Action Mapping
     │
     ▼
Computer Interaction
```

Example configurable mappings:

```text
OPEN_HAND    → PLAY / PAUSE
THUMBS_UP    → VOLUME UP
THUMBS_DOWN  → VOLUME DOWN
FIST         → MUTE
PEACE        → NEXT
ROCK_ON      → PREVIOUS
```

These mappings should be configurable rather than hard-coded into the recognition engine.

Actions should include:

- Cooldown protection
- Enable/disable configuration
- Platform checks
- Graceful fallback when unsupported

---

# 🔊 11. Volume Control

The original gesture workflow includes pinch-based volume control.

SignBridge preserves this functionality and can improve it using:

- Configurable pinch thresholds
- Smoothing
- Visual volume percentage
- Stable pinch detection

Conceptually:

```text
Thumb
  +
Index Finger
  │
  ▼
Pinch Distance
  │
  ▼
Normalized Volume
  │
  ▼
System Volume
```

Platform-specific audio functionality should remain isolated from the rest of the application.

---

# 🗣️ 12. Optional Text-to-Speech

A completed text phrase can optionally be converted into speech.

Workflow:

```text
ASL Characters
      │
      ▼
Text Buffer
      │
      ▼
Completed Phrase
      │
      ▼
Text-to-Speech
```

TTS should:

- Be optional
- Not run on every frame
- Not block the camera-processing loop unnecessarily
- Fail gracefully if the optional dependency is unavailable

---

# 📊 13. Performance Monitoring

Real-time computer vision requires measurable performance.

SignBridge should track:

- Current FPS
- Average FPS
- Frame processing time
- Average latency
- Minimum latency
- Maximum latency
- Frames processed
- Skipped/dropped frames where applicable

Example overlay:

```text
FPS:       29.4
Latency:   31.2 ms
Frames:    1842
Hands:     1
Mode:      SIGN LANGUAGE
```

Values must be measured at runtime.

Do not hard-code performance claims.

---

# 🔬 14. Processing-Stage Profiling

A profiling mode can measure approximate time spent in each major pipeline stage.

Example:

```text
Capture:          2.1 ms
Preprocessing:   1.4 ms
Detection:       18.7 ms
Features:         0.6 ms
Recognition:      0.4 ms
Rendering:        3.2 ms
--------------------------------
Total:           26.4 ms
```

This helps identify where latency is being introduced.

Actual measurements should be recorded only from real execution.

---

# 📈 15. Performance Metrics

A session can optionally record:

```text
FPS
Latency
Frame Count
Session Duration
Processing Stage Timing
```

A performance log can be stored as JSON:

```text
outputs/logs/performance_<timestamp>.json
```

The project should avoid making unsupported claims such as:

> "Runs at 60 FPS"

unless the result was actually measured and documented with the hardware/software environment.

---

# 🖥️ 16. Real-Time Visualization

The OpenCV interface can display:

```text
---------------------------------------------
              SIGNBRIDGE
---------------------------------------------

Gesture:       OPEN HAND
Confidence:    92%
Hands:         1

ASL Character: H
Text:          HELLO

FPS:            29.4
Latency:        31.2 ms

Mode:           SIGN LANGUAGE
---------------------------------------------
```

Useful keyboard controls:

```text
Q       → Quit
S       → Screenshot
C       → Clear text
SPACE   → Add space
1       → Gesture mode
2       → Sign-language mode
3       → Accessibility mode
P       → Performance overlay
R       → Reset statistics
```

---

# 📸 17. Screenshot Capture

Screenshots should preserve the existing functionality while making saved evidence more useful.

A screenshot can include:

- Current frame
- Recognized gesture/sign
- Current mode
- FPS
- Latency
- Timestamp

Example:

```text
outputs/screenshots/signbridge_2026-09-29_19-30-12.jpg
```

Screenshots should be captured on demand rather than continuously.

---

# ⚙️ 18. Configuration

Important settings should be configurable.

Example:

```yaml
camera:
  index: 0
  width: 1280
  height: 720
  target_fps: 30

detection:
  max_hands: 2
  min_detection_confidence: 0.5
  min_tracking_confidence: 0.5

smoothing:
  history_size: 5
  min_stable_frames: 3
  cooldown_ms: 500

preprocessing:
  enabled: false
  clahe: false
  blur: false
  sharpening: false

performance:
  enabled: true
  profiling: false

accessibility:
  enabled: true

sign_language:
  enabled: true
  speech_enabled: false
```

Actual configuration values should match the implementation.

---

# 📂 Repository Structure

A modular implementation can follow this structure:

```text
signbridge/
│
├── src/
│   ├── camera.py
│   ├── hand_detector.py
│   ├── gesture_recognizer.py
│   ├── sign_language.py
│   ├── temporal_smoother.py
│   ├── feature_extractor.py
│   ├── confidence.py
│   ├── accessibility.py
│   ├── performance.py
│   ├── preprocessing.py
│   ├── ui.py
│   ├── logger.py
│   └── utils.py
│
├── configs/
│   └── config.yaml
│
├── outputs/
│   ├── screenshots/
│   └── logs/
│
├── tests/
│   ├── test_gestures.py
│   ├── test_features.py
│   ├── test_smoothing.py
│   └── test_performance.py
│
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

The actual repository may use a slightly different structure if that better preserves the original implementation.

---

# 🛠️ Technology Stack

| Technology | Role |
|---|---|
| **Python** | Core programming language |
| **OpenCV** | Webcam capture, image processing and visualization |
| **MediaPipe** | Hand detection and 21-point landmark extraction |
| **NumPy** | Numerical and geometric feature processing |
| **PyYAML** | Configuration management |
| **pyttsx3** *(optional)* | Text-to-speech |
| **PyCaw** *(optional)* | Windows audio control |
| **Git** | Version control |
| **GitHub** | Source-code hosting |

The project intentionally avoids adding C++ or embedded hardware dependencies.

---

# ⚙️ Requirements

Recommended environment:

```text
Python 3.x
```

Core dependencies:

```text
opencv-python
mediapipe
numpy
PyYAML
```

Optional dependencies may include:

```text
pyttsx3
pycaw
```

The exact versions should be maintained in `requirements.txt`.

---

# 🚀 Installation

## 1. Clone the repository

```bash
git clone <your-repository-url>
cd signbridge
```

## 2. Create a virtual environment

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 3. Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

# ▶️ Running the Application

Start the application using the project's main entry point:

```bash
python main.py
```

If the project retains separate mode-specific entry points, document those commands here as well.

A webcam should be available for real-time inference.

---

# 🧪 Application Workflow

## Step 1 — Start Camera

The application initializes the configured webcam.

```text
Webcam
  ↓
OpenCV
  ↓
Frame Stream
```

## Step 2 — Detect Hands

MediaPipe detects visible hands and their landmarks.

```text
Frame
  ↓
MediaPipe
  ↓
21 Landmarks
```

## Step 3 — Extract Features

Landmark coordinates are transformed into normalized geometric features.

## Step 4 — Recognize

The system recognizes supported gestures or ASL alphabet signs.

## Step 5 — Stabilize

Temporal filtering determines whether a result is stable enough to accept.

## Step 6 — Act

The result can become:

```text
Gesture → Accessibility Action
```

or:

```text
ASL → Character → Text
```

or:

```text
Text → Speech
```

## Step 7 — Monitor

The application reports measured FPS and latency.

---

# 🧪 Testing

Unit tests should cover logic that does not require a physical webcam.

Recommended tests include:

### Feature Tests

- Distance calculation
- Angle calculation
- Feature normalization
- Invalid landmark handling

### Recognition Tests

- Known gesture patterns
- Unknown gesture handling
- Threshold behavior

### Smoothing Tests

- History buffering
- Majority voting
- Minimum stable frames
- Cooldown logic

### Performance Tests

- Frame timing
- FPS calculation
- Latency statistics
- Session aggregation

Run:

```bash
pytest
```

Hardware-dependent webcam tests should be identified separately.

---

# 📊 Performance Methodology

Performance depends on:

- CPU/GPU
- Camera resolution
- Number of hands
- MediaPipe configuration
- Image preprocessing
- Lighting
- Python/runtime environment

The application should measure:

```text
FPS
Latency per Frame
Processing Time
Capture Time
Detection Time
Recognition Time
Rendering Time
Memory Usage where practical
```

Performance results should always be reported together with the test environment.

---

# ⚠️ Limitations

The current system has several important limitations.

### Static Sign Recognition

The project focuses on static hand/ASL alphabet recognition. It should not be described as a complete sign-language translation system.

### Lighting

Hand detection can be affected by:

- Low light
- Strong shadows
- Backlighting
- Motion blur

### Camera Position

Recognition can vary with:

- Camera angle
- Hand orientation
- Distance from camera
- Occlusion

### Gesture Ambiguity

Some gestures may have similar visual characteristics.

### Platform-Specific Controls

Accessibility actions such as system volume control may depend on the operating system.

### No Depth Sensor

The project does not perform true depth sensing.

### Performance

Real-time performance depends on the execution environment and configured processing pipeline.

---

# 🔐 Responsible AI / Accessibility Considerations

SignBridge is an experimental computer-vision and accessibility project.

Recognition results should not be treated as authoritative communication without appropriate validation.

For real-world accessibility deployment, additional work would be required around:

- Recognition accuracy
- User testing
- Accessibility evaluation
- Diverse hand appearances and signing styles
- False-positive analysis
- False-negative analysis
- Robustness across lighting conditions
- Privacy
- On-device processing
- Human-centered design

---

# 🚀 Future Development Roadmap

## Phase 1 — Core Recognition

- [x] Real-time webcam processing
- [x] Hand landmark detection
- [x] Gesture recognition
- [x] ASL alphabet recognition
- [x] Temporal smoothing
- [x] FPS monitoring

## Phase 2 — Real-Time CV Engineering

- [ ] Modular camera pipeline
- [ ] Configurable preprocessing
- [ ] Normalized feature extraction
- [ ] Two-hand processing
- [ ] Confidence/stability filtering
- [ ] Processing-stage profiling
- [ ] Latency logging

## Phase 3 — Accessibility

- [ ] Configurable gesture-to-action mapping
- [ ] Improved volume control
- [ ] Optional text-to-speech
- [ ] Additional accessibility actions
- [ ] Optional voice-to-caption mode

## Phase 4 — Advanced Vision

Potential future research directions:

- Dynamic gesture recognition
- Temporal sequence models
- Personalized gesture calibration
- Robustness to different lighting conditions
- Lightweight on-device inference
- Model-based hand-pose classification

---

# 🧠 Engineering Lessons

This project provides practical experience across:

### Computer Vision

- Hand detection
- Landmark estimation
- Image preprocessing
- Geometric feature extraction
- Gesture recognition
- Temporal filtering
- Real-time video processing

### Real-Time Systems

- Frame-by-frame processing
- Latency measurement
- FPS measurement
- Processing-stage profiling
- Resource-aware pipeline design

### Machine Learning / Recognition

- Feature representation
- Classification logic
- Threshold selection
- Stability filtering
- Recognition under noisy inputs

### Software Engineering

- Modular Python architecture
- Configuration management
- Error handling
- Logging
- Unit testing
- Dependency management

### Accessibility

- Gesture-based computer interaction
- Sign-to-text workflow
- Optional text-to-speech
- Configurable interaction mappings

---

# ⚡ Performance Optimization Considerations

Potential optimization strategies include:

- Lowering camera resolution
- Reducing unnecessary preprocessing
- Limiting maximum detected hands
- Frame skipping where appropriate
- Avoiding repeated system actions
- Efficient landmark processing
- Profiling before optimization
- Keeping rendering separate from recognition logic

Optimization should be driven by measured bottlenecks rather than assumptions.

---

# 🧪 Recommended Evaluation

A useful evaluation should test the system under different conditions:

```text
Lighting
├── Normal
├── Low light
└── Backlit

Camera Distance
├── Near
├── Medium
└── Far

Hand Count
├── One hand
└── Two hands

Motion
├── Static
└── Moving

Background
├── Simple
└── Cluttered
```

Record actual observations and measurements rather than fabricating accuracy or performance numbers.

---

# 📋 Definition of Done

A feature should be considered complete when:

```text
[ ] Implementation complete
[ ] Existing functionality preserved
[ ] Input validation added
[ ] Error handling added
[ ] Unit tests added where appropriate
[ ] Tested locally
[ ] Hardware-dependent behavior checked
[ ] Performance considered
[ ] Documentation updated
[ ] Dependencies reviewed
[ ] No secrets committed
```

---

# 🔒 Privacy and Security

The application processes webcam frames and may generate screenshots or logs.

A production implementation should consider:

- Explicit camera permission
- Local/on-device processing where possible
- Screenshot management
- Log retention
- Temporary-file cleanup
- No unnecessary cloud upload
- Dependency security
- No API keys or credentials in source code

The application should not retain camera data unnecessarily.

---

# 🗂️ Git Workflow

Recommended workflow:

```bash
git status
```

Create a feature branch:

```bash
git checkout -b feature/signbridge-upgrade
```

Stage changes:

```bash
git add .
```

Commit:

```bash
git commit -m "feat: upgrade gesture recognition pipeline"
```

Push:

```bash
git push -u origin feature/signbridge-upgrade
```

---

# 📝 Commit Convention

Recommended prefixes:

```text
feat:
fix:
docs:
refactor:
test:
perf:
chore:
```

Examples:

```bash
git commit -m "feat: add temporal gesture smoothing"

git commit -m "feat: add ASL text buffer"

git commit -m "perf: add frame latency profiling"

git commit -m "test: add feature extraction tests"

git commit -m "docs: update computer vision pipeline"
```

---

# ⚠️ Attribution

This project is based on and extends an existing hand-gesture recognition implementation.

When redistributing or modifying the original repository, respect:

- Original repository license
- Third-party dependency licenses
- MediaPipe licensing
- Dataset/model licensing
- Original author attribution requirements

Clearly document which components were inherited and which were added or modified.

---

# 👨‍💻 Project

## SignBridge

**Real-Time Sign Language & Assistive Gesture Recognition**

Built with:

```text
Python
OpenCV
MediaPipe
NumPy
PyYAML
```

Core concepts:

```text
Computer Vision
      +
Image Processing
      +
Hand Landmark Detection
      +
Gesture Recognition
      +
Temporal Filtering
      +
Real-Time Video Processing
      +
Performance Profiling
      +
Accessibility
```

---

# 🌉 Project Vision

The goal of SignBridge is to explore how real-time computer vision can connect human gestures with digital interfaces.

```text
Human Hand
    ↓
Camera
    ↓
Computer Vision
    ↓
Landmarks
    ↓
Gesture / Sign
    ↓
Text / Action
    ↓
Accessible Interaction
```

The project is designed as an engineering-focused exploration of **real-time camera processing, computer vision, and accessible human-computer interaction**.
