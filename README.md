# Age & Race Detection (YOLO + Multi-threading)

Dự án này sử dụng **Ultralytics YOLO** để thực hiện:

* Phát hiện khuôn mặt (Face Detection)
* Phân loại tuổi (Age Classification)
* Phân loại chủng tộc (Race Classification)

Hệ thống chạy **real-time** bằng cách tách xử lý thành 3 luồng (threads):

* `capture_thread`: lấy ảnh từ webcam
* `inference_thread`: detect + phân loại
* `display_thread`: hiển thị kết quả & FPS

Dữ liệu được truyền giữa các luồng bằng `queue` kích thước 1 để tránh trễ hình, đảm bảo luôn xử lý **frame mới nhất**.

---

## 📁 **Cấu trúc dự án**

```
project/
│
├── main.py                     # File chạy chính
├── config.py                   # Load models & biến dùng chung
├── utils.py                    # Hàm smoothing + xử lý nhãn
│
├── threads/
│   ├── capture_thread.py       # Luồng lấy từ webcam
│   ├── inference_thread.py     # Luồng YOLO detect + age/race
│   └── display_thread.py       # Luồng hiển thị kết quả
│
└── README.md
```

---

## 🚀 **Tính năng chính**

* Chạy real-time với hiệu suất cao nhờ đa luồng
* Phát hiện nhiều khuôn mặt trong cùng một khung hình
* Dự đoán tuổi và chủng tộc cho từng khuôn mặt
* Smoothing kết quả theo lịch sử để giảm nhiễu (mode filter)
* Hiển thị FPS theo thời gian thực
* Code chia module rõ ràng, dễ bảo trì, dễ mở rộng

---

## 🧠 **Mô hình được sử dụng**

| Loại model          | File               | Mục đích                  |
| ------------------- | ------------------ | ------------------------- |
| Face Detection      | `yolov11n-face.pt` | Xác định vị trí khuôn mặt |
| Age Classification  | `age.pt`          | Dự đoán tuổi              |
| Race Classification | `race.pt`          | Dự đoán chủng tộc         |

---

## 🛠 **Cách cài đặt**

### 1. Clone hoặc tải project

```bash
git clone <your-repo-url>
cd project
```

### 2. Cài đặt thư viện

```bash
pip install ultralytics opencv-python
```

*(Nếu bạn dùng GPU thì đảm bảo đã cài CUDA + Torch phù hợp.)*

### 3. Cập nhật đường dẫn model trong `config.py`

```python
model_detect = YOLO(r"\path\to\yolov11n-face.pt")
model_age    = YOLO(r"\path\to\age\age.pt")
model_race   = YOLO(r"\path\to\race\race.pt")
```

---

## ▶️ **Chạy chương trình**

Tại thư mục chính:

```bash
python main.py
```

Nhấn **Q** để thoát chương trình.

---

## 📸 **Cách hoạt động**

### 1. **Capture Thread**

* Lấy frame từ webcam liên tục
* Đưa vào `capture_queue` (kích thước 1)

### 2. **Inference Thread**

* Lấy frame từ capture queue
* Chạy face detection
* Crop từng khuôn mặt
* Chạy age + race classification
* Smoothing kết quả theo history
* Đưa kết quả cuối vào `display_queue`

### 3. **Display Thread**

* Vẽ bounding box & nhãn
* Hiển thị FPS
* Render lên cửa sổ OpenCV


