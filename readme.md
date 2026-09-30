# 🚧 Pothole Detection & Tracking using YOLO

> **AI-powered road-surface analysis: detect, track, count, map and report potholes from images, videos and live streams.**

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![YOLO](https://img.shields.io/badge/YOLO-Ultralytics-orange)
![ByteTrack](https://img.shields.io/badge/Tracker-ByteTrack-green)
![Streamlit](https://img.shields.io/badge/UI-Streamlit-red)

<img src="Screenshot 2026-08-26 154942.png" alt="Pothole Detection & Tracking using YOLO">
<img src="Screenshot 2026-08-26 153843.png" alt="Pothole Detection & Tracking using YOLO">

---

## 📌 Overview

Potholes damage vehicles, raise maintenance costs and cause accidents, and manual road inspection is slow and expensive. This project uses **YOLO detection**, **ByteTrack tracking**, **OpenCV** video processing and a **Streamlit** dashboard to turn ordinary road footage into structured road-condition data.

Version 2 goes beyond drawing boxes on a video. It counts *unique* potholes, estimates severity, exports data, and can place detections on a map.

---

## ✨ Features

### Core (v1)
- YOLO pothole detection with a custom-trained model
- ByteTrack multi-object tracking with persistent IDs
- Annotated output video (box, class, confidence, track ID)
- Adjustable confidence threshold and image size
- Download of processed video

### 🆕 New in v2

| Feature | What it does |
|---|---|
| **Image detection** | Upload single images or a batch, not only video |
| **Live source support** | Run on a webcam, dashcam or RTSP/HTTP stream |
| **Unique pothole counter** | Counts distinct track IDs, so one pothole seen in 200 frames counts once |
| **Analytics dashboard** | Total count, confidence histogram, detections-per-frame timeline, FPS |
| **Severity estimation** | Low / Medium / High from relative bounding-box area and confidence |
| **Best-frame snapshots** | Saves the highest-confidence crop for each tracked pothole |
| **Data export** | CSV / JSON (frame, timestamp, ID, bbox, confidence, severity) |
| **GPS map view** | Reads GPS from `.srt` / `.gpx` / EXIF and plots potholes on an interactive map |
| **PDF / HTML report** | One-click summary with counts, severity breakdown and snapshots |
| **Performance controls** | Frame skip, device (CPU/GPU), half precision, tracker settings |
| **Model selector** | Switch between weight files (e.g. nano for speed, medium for accuracy) |
| **Progress & live preview** | Progress bar, ETA and live frame preview |
| **Input validation** | File-type and size checks, safe temp files, automatic cleanup |
| **Docker support** | One-command reproducible deployment |
| **Tests & CI** | `pytest` suite and GitHub Actions workflow |

---

## 🧠 System Architecture

```text
   Image / Video / Live Stream
               │
               ▼
        ┌──────────────┐
        │ Streamlit UI │◄── Sidebar: model, conf, imgsz, frame skip, device
        └──────┬───────┘
               ▼
        ┌──────────────┐
        │ Input Loader │  (validation, OpenCV reader)
        └──────┬───────┘
               ▼
        ┌──────────────┐
        │ YOLO Detector│  (Ultralytics)
        └──────┬───────┘
               ▼
        ┌──────────────┐
        │  ByteTrack   │  (persistent IDs)
        └──────┬───────┘
               ▼
   ┌───────────┴────────────┐
   ▼                        ▼
Annotation            Analytics Engine
(boxes, IDs)     (counts, severity, snapshots,
   │               GPS join, timeline)
   ▼                        │
Output Video                ▼
   │              CSV / JSON / Map / Report
   └────────────┬───────────┘
                ▼
     Visualization + Downloads
```

## 🔬 Processing Pipeline

```text
Input → Frame Extraction → (Frame Skip) → YOLO Inference → Confidence Filter
      → ByteTrack → Track IDs → Severity + Snapshot Logic → Annotation
      → Output Video + Detection Log → Analytics / Export / Map / Report
```

Detection runs per frame, tracking links detections across frames, and the analytics layer aggregates per track, so results describe **potholes**, not raw detections.

---

## 🧩 Core Components

- **YOLO (Ultralytics)** – single-stage detector returning box, class and confidence per frame.
- **ByteTrack** – associates detections across frames, including low-confidence ones, to keep IDs stable through brief occlusion or blur.
- **OpenCV** – opens videos and streams, reads and annotates frames, writes output video.
- **Analytics engine (new)** – keeps a per-track record: first/last frame, best confidence, best crop, severity, optional GPS position.
- **Streamlit** – upload, configuration, live preview, dashboard and downloads.

## 📐 Severity Estimation (new)

Severity is a **heuristic**, not a physical measurement:

```text
relative_area = bbox_area / frame_area

Low     relative_area <  1%
Medium  1% ≤ relative_area < 4%
High    relative_area ≥ 4%
```

Thresholds are configurable. Camera height, angle and lens change apparent size, so treat severity as a triage hint and validate it before acting on it.

---

## 📁 Repository Structure

```text
pothole-detection-yolo/
├── ui.py                       # Streamlit application
├── best (16).pt                # Trained YOLO weights
├── pothole-detection.ipynb     # Training / experimentation notebook
├── requirements.txt            # Dependencies
├── Dockerfile                  # (new) container build
├── .github/workflows/ci.yml    # (new) tests on every push
├── tests/                      # (new) pytest suite
└── README.md
```

## 🛠️ Technology Stack

| Technology | Role |
|---|---|
| Python | Core language |
| Ultralytics YOLO | Detection |
| ByteTrack | Tracking |
| OpenCV | Video and image processing |
| Streamlit | Web interface |
| Pandas | Detection log and statistics |
| Plotly / Folium | Charts and maps |
| pytest | Testing |
| Docker | Deployment |

---

## 🚀 Installation

```bash
git clone https://github.com/Ayman-muhammad/pothole-detection-yolo.git
cd pothole-detection-yolo
```

**Windows**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**Linux / macOS**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## ▶️ Run

```bash
streamlit run ui.py
```

Open `http://localhost:8501`.

**Docker (new)**
```bash
docker build -t pothole-yolo .
docker run -p 8501:8501 pothole-yolo
```

---

## 🧪 How to Use

1. **Choose a source** – image(s), video file, or live stream URL.
2. **Configure** – model, confidence, image size, frame skip, device.
3. **(Optional) Add GPS** – upload a `.srt` or `.gpx` file to geotag detections.
4. **Run** – watch the live preview and progress bar.
5. **Review** – unique count, severity split, confidence histogram, timeline.
6. **Export** – video, CSV/JSON log, snapshots, map, PDF/HTML report.

Example CSV output:

```csv
frame,timestamp_s,track_id,x1,y1,x2,y2,confidence,severity,lat,lon
120,4.00,7,312,410,455,520,0.86,Medium,17.0005,81.8040
```

---

## 📊 Model Development

```text
Dataset → Annotation → Training → Validation → Evaluation → Model Selection → Deployment
```

The notebook `pothole-detection.ipynb` contains the workflow. Experiment with epochs, image size, batch size, augmentation, learning rate and model size.

```text
Precision = TP / (TP + FP)
Recall    = TP / (TP + FN)
IoU       = Area of Intersection / Area of Union
mAP       = mean Average Precision across classes / IoU thresholds
```

Report only values you have actually measured:

| Metric | Value |
|---|---|
| Precision | _TBD_ |
| Recall | _TBD_ |
| mAP@0.5 | _TBD_ |
| mAP@0.5:0.95 | _TBD_ |

## 📚 Dataset Considerations

Diversity matters: pothole size and depth, road material, weather, lighting, camera angle and height, motion blur, shadows, water-filled potholes, occlusion and multiple potholes per frame.

## ⚠️ Known Challenges

- **Lighting** – glare, shadows, night, rain
- **Camera motion** – shake, blur, perspective change
- **Appearance** – potholes vary in shape, colour and texture
- **False positives** – cracks, patches, manholes, shadows, reflections, markings
- **ID switches** – a long occlusion can give a pothole a new ID and inflate the unique count
- **Severity accuracy** – area-based severity depends on camera setup

## ⚡ Performance

Options: GPU acceleration, smaller model, lower image size, frame skipping, `fp16`, background processing. The dashboard reports FPS, latency per frame and total time. When quoting performance, state the hardware and settings.

## 🧪 Testing (new)

```bash
pytest
```

- **Unit** – config handling, severity thresholds, track aggregation, exports
- **Integration** – model loading, video pipeline, tracker integration
- **App** – upload, processing, output availability, downloads

## 🔐 Security & Privacy

Road videos can contain licence plates, faces and GPS metadata. Recommended controls: file-type and size validation, safe filenames, temp-file cleanup, local processing by default, optional face/plate blurring, limited retention, and no secrets in the repo.

## 🤖 Responsible AI

Detections are decision support, not verified infrastructure assessments. Validate on representative local roads and analyse false positives, false negatives, dataset bias and weather/camera variation. Keep a human in the loop for maintenance decisions.

---

## 🏗️ Future Production Architecture

```text
Web / Mobile Clients
        │
   API Gateway
        │
 ┌──────┼───────────┐
 ▼      ▼           ▼
Detect  Media     Auth
 API   Service   Service
 └──────┼───────────┘
        ▼
 Inference (YOLO + Tracker)
        ▼
 Storage (metadata + media)
        ▼
 Analytics → Admin Dashboard
```

---

## 🗂️ Contributing

```bash
git checkout -b feature/new-feature
git add .
git commit -m "feat: describe your change"
git push -u origin feature/new-feature
```

Commit prefixes: `feat` · `fix` · `docs` · `refactor` · `test` · `perf` · `security` · `chore`

## 📦 Model Files

`best (16).pt` is committed directly. For larger models consider Git LFS, a model registry, object storage or release artifacts. Renaming it to something like `pothole_yolo_best.pt` avoids spaces and parentheses in paths.

## ⚠️ Attribution & Licensing

This repository may include model assets or implementation material derived from prior work. Respect original repository, dataset, model and dependency licences, and preserve required attribution. Nothing here claims ownership of third-party datasets, models or code. Document any modifications clearly.

---

## 👨‍💻 Author

Harshitha Arava

> *Building intelligent systems for real-world problems.*

<p align="center">

**🚧 Detect. Track. Analyze. Map. Improve Roads.**

</p>
