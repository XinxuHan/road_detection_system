import threading

from ultralytics import YOLO
from ultralytics.data.loaders import LoadStreams
from ultralytics.engine.predictor import BasePredictor
import numpy as np
import time
import cv2



class YoloPredictor(BasePredictor):
    def __init__(self):
        super(YoloPredictor, self).__init__()

        self.used_model_name = None
        self.new_model_name = None  # 新更改的模型
        self.source = ''

        # config
        self.iou_thres = 0.45  # iou
        self.conf_thres = 0.25  # conf




    # 加载模型
    def load_yolo_model(self):
        self.model = YOLO(model=self.new_model_name)
        self.model(np.zeros((48, 48, 3)))  # 预先加载推理模型


    def release_capture(self):
        LoadStreams.terminate_flag = True





# class YoloPredictor(BasePredictor):
#     def __init__(self):
#         super(YoloPredictor, self).__init__()
#
#         self.used_model_name = None
#         self.new_model_name = None  # 新更改的模型
#         self.source = None
#         self.iou_thres = 0.45
#         self.conf_thres = 0.25
#
#         self.thread = None  # 线程对象
#         self.running = False  # 是否正在运行
#
#         self.frame_storage = {
#             "latest_frame": None,
#             "frame_id": 0,
#             "processing": False,
#             "abort": False,
#             "lock": threading.Lock()
#         }
#
#     def load_yolo_model(self):
#         """ 加载 YOLO 模型 """
#         self.model = YOLO(model=self.new_model_name)
#         self.model(np.zeros((48, 48, 3)))  # 预加载推理模型
#
#     def release_capture(self):
#         """ 释放摄像头 """
#         LoadStreams.terminate_flag = True
#
#     def start_detection(self, source):
#         """ 启动检测（视频文件或摄像头） """
#         if self.running:
#             print("已有检测正在运行，先停止...")
#             self.stop_detection()
#
#         self.source = source  # 赋值 source
#         self.running = True
#         self.frame_storage["abort"] = False
#         self.thread = threading.Thread(target=self.process_video)
#         self.thread.start()
#
#     def stop_detection(self):
#         """ 停止检测 """
#         if self.running:
#             with self.frame_storage["lock"]:
#                 self.frame_storage["abort"] = True
#             self.running = False
#             print("检测已停止")
#
#     def get_latest_frame(self):
#         """ 获取最新帧 """
#         with self.frame_storage["lock"]:
#             current_frame = self.frame_storage["latest_frame"]
#             current_id = self.frame_storage["frame_id"]
#             processing = self.frame_storage["processing"]
#             detections = self.frame_storage["detections"]
#
#         if not current_frame:
#             return {"frame_url": None, "frame_id": 0, "processing": processing, "detections": []}
#
#         import base64
#         frame_base64 = base64.b64encode(current_frame).decode("utf-8")
#         return {"frame_url": f"data:image/jpeg;base64,{frame_base64}", "frame_id": current_id, "processing": processing, "detections": detections}
#
#     def process_video(self):
#         """ 处理视频流/摄像头 """
#         try:
#             if isinstance(self.source, int) or (isinstance(self.source, str) and self.source.isdigit()):
#                 self.source = int(self.source)
#                 print(f"正在启动摄像头 {self.source}...")
#             else:
#                 print(f"正在处理视频文件：{self.source}")
#
#             iter_model = iter(self.model.track(
#                 source=self.source,
#                 show=False,
#                 stream=True,
#                 iou=self.iou_thres,
#                 conf=self.conf_thres
#             ))
#
#             while self.running:
#                 results = next(iter_model)
#                 img_box = results.plot()
#
#                 with self.frame_storage["lock"]:
#                     if self.frame_storage["abort"]:
#                         self.release_capture()
#                         print("检测终止，安全退出")
#                         break
#
#                 detections = []
#                 if results.boxes is not None and len(results.boxes):
#                     class_names = getattr(results, 'names', {})
#
#                     for idx in range(len(results.boxes)):
#                         box = results.boxes.xyxy[idx].cpu().numpy().astype(int)
#                         if results.boxes.id is None or results.boxes.id[idx] is None:
#                             continue
#
#                         detection = {
#                             "id": int(results.boxes.id[idx].item()),
#                             "class_name": class_names.get(int(results.boxes.cls[idx].item()), "unknown"),
#                             "confidence": round(float(results.boxes.conf[idx].item()) * 100),
#                             "bbox": {"x1": int(box[0]), "y1": int(box[1]), "x2": int(box[2]), "y2": int(box[3])}
#                         }
#                         detections.append(detection)
#
#                 _, buffer = cv2.imencode(".jpg", img_box)
#                 with self.frame_storage["lock"]:
#                     self.frame_storage["latest_frame"] = buffer.tobytes()
#                     self.frame_storage["frame_id"] += 1
#                     self.frame_storage["detections"] = detections
#
#                 time.sleep(0.001)
#
#         except Exception as e:
#             print(f"检测异常：{str(e)}")
#         finally:
#             self.running = False
#             with self.frame_storage["lock"]:
#                 self.frame_storage["processing"] = False