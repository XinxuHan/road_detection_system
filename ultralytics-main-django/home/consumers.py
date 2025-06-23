import cv2
import asyncio
import base64
import threading
from channels.generic.websocket import AsyncWebsocketConsumer
from django.apps import apps

class StreamHandler(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, code):
        # No cleanup needed for now
        pass

    async def transmit_frame(self, image):
        success, encoded = cv2.imencode(".jpg", image)
        if success:
            payload = base64.b64encode(encoded).decode("utf-8")
            await self.send(text_data=f"data:image/jpeg;base64,{payload}")

    def _video_pipeline(self, path):
        app_conf = apps.get_app_config('home')
        yolo = app_conf.yolo_predict
        capture = cv2.VideoCapture(path)

        while capture.isOpened():
            success, frame = capture.read()
            if not success:
                break

            result = yolo.model.track(frame)[0]
            output = result.plot()

            asyncio.run(self.transmit_frame(output))

        capture.release()

    async def start_processing(self, path):
        thread = threading.Thread(target=self._video_pipeline, args=(path,))
        thread.start()
