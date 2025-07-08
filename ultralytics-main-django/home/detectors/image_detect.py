import os
import cv2
import django
from django.apps import apps
from PIL import ImageFile
from YOLOv11 import settings

# Set Django environment variables
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "YOLOv11.settings")
django.setup()

# Allow loading of incomplete images (to prevent PIL decoding failure)
ImageFile.LOAD_TRUNCATED_IMAGES = True


def detect(img_path):
    """
    Perform target detection on a single image and return the image path and recognition result of the result.
    :param img_path: Input the image path
    :return: A dictionary containing detection results and image paths
    """
    print(f"[Detect] Start detecting image: {img_path}")

    # Obtain the YOLO model predictor
    yolo = apps.get_app_config('home').yolo_predict
    output_dir = settings.MEDIA_ROOT

    # Initialize the response body
    response = {
        "image_url": "",
        "results": [],
        "error": None
    }

    try:
        # Read the image
        img = cv2.imread(img_path)
        if img is None:
            raise ValueError("Failed to read image file")
        print("[Detect] Image successfully loaded.")

        # Model reasoning
        predictions = iter(yolo.model.track(
            source=img,
            show=False,
            iou=yolo.iou_thres,
            conf=yolo.conf_thres
        ))
        result = next(predictions)
        print("[Detect] Inference completed.")

        # Obtain the prediction box and label mapping
        boxes = result.boxes
        label_map = getattr(result, 'names', {})
        detections = []

        if boxes is not None and len(boxes):
            print(f"[Detect] {len(boxes)} objects detected.")
            for idx in range(len(boxes)):
                coords = boxes.xyxy[idx].cpu().numpy().astype(int)
                cls_id = int(boxes.cls[idx].item())
                confidence = round(float(boxes.conf[idx].item()) * 100)
                obj_id = int(boxes.id[idx].item()) if boxes.id is not None else None

                detection = {
                    "id": obj_id,
                    "class_name": label_map.get(cls_id, "unknown"),
                    "confidence": confidence,
                    "bbox": {
                        "x1": int(coords[0]),
                        "y1": int(coords[1]),
                        "x2": int(coords[2]),
                        "y2": int(coords[3]),
                    }
                }
                detections.append(detection)
                print(f"[Detect] Object #{idx}: {detection}")

        else:
            print("[Detect] No objects detected.")

        # Save the detection result image
        result_img = result.plot()
        file_base = os.path.splitext(os.path.basename(img_path))[0]
        result_name = f"{file_base}_result.jpg"
        result_path = os.path.join(output_dir, result_name)
        cv2.imwrite(result_path, result_img)
        print(f"[Detect] Result image saved to: {result_path}")

        # Construct response information
        response["image_url"] = os.path.join(settings.MEDIA_URL, result_name)
        response["results"] = detections

    except Exception as e:
        # Catch and print the exception
        response["error"] = str(e)
        print(f"[Detect Error] {str(e)}")

    print("[Detect] Detection process completed.\n")
    return response
