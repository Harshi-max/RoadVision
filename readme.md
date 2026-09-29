# RoadVision

RoadVision is a lightweight road-defect analytics system that keeps the working YOLO pothole detection flow, adds tracking, severity estimation, optional OCR, location metadata, duplicate incident prevention, and reporting for maintenance workflows.

## Features
- Real-time pothole detection from video or webcam input
- Multi-object tracking across frames
- Road ROI and preprocessing configuration
- Severity estimation based on visible features only
- Optional OCR sampling for road signs and text
- GPS metadata support with graceful fallback
- Local incident tracking and deduplication
- Evidence-frame capture and JSON report generation
- Authority routing configuration layer
- Performance metrics for FPS and latency
- Experimental C++ camera pipeline in `cpp_camera`

## Architecture

```text
Camera / Video Input
        │
        ▼
  Frame Capture + Preprocessing
        │
        ▼
   YOLO Detection (Ultralytics)
        │
        ▼
     Track Manager + Deduplication
        │
        ├── Severity Estimation
        ├── OCR Sampling (optional)
        ├── GPS / location metadata (optional)
        ├── Incident persistence
        └── Performance monitor
                │
                ▼
        Streamlit dashboard + reports
```

## Installation

```bash
cd pothole-detection-yolo
python -m venv .venv
. .venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Running

### Video detection
```bash
streamlit run ui.py
```

Then upload a road video and click the detection button.

### Webcam workflow
```bash
python -c "from ultralytics import YOLO; model = YOLO('best (16).pt'); print('model loaded')"
```

The repository keeps its original YOLO-based pipeline and the Streamlit interface as the primary local workflow. Webcam access will depend on local camera permissions and environment support.

## Performance

The project measures metrics that are actually available during execution:
- input FPS is reported when the source provides it
- actual processing FPS is computed from processed frames over elapsed wall-clock time
- average frame latency is measured in milliseconds
- P95 latency is computed from the observed frame-latency samples
- dropped frames are counted when the processing loop skips or misses a frame
- total detections and unique tracked potholes are accumulated while processing

No benchmark claims are made in this project. Values are reported only from the running session.

## Project motivation

RoadVision is designed to support maintenance workflows by turning video observations into structured road-defect records. The system is intended to help prioritize inspections, collect evidence, and organize defect reporting without claiming physical depth measurement or production deployment status.

## Limitations
- Detection depends on the training data and camera conditions.
- Severity is a visual estimate based on measurable features rather than a true depth measurement.
- GPS data is optional and may be unavailable.
- OCR depends on readable text and image quality.
- Authority routing is prototype/configuration-based rather than a full municipal integration layer.

## Repository layout

```text
pothole-detection-yolo/
├── ui.py
├── roadvision/
│   ├── config.py
│   ├── authority/
│   ├── incidents/
│   ├── location/
│   ├── notifications/
│   ├── ocr/
│   ├── performance/
│   ├── preprocessing/
│   ├── reporting/
│   ├── severity/
│   └── tracking/
├── config/
├── data/
├── cpp_camera/
├── tests/
├── requirements.txt
├── .env.example
├── best (16).pt
├── readme.md
└── README.md
```

## Notes

The system keeps the original YOLO workflow functional while adding modular RoadVision components that can be tested independently.
