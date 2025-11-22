import tkinter as tk
from tkinter import ttk


class BasicTab:
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
        # Color mode section
        self.create_section("🎨 Chế độ màu")

        color_frame = tk.Frame(
            self.scrollable_frame, bg='white', relief='solid', bd=1
        )
        color_frame.pack(fill='x', padx=10, pady=5)

        tk.Radiobutton(
            color_frame, text="⚫ Đen trắng",
            variable=self.app.color_mode,
            value="grayscale", font=('Arial', 10), bg='white',
            command=self.app.on_color_mode_change
        ).pack(anchor='w', padx=10, pady=5)

        tk.Radiobutton(
            color_frame, text="🌈 Màu sắc",
            variable=self.app.color_mode,
            value="color", font=('Arial', 10), bg='white',
            command=self.app.on_color_mode_change
        ).pack(anchor='w', padx=10, pady=5)

        # Draw mode section
        self.create_section("✏️ Chế độ vẽ")

        mode_frame = tk.Frame(
            self.scrollable_frame, bg='white', relief='solid', bd=1
        )
        mode_frame.pack(fill='x', padx=10, pady=5)

        tk.Radiobutton(
            mode_frame, text="📐 Chỉ viền",
            variable=self.app.draw_mode,
            value="outline", font=('Arial', 10), bg='white'
        ).pack(anchor='w', padx=10, pady=3)

        tk.Radiobutton(
            mode_frame, text="🖌️ Fill đầy",
            variable=self.app.draw_mode,
            value="fill", font=('Arial', 10), bg='white'
        ).pack(anchor='w', padx=10, pady=3)

        tk.Radiobutton(
            mode_frame, text="🎯 Smart",
            variable=self.app.draw_mode,
            value="smart", font=('Arial', 10), bg='white'
        ).pack(anchor='w', padx=10, pady=3)

        # Edge thickness
        thick_frame = tk.Frame(mode_frame, bg='white')
        thick_frame.pack(fill='x', padx=10, pady=5)

        tk.Label(
            thick_frame, text="Độ dày viền:", font=('Arial', 9),
            bg='white'
        ).pack(side='left')

        tk.Scale(
            thick_frame, from_=1, to=5, resolution=1,
            orient='horizontal', variable=self.app.edge_thickness,
            length=150, bg='white', highlightthickness=0
        ).pack(side='left', padx=5)

        # Speed section
        self.create_section("⚡ Tốc độ và mật độ")

        speed_frame = tk.Frame(
            self.scrollable_frame, bg='white', relief='solid', bd=1
        )
        speed_frame.pack(fill='x', padx=10, pady=5)

        # Speed control
        speed_ctrl = tk.Frame(speed_frame, bg='white')
        speed_ctrl.pack(fill='x', padx=10, pady=5)

        tk.Label(
            speed_ctrl, text="Tốc độ (s):", font=('Arial', 9),
            bg='white', width=12, anchor='w'
        ).pack(side='left')

        tk.Scale(
            speed_ctrl, from_=0.0001, to=0.05, resolution=0.0001,
            orient='horizontal', variable=self.app.speed, length=180,
            bg='white', highlightthickness=0
        ).pack(side='left', padx=5)

        self.app.speed_label = tk.Label(
            speed_ctrl, text="0.001s",
            font=('Arial', 9, 'bold'), bg='white'
        )
        self.app.speed_label.pack(side='left')
        self.app.speed.trace('w', self.app.update_speed_label)

        # Density control
        density_ctrl = tk.Frame(speed_frame, bg='white')
        density_ctrl.pack(fill='x', padx=10, pady=5)

        tk.Label(
            density_ctrl, text="Mật độ:", font=('Arial', 9),
            bg='white', width=12, anchor='w'
        ).pack(side='left')

        tk.Scale(
            density_ctrl, from_=0.1, to=1.0, resolution=0.1,
            orient='horizontal', variable=self.app.point_density, length=180,
            bg='white', highlightthickness=0
        ).pack(side='left', padx=5)

        # Options
        tk.Checkbutton(
            speed_frame, text="⚡ Chế độ siêu tốc",
            variable=self.app.fast_mode,
            font=('Arial', 10, 'bold'), fg='red',
            bg='white'
        ).pack(anchor='w', padx=10, pady=5)

        tk.Checkbutton(
            speed_frame, text="📏 Giữ tỷ lệ ảnh",
            variable=self.app.keep_aspect_ratio,
            font=('Arial', 10, 'bold'), fg='blue',
            bg='white'
        ).pack(anchor='w', padx=10, pady=5)

    def create_section(self, title):
        tk.Label(
            self.scrollable_frame, text=title, font=('Arial', 10, 'bold'),
            bg='#f5f5f5', fg='#333333', anchor='w'
        ).pack(fill='x', padx=10, pady=(10, 5))

    def get_frame(self):
        return self.frame
