from ultralytics import YOLO
import queue
from collections import deque

# Load models 1 lần duy nhất
model_detect = YOLO(r"D:\Downloads\yolov11n-face.pt")
model_age = YOLO(r"D:\Downloads\age\weights\best.pt")
model_race = YOLO(r"D:\Downloads\race\weights\best.pt")

# Queue chung giữa các thread
capture_queue = queue.Queue(maxsize=1)
display_queue = queue.Queue(maxsize=1)

# Biến điều khiển chạy - dùng class để có thể thay đổi từ các thread khác
class State:
    running = True

# Lịch sử smoothing
age_history = deque(maxlen=3)
race_history = deque(maxlen=3)