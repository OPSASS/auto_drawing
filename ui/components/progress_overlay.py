import tkinter as tk
from tkinter import ttk
from utils.helpers import format_time


class ProgressOverlay(tk.Toplevel):
    def __init__(self, parent, title=""):
        super().__init__(parent)
        self.parent = parent

        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.attributes("-alpha", 0.9)
        self.config(bg="#1e1e1e")

        screen_width = self.winfo_screenwidth()
        self.geometry(f"350x200+{screen_width - 360}+10")

        self._setup_ui(title)

    def _setup_ui(self, title):
        # Title
        self.title_label = tk.Label(
            self, text=title, fg="white", bg="#1e1e1e",
            font=("Arial", 12, "bold")
        )
        self.title_label.pack(pady=(10, 5))

        # Color info
        self.color_frame = tk.Frame(self, bg="#1e1e1e")
        self.color_frame.pack(pady=5)

        self.color_indicator = tk.Label(
            self.color_frame, text="  ", bg="gray", width=4, height=2,
            relief='raised', bd=2
        )
        self.color_indicator.pack(side='left', padx=5)

        self.color_label = tk.Label(
            self.color_frame, text="Màu: Đen/trắng", fg="white",
            bg="#1e1e1e", font=("Arial", 10)
        )
        self.color_label.pack(side='left')

        # Status
        self.status_label = tk.Label(
            self, text="Chưa bắt đầu", fg="#00ff00", bg="#1e1e1e",
            font=("Arial", 10, "bold")
        )
        self.status_label.pack(pady=5)

        # Countdown
        self.countdown_label = tk.Label(
            self, text="⏰ Hoàn thành: --:--:--",
            fg="#00ff88", bg="#1e1e1e", font=("Arial", 10, "bold")
        )
        self.countdown_label.pack(pady=5)

        # Shortcuts
        self.shortcuts_label = tk.Label(
            self, text="F5: Tạm dừng / Tiếp tục, F6: Kết thúc, F7: Mở rộng",
            fg="#888888", bg="#1e1e1e", font=("Arial", 9)
        )
        self.shortcuts_label.pack(pady=5)

        # Progress bar
        self._setup_progressbar()

        # Progress label
        self.progress_label = tk.Label(
            self, text="0%", fg="white", bg="#1e1e1e",
            font=("Arial", 11, "bold")
        )
        self.progress_label.pack(pady=5)

    def _setup_progressbar(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure(
            "Custom.Horizontal.TProgressbar",
            troughcolor='#2d2d2d',
            background='#00ff88',
            bordercolor='#1e1e1e',
            lightcolor='#00ff88',
            darkcolor='#00ff88'
        )

        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            self, length=320, mode='determinate',
            variable=self.progress_var,
            style="Custom.Horizontal.TProgressbar"
        )
        self.progress_bar.pack(pady=5)

    def update_progress(self, value):
        self.progress_var.set(value)
        self.progress_label.config(text=f"{value:.1f}%")

    def update_status(self, text, color="#00ff00"):
        self.status_label.config(text=text, fg=color)

    def update_color(self, rgb_color, color_name=""):
        hex_color = f"#{rgb_color[0]:02x}{rgb_color[1]:02x}{rgb_color[2]:02x}"
        self.color_indicator.config(bg=hex_color)
        self.color_label.config(
            text=f"Màu: {color_name if color_name else hex_color}"
        )

    def update_countdown(self, time_remaining):
        time_str = format_time(time_remaining)
        self.countdown_label.config(text=f"⏰ Hoàn thành: {time_str}")
