import asyncio

import cv2
import threading
import os
import base64
from channels.generic.websocket import AsyncWebsocketConsumer
from django.apps import apps

class VideoStreamConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def send_frame(self, frame):
        _, buffer = cv2.imencode(".jpg", frame)
        frame_base64 = base64.b64encode(buffer).decode("utf-8")
        await self.send(text_data=f"data:image/jpeg;base64,{frame_base64}")

    def process_video(self, video_path):
        home_app_config = apps.get_app_config('home')
        yolo_predict = home_app_config.yolo_predict
        cap = cv2.VideoCapture(video_path)

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            results = yolo_predict.model.track(frame)[0]
            processed_frame = results.plot()

            # 发送处理后帧
            asyncio.run(self.send_frame(processed_frame))

        cap.release()

    async def start_processing(self, video_path):
        threading.Thread(target=self.process_video, args=(video_path,)).start()
