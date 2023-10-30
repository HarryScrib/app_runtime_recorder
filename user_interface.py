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
from tkinter import *
from tkinter.ttk import *
from datetime import datetime, timedelta

# class Timer:
#     def __init__(self):
#         self.start_time = None
#         self.active_app = None

#     def start_timer(self, app_name):
#         self.active_app = app_name
#         self.start_time = time.time()

#     def stop_timer(self):
#         if self.start_time is not None:
#             elapsed_time = time.time() - self.start_time
#             print(f"Time spent on {self.active_app}: {elapsed_time:.2f} seconds")
#             self.active_app = None

# def update_active_window(timer):
#     while True:
#         active_window = pygetwindow.getWindowsWithTitle(pygetwindow.getActiveWindowTitle())
#         if active_window:
#             app_name = active_window[0].title
#             timer.start_timer(app_name)
#         time.sleep(1)

def format_time(seconds):
    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    if days > 0:
        return f"{days}d {hours:02}:{minutes:02}:{seconds:02}"
    elif hours > 0:
        return f"{hours:02}:{minutes:02}:{seconds:02}"
    else:
        return f"{minutes:02}:{seconds:02}"

def update_progress(completion, max_time, current_time, canvas, bar):
    # Check if the current time is less than the maximum time
    if current_time < max_time:
        current_time += 1
        
        # Calculate the new width of the progress bar based on the length of the bar (200)
        new_width = int(current_time / max_time * 200)
        
        # Update the position of the progress bar
        canvas.coords(bar, 0, 0, new_width, 30)

        colour = get_progress_colour(current_time, max_time)
        canvas.itemconfig(bar, fill=colour)
        
        # Update the completion text
        completion.set(f"{format_time(current_time)} / {format_time(max_time)}")

        # Schedule the next update after 1000 milliseconds (1 second)
        canvas.after(1000, lambda: update_progress(completion, max_time, current_time, canvas, bar))

def progress_start(max_time, completion, canvas, bar):
    current_time = -1
    update_progress(completion, max_time, current_time, canvas, bar)

# Dynamically collect colour value based on current time input
def get_progress_colour(current_time, max_time):
    progress = current_time / max_time
    teal = "#4CC3D9"
    pink = "#FF6B6B"

    # Interpolate between teal and pink based on the progress
    r = int(int(teal[1:3], 16) * (1 - progress) + int(pink[1:3], 16) * progress)
    g = int(int(teal[3:5], 16) * (1 - progress) + int(pink[3:5], 16) * progress)
    b = int(int(teal[5:7], 16) * (1 - progress) + int(pink[5:7], 16) * progress)
    
    # Interpolated colour
    return f"#{r:02X}{g:02X}{b:02X}" 

def create_progress_bar(root, max_time):
    completion = tk.StringVar()
    frame = tk.Frame(root)
    frame.pack(pady=10)

    canvas = tk.Canvas(frame, width=200, height=30, bg="white", highlightthickness=0)
    canvas.pack()

    bar = canvas.create_rectangle(0, 0, 0, 30, fill="red", width=2)
    border = canvas.create_rectangle(0, 0, 200, 30, outline="black", width=2)
    completion_label = tk.Label(root, textvariable=completion, font=("Tahoma", 12))
    completion_label.pack()
    button = tk.Button(root, text="Start Timer", command=lambda: progress_start(max_time, completion, canvas, bar))
    button.pack()

    return completion

class CustomDropdownMenu:
    def __init__(self, parent, options, default_option, on_change_callback):
        self.parent = parent
        self.options = options
        self.selected_option = tk.StringVar()
        self.selected_option.set(default_option)
        self.on_change_callback = on_change_callback

        self.create_dropdown_menu()

    def create_dropdown_menu(self):
        dropdown = tk.OptionMenu(self.parent, self.selected_option, *self.options)
        dropdown.pack()

        def on_option_change(*args):
            selected_option_value = self.selected_option.get()
            self.on_change_callback(selected_option_value)

        self.selected_option.trace("w", on_option_change)

def option_changed(selected_option):
    print("Selected Option:", selected_option)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Application Time Tracker")
    root.geometry("750x400")

    max_time_1 = 60  # Set the max_time for the first progress bar
    percent_1 = create_progress_bar(root, max_time_1)

    max_time_2 = 30  # Set the max_time for the second progress bar
    percent_2 = create_progress_bar(root, max_time_2)

    applications_opened = ["Google Chrome", "Discord", "Diablo II: Lord of Destruction"]
    default_option = applications_opened[0]

    applications_dropdown = CustomDropdownMenu(root, applications_opened, default_option, option_changed)

    root.mainloop()

# root = tk.Tk()
# root.title("Application Time Tracker")
# root.geometry("400x300")

# frame = tk.Frame(root)
# frame.pack(pady=10)

# canvas = tk.Canvas(frame, width=200, height=30, bg="white", highlightthickness=0)
# canvas.pack()

# custom_style = {
#     "bg": "lightblue",
#     "font": ("Tahoma", 12),
#     "relief": "flat",
# }

# #test button
# button = tk.Button(root, text="Testing Out Some Buttons")
# button.pack()

# #custom style test button
# button = tk.Button(root, text="Custom Style Test", **custom_style)
# button.pack(pady=20)

# #breeze button
# button = tk.Button(root, text="Does This Look Like Breeze", command=lambda: print("CLICK"))
# button.pack(padx=15, pady=15)

# completion = tk.StringVar()

# # canvas.configure("Custom.Horizontal.TProgressbar", thickness=230)

# bar = canvas.create_rectangle(0, 0, 0, 30, fill="blue")
# #tk.Progressbar(root, orient=tk.HORIZONTAL, length=200, mode="determinate", style="Custom.Horizontal.TProgressbar")
# # bar.pack(pady=10)

# completion_label = tk.Label(root, textvariable=completion, font=("Tahoma", 12))
# completion_label.pack()

# max_time = 185
# current_time = -1

# # completion_label["style"] = "CustomProgressLabel.TLabel"

# button = tk.Button(root, text="progress test", command=progress_start)
# button.pack()

# timer = Timer()

# root.wm_attributes("-topmost", 1)

# # Create and place UI components
# app_label = tk.Label(root, text="Active Application:")
# app_label.pack()

# time_label = tk.Label(root, text="")
# time_label.pack()

# # Start the window monitoring thread
# monitor_thread = threading.Thread(target=update_active_window, args=(timer,))
# monitor_thread.start()

# def toggle_lock():
#     if lock_button.cget("text") == "Lock":
#         lock_button.config(text="Unlock")
#         root.overrideredirect(True)
#     else:
#         lock_button.config(text="Lock")
#         root.overrideredirect(False)

# lock_button = tk.Button(root, text="Lock", command=toggle_lock)
# lock_button.pack()

# # def start():
    
# #    w.start()

# # def stopfunc():
# #     w.stop()
# #     #var.set(var.get())

# # def reset():
# #     var.set(0)

# # window = Tk()

# # var = IntVar()

# # w = ttk.Progressbar(window, variable=var)
# # w.pack()
# # button1 = ttk.Button(window, text = 'start', command = start)
# # button1.pack()
# # button2 = ttk.Button(window, text = 'stop', command = stopfunc)
# # button2.pack()

# # button2 = ttk.Button(window, text = 'reset', command = reset)
# # button2.pack()