import cv2
import asyncio
import base64
import threading
from channels.generic.websocket import AsyncWebsocketConsumer
from django.apps import apps

class StreamHandler(AsyncWebsocketConsumer):
    async def connect(self):
        """The WebSocket connection is called when it is established"""
        await self.accept()
        print("[WebSocket] Connection accepted.")

    async def disconnect(self, code):
        """It is called when WebSocket is disconnected"""
        print(f"[WebSocket] Disconnected. Code: {code}")
        # There is no specific cleaning logic at present

    async def transmit_frame(self, image):
        """
        Encode the image frame as a JPEG and then send a base64 string via WebSocket
        """
        success, encoded = cv2.imencode(".jpg", image)
        if success:
            payload = base64.b64encode(encoded).decode("utf-8")
            await self.send(text_data=f"data:image/jpeg;base64,{payload}")
            print("[Transmit] Frame sent successfully.")
        else:
            print("[Transmit] Frame encoding failed.")

    def _video_pipeline(self, path):
        """
        Video processing pipeline (running in threads) :
        - Open the video stream
        - Perform YOLO object detection frame by frame
        - Draw the result and send it via WebSocket
        """
        print(f"[Pipeline] Starting video processing for: {path}")

        # Get the YoloPredictor instance
        app_conf = apps.get_app_config('home')
        yolo = app_conf.yolo_predict

        # Open the video file or camera stream
        capture = cv2.VideoCapture(path)

        if not capture.isOpened():
            print(f"[Pipeline] Failed to open video: {path}")
            return

        frame_count = 0

        while capture.isOpened():
            success, frame = capture.read()
            if not success:
                print("[Pipeline] Failed to read frame or stream ended.")
                break

            # Use YOLO for target tracking
            result = yolo.model.track(frame)[0]

            # Draw the results of the detection box
            output = result.plot()

            # Asynchronously push frames to WebSocket (executed in the main thread)
            asyncio.run(self.transmit_frame(output))
            frame_count += 1

        print(f"[Pipeline] Video processing finished. Total frames: {frame_count}")
        capture.release()

    async def start_processing(self, path):
        """
        Start the video processing thread (started in the main coroutine)
        """
        print(f"[WebSocket] Starting processing thread for video: {path}")
        thread = threading.Thread(target=self._video_pipeline, args=(path,))
        thread.start()
