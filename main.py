import tkinter as tk
from tkinter import ttk
import win32gui
from tkinter import font

class FontManager:
    def __init__(self):
        self.default_font = font.nametofont("TkDefaultFont")
        self.label_font = font.nametofont("TkDefaultFont")
        self.heading_font = font.nametofont("TkDefaultFont")

        # Set button font settings
        self.button_font = font.nametofont("TkDefaultFont")
        self.button_font.configure(size=8, family="Verdana")

    def label(self, parent, text, size=12):
        self.label_font.configure(size=size)
        return tk.Label(font=self.label_font, text=text)

    def heading(self, parent, text, size=16, weight="bold"):
        self.heading_font.configure(size=size, weight=weight)
        return tk.Label(font=self.heading_font, text=text)

    def button(self, parent, text, font_color="white"):
        button = tk.Button(parent, text=text, font=self.button_font, foreground=font_color)
        button.configure(bg="#444444", borderwidth=2, relief="raised", activebackground="#666666", activeforeground="white")
        return button

class ApplicationInterface:
    def __init__(self, root):
        self.root = root
        self.font_manager = FontManager()
        self.root.title("Application Monitor")

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)

        self.create_main_tab()
        self.create_settings_tab()
        self.create_blacklist_tab()

        self.blacklist_items = set()

    def create_main_tab(self):
        main_tab = tk.Frame(self.notebook, relief="solid", borderwidth=1, bg="#444444")
        self.notebook.add(main_tab, text="Main")

        main_label = tk.Label(main_tab, text="Select a Program")
        main_label.pack(padx=10, pady=10)

        self.main_combobox = ttk.Combobox(main_tab, width=50)
        self.main_combobox.pack(padx=10, pady=10)

    def create_settings_tab(self):
        settings_tab = tk.Frame(self.notebook, relief="solid", borderwidth=1, bg="#444444")
        self.notebook.add(settings_tab, text="Settings")

        settings_label = tk.Label(settings_tab, text="Settings")
        settings_label.grid(row=0, column=0, padx=10, pady=10)

        checkbox = ttk.Checkbutton(settings_tab, text="Option 1", onvalue=True, offvalue=False)
        checkbox.grid(row=1, column=0, padx=10, pady=5)

        # Set the initial state to unchecked
        checkbox.state(['!alternate'])

        entry = ttk.Entry(settings_tab)
        entry.grid(row=2, column=0, padx=10, pady=5)

        button = self.font_manager.button(settings_tab, text="Save")
        button.grid(row=3, column=0, padx=10, pady=10)

    def create_blacklist_tab(self):
        blacklist_tab = tk.Frame(self.notebook, relief="solid", borderwidth=1, bg="#444444")
        self.notebook.add(blacklist_tab, text="Blacklist")

        blacklist_label = tk.Label(blacklist_tab, text="Blacklist")
        blacklist_label.pack(padx=10, pady=10)

        self.blacklist_combobox = ttk.Combobox(blacklist_tab, width=50)
        self.blacklist_combobox.pack(padx=10, pady=10)

        move_to_empty_button = self.font_manager.button(blacklist_tab, text="Move to Blacklist")
        move_to_empty_button["command"] =self.move_to_empty
        move_to_empty_button.pack(pady=10)

        self.empty_listbox = tk.Listbox(blacklist_tab, width=50)
        self.empty_listbox.pack(padx=10, pady=10)
        
        undo_button = self.font_manager.button(blacklist_tab, text="Remove From Blacklist")
        undo_button["command"] = self.undo_move
        undo_button.pack(padx=10, pady=10)

    def move_to_empty(self):
        selected_item = self.blacklist_combobox.get()
        if selected_item:
            ui_functions.add_to_blacklist(selected_item)
            self.empty_listbox.insert(tk.END, selected_item)  # Add to the Listbox
            self.blacklist_combobox.set('')

    def undo_move(self):
        selected_item = self.empty_listbox.curselection()
        if selected_item:
            item_index = selected_item[0]
            app_name = self.empty_listbox.get(item_index)  # Get the app_name from the Listbox
            self.empty_listbox.delete(item_index)
            ui_functions.restore_from_blacklist(app_name)

    def update_combobox(self):
        # Implement the update logic for main_combobox here
        active_apps = ui_functions.update() 
        self.blacklist_combobox["values"] = tuple(active_apps)
        self.main_combobox["values"] = tuple(active_apps)
        self.root.after(1000, self.update_combobox)

class ApplicationInformation:
    def __init__(self, information_frame):
        self.information_frame = information_frame
        self.font_manager = FontManager()
        # Create a separator label with a custom background color
        self.create_separator()

        # Create the settings page in the provided information_frame
        self.notebook = ttk.Notebook(information_frame)
        self.notebook.pack(fill="both", expand=True)

        # Add settings widgets to the settings page
        self.create_information_widgets()

    def create_information_widgets(self):
        # Add settings widgets here
        label = self.font_manager.button(self.notebook, text="Settings:")
        label.pack(padx=10, pady=10)

        checkbox = ttk.Checkbutton(self.notebook, text="Option 1")
        checkbox.pack(padx=10, pady=10)

        entry = ttk.Entry(self.notebook)
        entry.pack(padx=10, pady=10)

        button = ttk.Button(self.notebook, text="Save")
        button.pack(padx=10, pady=10)

    def create_separator(self):
        # Create a separator label with a custom background color
        separator = tk.Label(self.information_frame, height=2, bg="#555555", text="Application Information", fg="white")
        separator.pack(fill="x")

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

class InterfaceFunctionality:
    def __init__(self):
        self.known_apps = {'popdown'}
        self.update_interval = 1 # Update interval in seconds

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

    def add_to_blacklist(self, app_name):
        self.known_apps.add(app_name)

    def restore_from_blacklist(self, app_name):
        self.known_apps.discard(app_name)

    def get_blacklisted_apps(self):
        return self.known_apps

    def update(self):
        current_apps = self.get_active_applications()
        blacklisted_apps = self.known_apps.copy()
        current_apps -= blacklisted_apps
        return current_apps

if __name__ == "__main__":
    root = tk.Tk()
    app_interface = ApplicationInterface(root)
    ui_functions = InterfaceFunctionality()    
    information_frame = ApplicationInformation(root)
    #app_settings = Settings(root)
    root.geometry("500x500")

    app_interface.update_combobox()


    
    root.mainloop()  
