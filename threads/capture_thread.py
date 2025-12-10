import cv2
from config import capture_queue, State

def capture_thread():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FPS, 30)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    while State.running:
        ret, frame = cap.read()
        if not ret:
            break
        try:
            capture_queue.put_nowait(frame)
        except:
            pass

    cap.release()
