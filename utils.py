from collections import Counter

def get_smoothed(history, value):
    history.append(value)
    return Counter(history).most_common(1)[0][0]


def safe_get_label(result):
    """An toàn lấy nhãn & độ tin cậy, không can thiệp ảnh"""
    try:
        r0 = result[0]

        if hasattr(r0, "probs"):
            top = getattr(r0.probs, "top1", None)
            conf = getattr(r0.probs, "top1conf", 0.0)

            if top is not None:
                label = r0.names.get(int(top), str(top))
                return label, float(conf)

        return "Unknown", 0.0

    except Exception:
        return "Unknown", 0.0
