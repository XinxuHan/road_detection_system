import time
import cv2
from django.apps import apps
from home.frame_state import frame_storage


def process_video(source):
    """
    Process local video files or camera video streams, and use the YOLO model for object detection
    The detection results are saved in the global shared variable frame_storage for real-time access by the front end.
    """

    print(f"[Video] Starting video processing for source: {source}")

    # Obtain an example of the YOLO prediction model
    yolo = apps.get_app_config('home').yolo_predict

    # Initialize the state of the shared frame
    with frame_storage["lock"]:
        frame_storage.update({
            "processing": True,
            "stop": False,
            "frame_id": 0,
            "detections": []
        })
    print("[Video] Frame storage initialized.")

    try:
        # If it is a digital number of the camera (such as 0), convert it to int
        if isinstance(source, int) or (isinstance(source, str) and source.isdigit()):
            source = int(source)
            print(f"[Video] Source interpreted as camera index: {source}")

        # Start tracking (streaming)
        track_stream = iter(yolo.model.track(
            source=source,
            show=False,
            stream=True,
            iou=yolo.iou_thres,
            conf=yolo.conf_thres
        ))
        print("[Video] Model tracking stream initialized.")

        while True:
            # Get the detection result of the next frame
            result = next(track_stream)
            rendered = result.plot()

            # Check if there is a stop signal
            with frame_storage["lock"]:
                if frame_storage["stop"]:
                    print("[Video] Stop signal received. Releasing capture.")
                    yolo.release_capture()
                    break

            # Analyze the detection results
            detections = []
            boxes = result.boxes
            label_map = getattr(result, 'names', {})

            if boxes is not None and len(boxes):
                print(f"[Video] Detected {len(boxes)} objects.")
                for idx in range(len(boxes)):
                    if boxes.id is None or boxes.id[idx] is None:
                        continue
                    coords = boxes.xyxy[idx].cpu().numpy().astype(int)
                    cls_id = int(boxes.cls[idx].item())
                    confidence = round(float(boxes.conf[idx].item()) * 100)
                    obj_id = int(boxes.id[idx].item())

                    detection = {
                        "id": obj_id,
                        "class_name": label_map.get(cls_id, "unknown"),
                        "confidence": confidence,
                        "bbox": {
                            "x1": int(coords[0]), "y1": int(coords[1]),
                            "x2": int(coords[2]), "y2": int(coords[3])
                        }
                    }
                    detections.append(detection)
                    print(f"[Video] Detection {idx}: {detection}")

            # Encode the image as JPEG for display on the front-end page
            _, buffer = cv2.imencode(".jpg", rendered)

            # Update the global frame store
            with frame_storage["lock"]:
                frame_storage["latest_frame"] = buffer.tobytes()
                frame_storage["frame_id"] += 1
                frame_storage["detections"] = detections

            time.sleep(0.001)  # Control the frame processing speed to prevent excessive CPU usage

    finally:
        # After the video stream processing is completed, clear the frame_storage state
        with frame_storage["lock"]:
            frame_storage.update({
                "processing": False,
                "latest_frame": None,
                "frame_id": 0,
                "detections": []
            })
        print("[Video] Video processing ended and frame storage cleared.")
