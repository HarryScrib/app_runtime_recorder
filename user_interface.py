import tkinter as tk
from tkinter import ttk
import win32gui
import psutil
import os
import win32process

class Settings:
    def __init__(self, settings_frame):
        self.settings_frame = settings_frame

        # Create the settings page in the provided settings_frame
        self.notebook = ttk.Notebook(self.settings_frame)
        self.notebook.pack(fill="both", expand=True)

        # Add settings widgets to the settings page
        self.create_settings_widgets()

    def create_settings_widgets(self):
        # Add settings widgets here
        label = ttk.Label(self.notebook, text="Settings:")
        label.grid(row=0, column=0, padx=10, pady=10)

        checkbox = ttk.Checkbutton(self.notebook, text="Option 1")
        checkbox.grid(row=1, column=0, padx=10, pady=5)

        entry = ttk.Entry(self.notebook)
        entry.grid(row=2, column=0, padx=10, pady=5)

        button = ttk.Button(self.notebook, text="Save")
        button.grid(row=3, column=0, padx=10, pady=10)

class CustomProgressBar:
    def __init__(self, root, max_time):
        self.root = root
        self.max_time = max_time
        self.current_time = 0

        # Create a variable to hold completion text
        self.completion = tk.StringVar()
        self.create_progress_bar()
        self.visible = False # Initially, the progress bar is hidden

    # Create the UI elements for the progress bar
    def create_progress_bar(self):
        # Initialise the canvas for the progress bar
        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        self.canvas = tk.Canvas(frame, width=200, height=30, bg="white", highlightthickness=0)
        self.canvas.pack()

        # Create a rectangle to represent the progress bar
        self.bar = self.canvas.create_rectangle(0, 0, 0, 30, fill="red", width=2)
        border = self.canvas.create_rectangle(0, 0, 200, 30, outline="black", width=2)

        # Create a label for completion text
        completion_label = tk.Label(self.root, textvariable=self.completion, font=("Tahoma", 12))
        completion_label.pack()

        # Create a button to start the timer
        button = tk.Button(self.root, text="Start Timer", command=self.progress_start)
        button.pack()

    def update_max_time(self, max_time):
        self.max_time = max_time

    def hide(self):
        self.visible = False

    # Format the time in days, hours, minutes, and seconds
    def format_time(self, seconds):
        days, seconds = divmod(seconds, 86400)
        hours, seconds = divmod(seconds, 3600)
        minutes, seconds = divmod(seconds, 60)
        if days > 0:
            return f"{days}d {hours:02}:{minutes:02}:{seconds:02}"
        elif hours > 0:
            return f"{hours:02}:{minutes:02}:{seconds:02}"
        else:
            return f"{minutes:02}:{seconds:02}"

    # Update the progress of the bar and change its colour based on time
    def update_progress(self):
        if self.current_time < self.max_time:
            self.current_time += 1
            new_width = int(self.current_time / self.max_time * 200)
            self.canvas.coords(self.bar, 0, 0, new_width, 30)
            colour = self.get_progress_colour(self.current_time, self.max_time)
            self.canvas.itemconfig(self.bar, fill=colour)
            self.completion.set(f"{self.format_time(self.current_time)} / {self.format_time(self.max_time)}")
            self.root.after(1000, self.update_progress)

    def progress_start(self):
        self.current_time = -1
        self.update_progress()
        self.visible = True # Show the progress bar.

    # Calculate and return a colour based on the progress
    def get_progress_colour(self, current_time, max_time):
        progress = current_time / max_time
        teal = "#4CC3D9"
        pink = "#FF6B6B"
        r = int(int(teal[1:3], 16) * (1 - progress) + int(pink[1:3], 16) * progress)
        g = int(int(teal[3:5], 16) * (1 - progress) + int(pink[3:5], 16) * progress)
        b = int(int(teal[5:7], 16) * (1 - progress) + int(pink[5:7], 16) * progress)
        return f"#{r:02X}{g:02X}{b:02X}"

class CustomDropdownMenu:
    def __init__(self, parent, options, default_option, on_change_callback):
        self.parent = parent
        self.options = options
        self.selected_option = tk.StringVar()
        self.selected_option.set(default_option)
        self.on_change_callback = on_change_callback

        self.create_dropdown_menu()

    def create_dropdown_menu(self):
        dropdown = ttk.Combobox(self.parent, self.selected_option, *self.options)
        dropdown.pack()

        # Define a callback function for when the dropdown selection changes
        def on_option_change(*args):
            selected_option_value = self.selected_option.get()
            self.on_change_callback(selected_option_value)

        # Attach the callback to the selected_option variable to trigger when it changes
        self.selected_option.trace("w", self.on_option_change)

    def on_option_change(self, *args):
        # Callback function triggered when the drop selection changes
        selected_option_value = self.selected_option.get()
        # Update the progress bars with the new max_time based on the selected option
        self.update_progress_bars(int(selected_option_value))

    def update_progress_bars(self, max_time):
        # Iterate through each progress bar and update their max_time
        for progress_bar in self.progress_bars:
            progress_bar.update_max_time(max_time)
            progress_bar.progress_start()

class ApplicationMonitor:
    def __init__(self, root):
        self.root = root
        self.root.title("Interactive Executables Monitor")
        self.known_apps = set()
        self.dropdown = ttk.Combobox(self.root, width=50)
        self.dropdown.pack(padx=10, pady=10)

    def get_active_applications(self):
        active_apps = set()
        hwnds = []
        win32gui.EnumWindows(lambda hwnd, param: param.append(hwnd), hwnds)

        for hwnd in hwnds:
            if win32gui.IsWindowVisible(hwnd):
                app_name = self.get_root_app_name(hwnd)
                if app_name:
                    active_apps.add(app_name)

        return active_apps

    def get_root_app_name(self, hwnd):
        try:
            window_text = win32gui.GetWindowText(hwnd)
            root_app_name = window_text.split(" - ")[-1]  # Extract the root application name
            return root_app_name
        except Exception:
            return None

    def update_dropdown(self):
        current_apps = self.get_active_applications()
        self.dropdown["values"] = tuple(current_apps)
        self.root.after(5000, self.update_dropdown)

if __name__ == "__main__":
    root = tk.Tk()
    
    main_frame = ttk.Label(root, text="Main")
    main_frame.pack(padx=10, pady=10)

    settings_frame = ttk.Label(root, text="Settings")
    settings_frame.pack(padx=10, pady=10)

    blacklist_frame = ttk.Label(root, text="Blacklist")
    blacklist_frame.pack(padx=10, pady=10)
    
    app_settings = Settings(root)
    root.title("Application Monitor")
    root.geometry("1000x500")


    
    app_monitor = ApplicationMonitor(root)
    app_monitor.update_dropdown()
    
    root.mainloop()