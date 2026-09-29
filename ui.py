import os
import tempfile
import time
from pathlib import Path

import cv2
import streamlit as st
from ultralytics import YOLO

from roadvision.config import load_config
from roadvision.incidents.incident_manager import IncidentManager
from roadvision.ocr.ocr_service import OCRService
from roadvision.performance.performance_monitor import PerformanceMonitor
from roadvision.preprocessing.preprocessor import PreprocessingPipeline
from roadvision.severity.severity_estimator import estimate_severity
from roadvision.tracking.track_manager import TrackManager

st.set_page_config(
    page_title="RoadVision",
    page_icon="🚧",
    layout="wide",
)

st.title("RoadVision — Real-Time Road Defect Detection & Reporting")
st.write("YOLO-based pothole detection, tracking, severity estimation, and report generation.")

cfg = load_config()


@st.cache_resource
def load_model():
    return YOLO("best (16).pt")


model = load_model()

uploaded_file = st.file_uploader(
    "Upload a road video or image",
    type=["mp4", "avi", "mov", "mkv", "jpg", "jpeg", "png"],
)

source_mode = st.radio("Input source", ["Uploaded media", "Webcam (device 0)"])
confidence = st.slider("Confidence threshold", 0.1, 1.0, float(cfg["detection"]["confidence_threshold"]), 0.05)
image_size = st.selectbox("Image size", [640, 768, 960], index=2)
preprocess_enabled = st.checkbox("Enable preprocessing", value=bool(cfg["preprocessing"]["enabled"]))

if uploaded_file is not None:
    st.image(uploaded_file, channels="BGR") if uploaded_file.type.lower().startswith("image") else st.video(uploaded_file)

    if st.button("🚀 Detect Road Defects"):
        input_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
        input_file.write(uploaded_file.read())
        input_file.close()
        input_path = input_file.name

        output_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
        output_file.close()
        output_path = output_file.name

        cap = cv2.VideoCapture(input_path)
        if not cap.isOpened():
            st.error("Could not open the uploaded media.")
        else:
            fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) or 960
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) or 540
            fourcc = cv2.VideoWriter_fourcc(*"mp4v")
            writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) or 0
            progress_bar = st.progress(0)
            status = st.empty()
            frame_number = 0

            monitor = PerformanceMonitor(sample_window=int(cfg["performance"]["sample_window"]))
            tracker = TrackManager()
            incident_manager = IncidentManager()
            preprocessor = PreprocessingPipeline({**cfg["preprocessing"], "enabled": preprocess_enabled})
            ocr = OCRService(enabled=bool(cfg["ocr"]["enabled"]), min_confidence=float(cfg["ocr"].get("min_confidence", 0.4)))

            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                frame_number += 1
                start = time.perf_counter()
                processed_frame = preprocessor.apply(frame)
                results = model.track(
                    processed_frame,
                    conf=confidence,
                    imgsz=image_size,
                    tracker=cfg["tracking"]["tracker"],
                    persist=True,
                    verbose=False,
                )
                latency = time.perf_counter() - start
                monitor.record_frame(latency)

                annotated_frame = results[0].plot() if results else frame.copy()
                if hasattr(results[0], "boxes") and results[0].boxes is not None:
                    for box in results[0].boxes:
                        if box.conf is None:
                            continue
                        conf_value = float(box.conf[0])
                        if conf_value < confidence:
                            continue
                        track_id = int(box.id[0]) if getattr(box, "id", None) is not None and box.id is not None else frame_number
                        xyxy = [int(v) for v in box.xyxy[0].tolist()]
                        x1, y1, x2, y2 = xyxy
                        relative_area = ((x2 - x1) * (y2 - y1)) / max(frame.shape[0] * frame.shape[1], 1)
                        severity = estimate_severity(confidence=conf_value, relative_area=relative_area, persistence=0.6, road_coverage=relative_area)
                        tracker.update_track(track_id, frame_number, conf_value, tuple(xyxy))
                        cv2.putText(
                            annotated_frame,
                            f"ID {track_id} {severity['severity']}",
                            (x1, max(20, y1 - 8)),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.6,
                            (0, 255, 255),
                            2,
                        )
                        incident_manager.create_incident(
                            track_id=track_id,
                            confidence=conf_value,
                            severity=severity["severity"],
                            source_video=input_path,
                            severity_score=severity["severity_score"],
                            frame_count=1,
                            location_status="unavailable",
                        )

                writer.write(annotated_frame)
                if frame_number % int(cfg["ocr"].get("sample_every_n_frames", 60)) == 0:
                    ocr_result = ocr.process_frame(annotated_frame, frame_id=frame_number, timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
                    if ocr_result:
                        st.caption(f"OCR sample: {ocr_result['text']}")

                if total_frames > 0:
                    progress = frame_number / total_frames
                    progress_bar.progress(progress)
                    status.write(f"Processing frame {frame_number}/{total_frames}")

            cap.release()
            writer.release()
            progress_bar.progress(1.0)
            status.success("RoadVision detection completed.")

            stats = monitor.summary()
            st.subheader("Performance metrics")
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Processing FPS", f"{stats['actual_fps']:.2f}")
            m2.metric("Average latency", f"{stats['avg_latency_ms']:.2f} ms")
            m3.metric("P95 latency", f"{stats['p95_latency_ms']:.2f} ms")
            m4.metric("Frames processed", stats["frames_processed"])

            st.write(stats)

            st.subheader("Processed video")
            with open(output_path, "rb") as video_file:
                video_bytes = video_file.read()
            st.video(video_bytes)
            st.download_button("⬇️ Download processed video", data=video_bytes, file_name="roadvision_output.mp4", mime="video/mp4")

            if os.path.exists(input_path):
                os.remove(input_path)

            if os.path.exists(output_path):
                pass

if source_mode == "Webcam (device 0)":
    st.info("Webcam mode is available in the local Python workflow. For a live Streamlit session, use local execution and camera access permissions.")
    if st.button("Open Webcam Capture"):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            st.error("Could not access the webcam.")
        else:
            placeholder = st.empty()
            frame_count = 0
            while frame_count < 40:
                ret, frame = cap.read()
                if not ret:
                    break
                results = model.track(frame, conf=confidence, imgsz=image_size, tracker="bytetrack.yaml", persist=True, verbose=False)
                annotated = results[0].plot() if results else frame
                placeholder.image(annotated, channels="BGR")
                frame_count += 1
            cap.release()
