# 🎥 webcam_scare — Advanced Auto‑Capture Webcam Recorder

---

# 🛰️ **⭐ FEATURES | ویژگی‌ها**

### **English**

* Automatically captures **photo, video, and audio**.
* Starts recording immediately when webcam is available.
* Stops recording **automatically** once webcam disconnects.
* Saves all files with **timestamp-based names**.
* Multithreaded audio recording for stable performance.
* Uses OpenCV, PyAudio, and Wave libraries.

### **فارسی**

* ثبت خودکار **عکس، ویدیو و صدا** به‌محض اتصال وبکم.
* توقف خودکار ضبط هنگام **قطع شدن وبکم**.
* ذخیره تمام خروجی‌ها با نام‌گذاری زمان‌دار.
* ضبط صدا با استفاده از چندریسمانی (Threading).
* استفاده از کتابخانه‌های OpenCV، PyAudio و Wave.

---

# 📂 PROJECT STRUCTURE | ساختار پروژه

```
webcam_scare/
│
├── webcam_scare.py        # برنامه اصلی
├── photo_YYYYMMDD.jpg     # عکس ذخیره‌شده
├── video_YYYYMMDD.avi     # ویدیو ضبط‌شده
└── audio_YYYYMMDD.wav     # صدا ضبط‌شده
```

---

# 🔧 REQUIREMENTS | پیش‌نیازها

### Python 3.8+

Install required libraries:

```
pip install opencv-python pyaudio
```

*(کتابخانه‌های wave و datetime داخلی هستند)*

---

# 🎛️ USAGE — webcam_scare

### ⬛ اجرای برنامه

```
python webcam_scare.py
```

Program will:

1. Capture a photo.
2. Start video recording.
3. Start audio recording on separate thread.
4. Stop automatically when webcam disconnects.

---

# 📌 HOW IT WORKS | توضیح عملکرد

### English

* Opens the webcam using OpenCV.
* Captures a single photo.
* Initializes AVI video recording at 640×480.
* Starts a background thread that records audio continuously.
* Enters a loop recording video frames.
* If webcam stops providing frames → program ends and saves outputs.

### فارسی

* وبکم با OpenCV باز می‌شود.
* یک عکس فوری گرفته می‌شود.
* ضبط ویدیو با رزولوشن 480×640 شروع می‌شود.
* یک ترد پس‌زمینه صدا را به‌صورت پیوسته ضبط می‌کند.
* حلقه اصلی تا زمانی که تصویر دریافت شود ادامه دارد.
* در صورت قطع وبکم → تمام فایل‌ها ذخیره شده و برنامه پایان می‌یابد.

---

# 💻 FULL SOURCE CODE | کد کامل برنامه

```python
import cv2
import pyaudio
import wave
import threading
from datetime import datetime

# ---------- فایل‌ها ----------
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
photo_name = f"photo_{timestamp}.jpg"
video_name = f"video_{timestamp}.avi"
audio_name = f"audio_{timestamp}.wav"

# ---------- تنظیمات ویدیو ----------
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(3, 640)
cap.set(4, 480)

# چند فریم اول برای تثبیت تصویر
for _ in range(8):
    cap.read()

# گرفتن عکس
ret, frame = cap.read()
if ret:
    cv2.imwrite(photo_name, frame)
    print("Photo saved:", photo_name)
else:
    print("Error taking photo")

# ---------- ضبط ویدیو ----------
fourcc = cv2.VideoWriter_fourcc(*"MJPG")
out = cv2.VideoWriter(video_name, fourcc, 20.0, (640, 480))

# ---------- ضبط صدا ----------
audio_running = True
p = pyaudio.PyAudio()
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

def record_audio():
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    frames = []
    while audio_running:
        try:
            data = stream.read(CHUNK)
            frames.append(data)
        except:
            continue
    stream.stop_stream()
    stream.close()
    wf = wave.open(audio_name, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

audio_thread = threading.Thread(target=record_audio)
audio_thread.start()

print("Recording started... Program will stop automatically when webcam is disconnected.")

# ---------- حلقه ضبط خودکار ----------
while True:
    ret, frame = cap.read()
    if not ret:
        print("\nWebcam disconnected or unavailable. Stopping recording...")
        break
    out.write(frame)

# ---------- پایان ضبط ----------
audio_running = False
audio_thread.join()
cap.release()
out.release()
p.terminate()

print("Video saved:", video_name)
print("Audio saved:", audio_name)
print("Done.")
```

---

# ⚠️ LIMITATIONS | محدودیت‌ها

* Works only when a webcam is available.
* Audio recording depends on system microphone permissions.
* High‑quality video may require stronger hardware.
* Webcam disconnect ends the program immediately.

---

# 🔒 SECURITY WARNING | هشدار امنیتی

### English

This tool is for **educational and recording purposes only**. Do not use it to record others without permission.

### فارسی

این ابزار فقط برای **آموزش و رکورد شخصی** ساخته شده است. ضبط افراد بدون اجازه آن‌ها غیرقانونی است.

---

# 🧩 ROADMAP / TODO | نقشه راه

* [ ] Add GUI panel
* [ ] Add motion detection trigger
* [ ] Add notification alerts
* [ ] Add microphone noise filtering
* [ ] Add auto‑upload feature

---

# 📜 LICENSE | لایسنس

Released under MIT License.
این پروژه تحت لایسنس MIT منتشر شده است.

```
MIT License

Copyright (c) 2025 Mahdi
```

---

# 🖤 Thanks for using webcam_scare

A fully automated multi‑capture webcam recorder.

