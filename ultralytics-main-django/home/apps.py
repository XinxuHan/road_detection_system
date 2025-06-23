import os
from django.apps import AppConfig

from YOLOv11 import settings
from .detect_main import YoloPredictor


class HomeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'home'

    def ready(self):
        if os.environ.get('RUN_MAIN') == 'true':  # Execute only in the main process
            self.yolo_predict = YoloPredictor()
            weight = os.path.join(settings.SAVEMODEL_ROOT, 'yolo11n.pt')
            self.yolo_predict.new_model_name = weight
            self.yolo_predict.load_yolo_model()
