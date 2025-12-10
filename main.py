import time
import threading
from config import State
from threads.capture_thread import capture_thread
from threads.inference_thread import inference_thread
from threads.display_thread import display_thread

if __name__ == "__main__":
    t1 = threading.Thread(target=capture_thread, daemon=True)
    t2 = threading.Thread(target=inference_thread, daemon=True)
    t3 = threading.Thread(target=display_thread, daemon=True)

    t1.start()
    t2.start()
    t3.start()

    try:
        while State.running:
            time.sleep(0.1)
    except KeyboardInterrupt:
        State.running = False

    print("Stopped.")
