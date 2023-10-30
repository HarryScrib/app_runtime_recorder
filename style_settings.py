import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk, ThemedStyle

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

root.wm_attributes("-topmost", 1)

# Create and place UI components
app_label = tk.Label(root, text="Active Application:")
app_label.pack()

time_label = tk.Label(root, text="")
time_label.pack()


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