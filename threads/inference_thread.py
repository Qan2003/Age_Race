from config import *
from utils import safe_get_label, get_smoothed

def inference_thread():
    skip = 0
    frame_skip_rate = 2

    while State.running:
        try:
            frame = capture_queue.get(timeout=0.1)
        except:
            continue

        skip += 1
        if skip < frame_skip_rate:
            continue
        skip = 0

        try:
            results_detect = model_detect.predict(frame, verbose=False, conf=0.5)
        except Exception as e:
            print("Detection error:", e)
            continue

        results = []

        for result in results_detect:
            if not hasattr(result, "boxes"):
                continue

            boxes = result.boxes.xyxy.cpu().numpy()

            for box in boxes:
                x1, y1, x2, y2 = map(int, box)

                face = frame[y1:y2, x1:x2]

                try:
                    age_r = model_age.predict(face, verbose=False)
                    race_r = model_race.predict(face, verbose=False)

                    age, age_conf = safe_get_label(age_r)
                    race, race_conf = safe_get_label(race_r)

                    age = get_smoothed(age_history, age)
                    race = get_smoothed(race_history, race)

                except Exception as e:
                    print("Classification error:", e)
                    age, race = "Err", "Err"
                    age_conf = race_conf = 0.0

                results.append(((x1, y1, x2, y2), age, age_conf, race, race_conf))

        try:
            display_queue.put_nowait((frame, results))
        except:
            pass
