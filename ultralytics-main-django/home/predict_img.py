import os
import cv2
import time
import threading
from django.apps import apps
import django
from PIL import ImageFile
from YOLOv11 import settings

# Set Django environment and allow loading incomplete images
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "YOLOv11.settings")
django.setup()
ImageFile.LOAD_TRUNCATED_IMAGES = True

# Shared state for video/camera streaming
frame_storage = {
    "latest_frame": None,
    "frame_id": 0,
    "processing": False,
    "abort": False,
    "lock": threading.Lock(),
    "detections": [],
}

def detect(img_path):
    """Performs object detection on a single image."""
    yolo = apps.get_app_config('home').yolo_predict
    output_dir = settings.MEDIA_ROOT
    response = {"image_url": "", "results": [], "error": None}

    try:
        img = cv2.imread(img_path)
        if img is None:
            raise ValueError("Failed to read image file")

        predictions = iter(yolo.model.track(
            source=img,
            show=False,
            iou=yolo.iou_thres,
            conf=yolo.conf_thres
        ))
        result = next(predictions)

        boxes = result.boxes
        label_map = getattr(result, 'names', {})
        detections = []

        if boxes is not None and len(boxes):
            for idx in range(len(boxes)):
                coords = boxes.xyxy[idx].cpu().numpy().astype(int)
                cls_id = int(boxes.cls[idx].item())
                confidence = round(float(boxes.conf[idx].item()) * 100)
                obj_id = int(boxes.id[idx].item()) if boxes.id is not None else None

                detections.append({
                    "id": obj_id,
                    "class_name": label_map.get(cls_id, "unknown"),
                    "confidence": confidence,
                    "bbox": {
                        "x1": int(coords[0]),
                        "y1": int(coords[1]),
                        "x2": int(coords[2]),
                        "y2": int(coords[3]),
                    }
                })

        result_img = result.plot()
        file_base = os.path.splitext(os.path.basename(img_path))[0]
        result_name = f"{file_base}_result.jpg"
        result_path = os.path.join(output_dir, result_name)
        cv2.imwrite(result_path, result_img)

        response["image_url"] = os.path.join(settings.MEDIA_URL, result_name)
        response["results"] = detections

    except Exception as e:
        response["error"] = str(e)
        print(f"[detect error]: {str(e)}")

    return response

def process_video(source):
    """Streams and tracks objects from video or webcam."""
    yolo = apps.get_app_config('home').yolo_predict

    with frame_storage["lock"]:
        frame_storage.update({
            "processing": True,
            "abort": False,
            "frame_id": 0,
            "detections": []
        })

    try:
        if isinstance(source, int) or (isinstance(source, str) and source.isdigit()):
            source = int(source)
            print(f"Opening camera {source}...")
        else:
            print(f"Opening video file: {source}")

        track_stream = iter(yolo.model.track(
            source=source,
            show=False,
            stream=True,
            iou=yolo.iou_thres,
            conf=yolo.conf_thres
        ))

        while True:
            result = next(track_stream)
            rendered = result.plot()

            with frame_storage["lock"]:
                if frame_storage["abort"]:
                    yolo.release_capture()
                    print("[stream] Aborted by user.")
                    break

            boxes = result.boxes
            label_map = getattr(result, 'names', {})
            detections = []

            if boxes is not None and len(boxes):
                for idx in range(len(boxes)):
                    if boxes.id is None or boxes.id[idx] is None:
                        continue
                    coords = boxes.xyxy[idx].cpu().numpy().astype(int)
                    cls_id = int(boxes.cls[idx].item())
                    confidence = round(float(boxes.conf[idx].item()) * 100)
                    obj_id = int(boxes.id[idx].item())

                    detections.append({
                        "id": obj_id,
                        "class_name": label_map.get(cls_id, "unknown"),
                        "confidence": confidence,
                        "bbox": {
                            "x1": int(coords[0]),
                            "y1": int(coords[1]),
                            "x2": int(coords[2]),
                            "y2": int(coords[3]),
                        }
                    })

            _, buffer = cv2.imencode(".jpg", rendered)
            with frame_storage["lock"]:
                frame_storage["latest_frame"] = buffer.tobytes()
                frame_storage["frame_id"] += 1
                frame_storage["detections"] = detections

            time.sleep(0.001)

    except Exception as e:
        print(f"[stream error]: {str(e)}")
    finally:
        with frame_storage["lock"]:
            frame_storage.update({
                "processing": False,
                "latest_frame": None,
                "frame_id": 0,
                "detections": []
            })

def process_camera(source):
    """Processes frames from live camera source one by one."""
    yolo = apps.get_app_config('home').yolo_predict
    cap = cv2.VideoCapture(source)

    with frame_storage["lock"]:
        frame_storage.update({
            "processing": True,
            "abort": False,
            "frame_id": 0,
            "detections": []
        })

    try:
        frame_count = 0
        while cap.isOpened():
            with frame_storage["lock"]:
                if frame_storage["abort"]:
                    break

            ret, frame = cap.read()
            if not ret:
                break

            result = yolo.model.track(
                source=frame,
                iou=yolo.iou_thres,
                conf=yolo.conf_thres
            )[0]
            processed = result.plot()

            boxes = result.boxes
            label_map = getattr(result, 'names', {})
            detections = []

            if boxes is not None and len(boxes):
                for idx in range(len(boxes)):
                    if boxes.id is None or boxes.id[idx] is None:
                        continue
                    coords = boxes.xyxy[idx].cpu().numpy().astype(int)
                    cls_id = int(boxes.cls[idx].item())
                    confidence = round(float(boxes.conf[idx].item()) * 100)
                    obj_id = int(boxes.id[idx].item())

                    detections.append({
                        "id": obj_id,
                        "class_name": label_map.get(cls_id, "unknown"),
                        "confidence": confidence,
                        "bbox": {
                            "x1": int(coords[0]),
                            "y1": int(coords[1]),
                            "x2": int(coords[2]),
                            "y2": int(coords[3]),
                        }
                    })

            _, buffer = cv2.imencode(".jpg", processed)
            with frame_storage["lock"]:
                frame_storage["latest_frame"] = buffer.tobytes()
                frame_storage["frame_id"] = frame_count
                frame_storage["detections"] = detections

            frame_count += 1
            time.sleep(0.001)

    finally:
        with frame_storage["lock"]:
            frame_storage.update({
                "processing": False,
                "latest_frame": None,
                "frame_id": 0,
                "detections": []
            })
        cap.release()
