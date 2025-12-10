import cv2
import time
from config import display_queue, State

def display_thread():
    fps = 0
    fps_time = time.time()
    fps_count = 0

    while State.running:
        try:
            frame, results = display_queue.get(timeout=0.1)
        except:
            continue

        for (x1, y1, x2, y2), age, age_conf, race, race_conf in results:
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"Age: {age} ({age_conf:.2f})", (x1+5, y1-30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)
            cv2.putText(frame, f"Race: {race} ({race_conf:.2f})", (x1+5, y1-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)

        fps_count += 1
        now = time.time()
        if now - fps_time >= 1:
            fps = fps_count / (now - fps_time)
            fps_count = 0
            fps_time = now

        cv2.putText(frame, f"FPS: {fps:.1f}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)

        cv2.imshow("Age & Race Detection", frame)
        if cv2.waitKey(1) == ord('q'):
            State.running = False
            break

    cv2.destroyAllWindows()
