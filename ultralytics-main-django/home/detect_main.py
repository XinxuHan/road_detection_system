from ultralytics import YOLO
from ultralytics.data.loaders import LoadStreams
from ultralytics.engine.predictor import BasePredictor
import numpy as np


class YoloPredictor(BasePredictor):
    def __init__(self):
        # Initialize the parent class
        super(YoloPredictor, self).__init__()

        # The file name (path) of the currently used model
        self.used_model_name = None

        # The file name (path) of the new model to be loaded
        self.new_model_name = None

        # Data sources, such as image paths, video stream addresses, etc
        self.source = ''

        # Configuration item
        self.iou_thres = 0.45

        # Configuration item
        self.conf_thres = 0.25

        print("[Init] YoloPredictor initialized with default settings.")
        print(f"[Init] IOU threshold = {self.iou_thres}, Confidence threshold = {self.conf_thres}")

    # Load model
    def load_yolo_model(self):
        if not self.new_model_name:
            print("[Error] No model file specified in self.new_model_name!")
            return

        print(f"[Load] Loading YOLO model from: {self.new_model_name}")
        self.model = YOLO(model=self.new_model_name)

        # Trigger the preheating of the model to avoid the delay of the first inference
        dummy_input = np.zeros((48, 48, 3))
        self.model(dummy_input)

        print("[Load] Model loaded successfully.")
        print("[Load] Model class names:")
        print(self.model.names)

    # Release the video stream
    def release_capture(self):
        print("[Release] Releasing video/camera stream capture...")
        LoadStreams.terminate_flag = True
        print("[Release] Capture terminated.")
