import os
import cv2
import threading
import time
from django.apps import apps
import django
from YOLOv11 import settings
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "YOLOv11.settings")
django.setup()


def detect(img_path):
    out_dir = settings.MEDIA_ROOT
    home_app_config = apps.get_app_config('home')
    yolo_predict = home_app_config.yolo_predict

    response_data = {
        "image_url": "",
        "results": [],
        "error": None
    }

    try:
        # 读取图片
        image = cv2.imread(img_path)
        if image is None:
            raise ValueError("无法读取图片文件")

        iter_model = iter(yolo_predict.model.track(
            source=image,
            show=False,
            iou=yolo_predict.iou_thres,
            conf=yolo_predict.conf_thres
        ))
        result = next(iter_model)


        detections = []
        if result.boxes is not None and len(result.boxes):
            class_names = getattr(result, 'names', {})  # 获取类别名称映射

            for idx in range(len(result.boxes)):
                # 处理每个检测目标
                box = result.boxes.xyxy[idx].cpu().numpy().astype(int)
                # 是否存在tracking id
                if result.boxes.id is not None:
                    obj_id = int(result.boxes.id[idx].item())
                else:
                    obj_id = None

                detection = {
                    "id": obj_id,
                    "class_name": class_names.get(int(result.boxes.cls[idx].item()), "unknown"),
                    "confidence": round(float(result.boxes.conf[idx].item()) * 100),
                    "bbox": {
                        "x1": int(box[0]),
                        "y1": int(box[1]),
                        "x2": int(box[2]),
                        "y2": int(box[3])
                    }
                }

                detections.append(detection)

        #print(detections)

        # 保存结果图片
        result_img = result.plot()
        img_name = os.path.basename(img_path).split('.')[0]
        output_image_name = f'{img_name}_result.jpg'
        output_image_path = os.path.join(out_dir, output_image_name)
        cv2.imwrite(output_image_path, result_img)

        # 构建返回数据
        response_data["image_url"] = os.path.join(settings.MEDIA_URL, output_image_name)
        response_data["results"] = detections

    except Exception as e:
        response_data["error"] = str(e)
        print(f"检测出错: {str(e)}")

    return response_data


frame_storage = {
    "latest_frame": None,
    "frame_id": 0,
    "processing": False,
    "abort": False,
    "lock": threading.Lock(),

}





def process_video(source):
    home_app_config = apps.get_app_config('home')
    yolo_predict = home_app_config.yolo_predict

    # 初始化存储
    with frame_storage["lock"]:
        frame_storage["processing"] = True
        frame_storage["abort"] = False
        frame_storage["frame_id"] = 0
        frame_storage["detections"] = []

    try:
        # 自动判断输入源类型
        if isinstance(source, int) or (isinstance(source, str) and source.isdigit()):
            source = int(source)
            print(f"正在启动摄像头{source}...")
        else:
            print(f"正在处理视频文件：{source}")

        iter_model = iter(yolo_predict.model.track(
            source=source,
            show=False,
            stream=True,
            iou=yolo_predict.iou_thres,
            conf=yolo_predict.conf_thres
        ))



        # 处理循环
        while True:
            results = next(iter_model)
            img_box = results.plot()

            # 检查是否被终止
            with frame_storage["lock"]:
                if frame_storage["abort"]:
                    yolo_predict.release_capture()
                    print("检测到终止请求，安全退出")
                    break


            detections = []
            if results.boxes is not None and len(results.boxes):
                class_names = getattr(results, 'names', {})  # 获取类别名称映射

                for idx in range(len(results.boxes)):
                    box = results.boxes.xyxy[idx].cpu().numpy().astype(int)

                    # 跳过 ID 为空的目标
                    if results.boxes.id is None or results.boxes.id[idx] is None:
                        continue

                    # 是否存在tracking id
                    if results.boxes.id is not None:
                        obj_id = int(results.boxes.id[idx].item())
                    else:
                        obj_id = None

                    detection = {
                        "id": obj_id,
                        "class_name": class_names.get(int(results.boxes.cls[idx].item()), "unknown"),
                        "confidence": round(float(results.boxes.conf[idx].item()) * 100),
                        "bbox": {
                            "x1": int(box[0]),
                            "y1": int(box[1]),
                            "x2": int(box[2]),
                            "y2": int(box[3])
                        }
                    }
                    detections.append(detection)


            # 生成帧数据
            _, buffer = cv2.imencode(".jpg", img_box)
            with frame_storage["lock"]:
                frame_storage["latest_frame"] = buffer.tobytes()
                frame_storage["frame_id"] += 1
                frame_storage["detections"] = detections

            time.sleep(0.001)  # 控制帧率约30fps


    except Exception as e:
        print(f"检测异常：{str(e)}")
    finally:
        with frame_storage["lock"]:
            frame_storage["processing"] = False
            frame_storage["latest_frame"] = None  # 清空上一帧
            frame_storage["frame_id"] = 0
            frame_storage["detections"] = []





def process_camera(source):
    home_app_config = apps.get_app_config('home')
    yolo_predict = home_app_config.yolo_predict
    cap = cv2.VideoCapture(source)

    with frame_storage["lock"]:
        frame_storage["processing"] = True
        frame_storage["abort"] = False  # 重置终止标志
        frame_storage["frame_id"] = 0
        frame_storage["detections"] = []  # 初始化检测结果

    try:
        frame_counter = 0
        while cap.isOpened():
            # 检查是否被终止
            with frame_storage["lock"]:
                if frame_storage["abort"]:
                    break
            ret, frame = cap.read()
            if not ret:
                break

            results = yolo_predict.model.track(source=frame,iou=yolo_predict.iou_thres,conf=yolo_predict.conf_thres)[0]
            processed_frame = results.plot()

            detections = []
            if results.boxes is not None and len(results.boxes):
                class_names = getattr(results, 'names', {})  # 获取类别名称映射

                for idx in range(len(results.boxes)):
                    box = results.boxes.xyxy[idx].cpu().numpy().astype(int)

                    # 跳过 ID 为空的目标
                    if results.boxes.id is None or results.boxes.id[idx] is None:
                        continue

                    # 是否存在tracking id
                    if results.boxes.id is not None:
                        obj_id = int(results.boxes.id[idx].item())
                    else:
                        obj_id = None

                    detection = {
                        "id": obj_id,
                        "class_name": class_names.get(int(results.boxes.cls[idx].item()), "unknown"),
                        "confidence": round(float(results.boxes.conf[idx].item()) * 100),
                        "bbox": {
                            "x1": int(box[0]),
                            "y1": int(box[1]),
                            "x2": int(box[2]),
                            "y2": int(box[3])
                        }
                    }
                    detections.append(detection)

            # 生成帧数据
            _, buffer = cv2.imencode(".jpg", processed_frame)
            frame_data = buffer.tobytes()
            with frame_storage["lock"]:
                frame_storage["latest_frame"] = frame_data
                frame_counter += 1
                frame_storage["frame_id"] = frame_counter
                frame_storage["detections"] = detections

            time.sleep(0.001)

    finally:
        with frame_storage["lock"]:
            frame_storage["processing"] = False
            frame_storage["latest_frame"] = None  # 清空上一帧
            frame_storage["frame_id"] = 0
            frame_storage["detections"] = []
        cap.release()









