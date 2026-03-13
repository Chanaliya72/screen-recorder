import cv2
import numpy as np
import mss
import threading
import tkinter as tk
from tkinter import messagebox

# ======================
# SETTINGS
# ======================
FPS = 60
RESOLUTION = (1920, 1080)
OUTPUT_FILE = "screen_recording.mp4"
CODEC = cv2.VideoWriter_fourcc(*"mp4v")

# ======================
# GLOBAL STATES
# ======================
recording = False
paused = False

# ======================
# SCREEN RECORD FUNCTION
# ======================
def record_screen():
    global recording, paused

    sct = mss.mss()
    monitor = sct.monitors[1]

    video_writer = cv2.VideoWriter(
        OUTPUT_FILE,
        CODEC,
        FPS,
        RESOLUTION
    )

    while recording:
        if not paused:
            img = sct.grab(monitor)
            frame = np.array(img)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
            frame = cv2.resize(frame, RESOLUTION)
            video_writer.write(frame)

    video_writer.release()
    print("Recording stopped and saved.")

# ======================
# BUTTON FUNCTIONS
# ======================
def start_recording():
    global recording, paused
    if recording:
        messagebox.showinfo("Info", "Recording already started")
        return

    recording = True
    paused = False
    threading.Thread(target=record_screen, daemon=True).start()
    status_label.config(text="Status: Recording")

def pause_recording():
    global paused
    if not recording:
        return

    paused = not paused
    status_label.config(
        text="Status: Paused" if paused else "Status: Recording"
    )

def stop_recording():
    global recording
    if not recording:
        return

    recording = False
    status_label.config(text="Status: Stopped")
    messagebox.showinfo("Saved", "Recording saved as screen_recording.mp4")

# ======================
# UI SETUP
# ======================
root = tk.Tk()
root.title("Simple Screen Recorder")
root.geometry("300x200")
root.resizable(False, False)

title = tk.Label(root, text="Screen Recorder", font=("Arial", 16))
title.pack(pady=10)

start_btn = tk.Button(root, text="▶ Start", width=15, command=start_recording)
start_btn.pack(pady=5)

pause_btn = tk.Button(root, text="⏸ Pause / Resume", width=15, command=pause_recording)
pause_btn.pack(pady=5)

stop_btn = tk.Button(root, text="⏹ Stop", width=15, command=stop_recording)
stop_btn.pack(pady=5)

status_label = tk.Label(root, text="Status: Idle", fg="blue")
status_label.pack(pady=10)

root.mainloop()
