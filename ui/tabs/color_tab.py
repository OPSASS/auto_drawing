import tkinter as tk
from tkinter import ttk
from ui.components.step_manager import StepManager


class ColorTab:
    def __init__(self, parent, app):
        self.app = app
        self.frame = tk.Frame(parent, bg='#f5f5f5')

        # Canvas with scrollbar
        self.canvas = tk.Canvas(self.frame, bg='#f5f5f5', highlightthickness=0)
        scrollbar = ttk.Scrollbar(
            self.frame, orient="vertical", command=self.canvas.yview
        )
        self.scrollable_frame = tk.Frame(self.canvas, bg='#f5f5f5')

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window(
            (0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.setup_ui()

    def setup_ui(self):
        # Palette type
        self.create_section("🎨 Loại bảng màu")

        type_frame = tk.Frame(
            self.scrollable_frame, bg='white', relief='solid', bd=1
        )
        type_frame.pack(fill='x', padx=10, pady=5)

        tk.Radiobutton(
            type_frame, text="📋 Có bước mở/đóng + Vùng màu",
            variable=self.app.palette_type, value="type1",
            font=('Arial', 10), bg='white',
            command=self.app.on_palette_type_change
        ).pack(anchor='w', padx=10, pady=5)

        tk.Radiobutton(
            type_frame, text="🎯 Chỉ vùng màu",
            variable=self.app.palette_type, value="type2",
            font=('Arial', 10), bg='white',
            command=self.app.on_palette_type_change
        ).pack(anchor='w', padx=10, pady=5)

        # Number of colors
        num_frame = tk.Frame(type_frame, bg='white')
        num_frame.pack(fill='x', padx=10, pady=5)

        tk.Label(
            num_frame, text="Số màu:", font=('Arial', 9),
            bg='white'
        ).pack(side='left')

        tk.Scale(
            num_frame, from_=3, to=64, resolution=1,
            orient='horizontal', variable=self.app.num_colors,
            length=200, bg='white', highlightthickness=0
        ).pack(side='left', padx=5)

        # Action buttons
        btn_frame = tk.Frame(type_frame, bg='white')
        btn_frame.pack(fill='x', padx=10, pady=10)

        tk.Button(
            btn_frame, text="📍 Chọn vùng bảng màu",
            command=self.app.select_palette_area,
            bg='#673AB7', fg='white', font=('Arial', 9, 'bold'),
            relief='flat', cursor='hand2', padx=10, pady=5
        ).pack(side='left', padx=5)

        tk.Button(
            btn_frame, text="🔍 Phân tích màu",
            command=self.app.analyze_colors,
            bg='#3F51B5', fg='white', font=('Arial', 9, 'bold'),
            relief='flat', cursor='hand2', padx=10, pady=5
        ).pack(side='left', padx=5)

        # Color preview
        self.create_section("🎨 Màu đã phân tích")

        self.app.color_display_frame = tk.Frame(
            self.scrollable_frame, bg='white',
            relief='solid', bd=1
        )
        self.app.color_display_frame.pack(fill='x', padx=10, pady=5)

        tk.Label(
            self.app.color_display_frame, text="Chưa phân tích màu",
            font=('Arial', 9), fg='#888888', bg='white'
        ).pack(pady=10)

        # Open palette steps
        self.create_section("🔓 MỞ bảng màu")
        self.app.open_steps_container = tk.Frame(
            self.scrollable_frame, bg='#f5f5f5'
        )
        self.app.open_steps_container.pack(fill='x', padx=10, pady=5)

        self.app.open_palette_steps = StepManager(
            self.app.open_steps_container, self.app
        )
        self.app.open_palette_steps.pack(fill='both', expand=True)

        # Close palette steps
        self.create_section("🔒 ĐÓNG bảng màu (tùy chọn)")
        self.app.close_steps_container = tk.Frame(
            self.scrollable_frame, bg='#f5f5f5'
        )
        self.app.close_steps_container.pack(fill='x', padx=10, pady=5)

        self.app.close_palette_steps = StepManager(
            self.app.close_steps_container, self.app
        )
        self.app.close_palette_steps.pack(fill='both', expand=True)

    def create_section(self, title):
        tk.Label(
            self.scrollable_frame, text=title, font=('Arial', 10, 'bold'),
            bg='#f5f5f5', fg='#333333', anchor='w'
        ).pack(fill='x', padx=10, pady=(10, 5))

    def get_frame(self):
        return self.frame
