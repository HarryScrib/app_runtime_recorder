import tkinter as tk
import time
import pygetwindow
import psutil
import threading
from tkinter import ttk
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QColor, QPainter
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from ttkthemes import ThemedTk, ThemedStyle

class Timer:
    def __init__(self):
        self.start_time = None
        self.active_app = None

    def start_timer(self, app_name):
        self.active_app = app_name
        self.start_time = time.time()

    def stop_timer(self):
        if self.start_time is not None:
            elapsed_time = time.time() - self.start_time
            print(f"Time spent on {self.active_app}: {elapsed_time:.2f} seconds")
            self.active_app = None

def update_active_window(timer):
    while True:
        active_window = pygetwindow.getWindowsWithTitle(pygetwindow.getActiveWindowTitle())
        if active_window:
            app_name = active_window[0].title
            timer.start_timer(app_name)
        time.sleep(1)

root = tk.Tk()
root.title("Application Time Tracker")

custom_style = {
    "bg": "lightgray",
    "font": ("Tahoma", 12),
    "relief": "flat",
}

style = ThemedStyle(root)
style.set_theme("breeze")

button = ttk.Button(root, text="Testing Out Some Buttons")
button.pack()

button = tk.Button(root, text="Custom Style Test", **custom_style)
button.pack()

timer = Timer()

root.wm_attributes("-topmost", 1)

# Create and place UI components
app_label = tk.Label(root, text="Active Application:")
app_label.pack()

time_label = tk.Label(root, text="")
time_label.pack()

# Start the window monitoring thread
monitor_thread = threading.Thread(target=update_active_window, args=(timer,))
monitor_thread.start()

def toggle_lock():
    if lock_button.cget("text") == "Lock":
        lock_button.config(text="Unlock")
        root.overrideredirect(True)
    else:
        lock_button.config(text="Lock")
        root.overrideredirect(False)

lock_button = tk.Button(root, text="Lock", command=toggle_lock)
lock_button.pack()

root.mainloop()