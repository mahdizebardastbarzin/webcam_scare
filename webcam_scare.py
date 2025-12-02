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
