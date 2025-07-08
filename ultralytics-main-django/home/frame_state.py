# home/frame_state.py
import threading

frame_storage = {
    "latest_frame": None,
    "frame_id": 0,
    "processing": False,
    "stop": False,
    "lock": threading.Lock(),
    "detections": [],
}
