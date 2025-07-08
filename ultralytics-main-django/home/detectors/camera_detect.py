import time
import cv2
from django.apps import apps
from home.frame_state import frame_storage


def process_camera(source):
    """
    Process the camera or video stream input, perform target detection frame by frame
    and save the detection results in the shared frame_storage.
    """
    print(f"[Init] Starting camera processing for source: {source}")

    # Obtain the loaded YOLO model
    yolo = apps.get_app_config('home').yolo_predict
    cap = cv2.VideoCapture(source)

    # Initialize the shared frame state, set the processing state to True and the frame number to 0
    with frame_storage["lock"]:
        frame_storage.update({
            "processing": True,
            "stop": False,
            "frame_id": 0,
            "detections": []
        })
    print("[Init] Frame storage initialized.")

    try:
        frame_count = 0
        while cap.isOpened():
            # Check if it needs to be stopped
            with frame_storage["lock"]:
                if frame_storage["stop"]:
                    print("[Loop] Stop signal received. Exiting loop.")
                    break

            ret, frame = cap.read()
            if not ret:
                print("[Loop] Failed to read frame. Ending.")
                break

            # Object detection: YOLO tracking mode
            result = yolo.model.track(
                source=frame,
                iou=yolo.iou_thres,
                conf=yolo.conf_thres
            )[0]

            # Draw the results
            processed = result.plot()

            # Parse the detection boxes and categories
            detections = []
            boxes = result.boxes
            label_map = getattr(result, 'names', {})

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
                            "x1": int(coords[0]), "y1": int(coords[1]),
                            "x2": int(coords[2]), "y2": int(coords[3])
                        }
                    })
                print(f"[Detect] Frame {frame_count}: {len(detections)} objects detected.")

            # Encode the image in JPEG format
            _, buffer = cv2.imencode(".jpg", processed)

            # Update the status of the shared frame
            with frame_storage["lock"]:
                frame_storage["latest_frame"] = buffer.tobytes()
                frame_storage["frame_id"] = frame_count
                frame_storage["detections"] = detections

            frame_count += 1
            time.sleep(0.001)  # Prevent CPU/GPU overload

    finally:
        # Clear status and resources
        with frame_storage["lock"]:
            frame_storage.update({
                "processing": False,
                "latest_frame": None,
                "frame_id": 0,
                "detections": []
            })
        cap.release()
        print(f"[Cleanup] Camera released and frame storage cleared. Total frames processed: {frame_count}")
