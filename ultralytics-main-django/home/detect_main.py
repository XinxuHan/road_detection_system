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



