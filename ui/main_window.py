import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk
import pyautogui
import keyboard
import threading
from config.settings import *
from config.constants import *
from core.drawing_engine import DrawingEngine
from core.color_analyzer import ColorAnalyzer
from ui.components.selector_dialogs import ScreenSelector
from ui.components.progress_overlay import ProgressOverlay
from ui.tabs.basic_tab import BasicTab
from ui.tabs.color_tab import ColorTab
from ui.tabs.advanced_tab import AdvancedTab


class AutoDrawApp:
    def __init__(self, root):
        self.root = root
        self.root.title(WINDOW_TITLE)
        self.root.geometry(WINDOW_SIZE)
        self.root.configure(bg=WINDOW_BG)
        self.root.bind("<Unmap>", self.on_unmap)

        # Image variables
        self.image = None
        self.color_image = None
        self.display_image = None

        # Drawing variables
        self.drawing_engine = DrawingEngine(self)
        self.target_coords = None
        self.overlay = None
        self.ui_hidden = False

        # Color variables
        self.color_clusters = []
        self.palette_area_coords = None

        # UI Variables
        self.color_mode = tk.StringVar(value=COLOR_MODE_GRAYSCALE)
        self.palette_type = tk.StringVar(value=PALETTE_TYPE_1)
        self.num_colors = tk.IntVar(value=DEFAULT_NUM_COLORS)
        self.speed = tk.DoubleVar(value=DEFAULT_SPEED)
        self.progress = tk.DoubleVar(value=0)
        self.point_density = tk.DoubleVar(value=DEFAULT_POINT_DENSITY)
        self.fast_mode = tk.BooleanVar(value=True)
        self.draw_mode = tk.StringVar(value=DRAW_MODE_OUTLINE)
        self.edge_thickness = tk.IntVar(value=DEFAULT_EDGE_THICKNESS)
        self.keep_aspect_ratio = tk.BooleanVar(value=True)

        self.setup_ui()
        self.setup_hotkeys()

        # PyAutoGUI settings
        pyautogui.FAILSAFE = PYAUTOGUI_FAILSAFE
        pyautogui.PAUSE = PYAUTOGUI_PAUSE

    def setup_ui(self):
        # Main container
        main_container = tk.Frame(self.root, bg=WINDOW_BG)
        main_container.pack(fill='both', expand=True)

        # Left panel
        self.left_panel = tk.Frame(
            main_container, bg='#ffffff',
            relief='solid', borderwidth=1, width=450
        )
        self.left_panel.pack(side='left', fill='both', padx=5, pady=5)
        self.left_panel.pack_propagate(False)

        self.setup_left_panel()

        # Right panel
        right_panel = tk.Frame(
            main_container, bg='#e0e0e0',
            relief='solid', borderwidth=1
        )
        right_panel.pack(side='right', fill='both',
                         expand=True, padx=5, pady=5)

        self.setup_right_panel(right_panel)

    def setup_left_panel(self):
        # Control buttons
        control_frame = tk.Frame(self.left_panel, bg='#ffffff')
        control_frame.pack(fill='x', padx=10, pady=10)

        self.upload_button = tk.Button(
            control_frame, text="📁 Chọn ảnh mẫu",
            command=self.load_image,
            bg=COLOR_PRIMARY, fg='white', font=('Arial', 10, 'bold'),
            relief='flat', cursor='hand2', padx=15, pady=8
        )
        self.upload_button.pack(side='left', padx=3)

        tk.Button(
            control_frame, text="📍 Vùng vẽ",
            command=self.select_drawing_area,
            bg=COLOR_SECONDARY, fg='white', font=('Arial', 10, 'bold'),
            relief='flat', cursor='hand2', padx=15, pady=8
        ).pack(side='left', padx=3)

        # Start/Stop buttons
        btn_frame = tk.Frame(self.left_panel, bg='#ffffff')
        btn_frame.pack(fill='x', padx=10, pady=5)

        self.start_button = tk.Button(
            btn_frame, text="▶ Bắt đầu (F5)",
            command=self.drawing_action,
            bg=COLOR_WARNING, fg='white',
            font=('Arial', 10, 'bold'),
            relief='flat', cursor='hand2',
            padx=12, pady=8
        )
        self.start_button.pack(side='left', padx=3)

        tk.Button(
            btn_frame, text="⏹ Kết thúc (F6)",
            command=self.stop_drawing,
            bg=COLOR_DANGER, fg='white', font=('Arial', 10, 'bold'),
            relief='flat', cursor='hand2', padx=12, pady=8
        ).pack(side='left', padx=3)

        # Status label
        self.status_label = tk.Label(
            self.left_panel, text=STATUS_NO_IMAGE,
            font=('Arial', 10, 'bold'), fg=COLOR_SECONDARY, bg='#ffffff',
            wraplength=400, justify='left'
        )
        self.status_label.pack(pady=5, padx=10)

        # Tabbed interface
        self.notebook = ttk.Notebook(self.left_panel)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=5)

        # Style for tabs
        style = ttk.Style()
        style.configure('TNotebook.Tab', padding=[
                        20, 10], font=('Arial', 9, 'bold'))

        # Create tabs
        self.basic_tab = BasicTab(self.notebook, self)
        self.color_tab = ColorTab(self.notebook, self)
        self.advanced_tab = AdvancedTab(self.notebook, self)

        self.notebook.add(self.basic_tab.get_frame(), text='⚙️ Cơ bản')
        self.notebook.add(self.color_tab.get_frame(), text='🎨 Màu sắc')
        self.notebook.add(self.advanced_tab.get_frame(), text='ℹ️ Nâng cao')

    def setup_right_panel(self, parent):
        # Image info
        info_frame = tk.Frame(parent, bg='#e0e0e0')
        info_frame.pack(fill='x', padx=10, pady=10)

        tk.Label(
            info_frame, text="🖼️ Xem trước ảnh",
            font=('Arial', 12, 'bold'), bg='#e0e0e0'
        ).pack()

        self.coords_label = tk.Label(
            info_frame, text="Vùng vẽ: Chưa chọn",
            font=('Arial', 9), fg='#666666', bg='#e0e0e0'
        )
        self.coords_label.pack(pady=5)

        # Image display
        self.image_frame = tk.Frame(
            parent, bg='#cccccc', relief='sunken', bd=2
        )
        self.image_frame.pack(fill='both', expand=True, padx=10, pady=10)

        self.image_label = tk.Label(
            self.image_frame,
            text="Chưa có ảnh\n\nNhấn 'Tải ảnh' để bắt đầu",
            bg='#cccccc', font=('Arial', 14), fg='#888888'
        )
        self.image_label.pack(fill='both', expand=True)

        # Progress
        progress_frame = tk.Frame(parent, bg='#e0e0e0')
        progress_frame.pack(fill='x', padx=10, pady=5)

        tk.Label(
            progress_frame, text="Tiến độ:", font=('Arial', 10, 'bold'),
            bg='#e0e0e0'
        ).pack(side='left', padx=5)

        self.progress_bar = ttk.Progressbar(
            progress_frame, length=300,
            mode='determinate', variable=self.progress
        )
        self.progress_bar.pack(side='left', padx=5)

        self.progress_label = tk.Label(
            progress_frame, text="0%", font=('Arial', 10, 'bold'), bg='#e0e0e0'
        )
        self.progress_label.pack(side='left', padx=5)

        self.countdown_label = tk.Label(
            progress_frame, text="⏰ --:--:--",
            fg="#006600", font=('Arial', 10, 'bold'), bg='#e0e0e0'
        )
        self.countdown_label.pack(side='left', padx=10)

    def setup_hotkeys(self):
        keyboard.add_hotkey(HOTKEY_PAUSE_RESUME, self.drawing_action)
        keyboard.add_hotkey(HOTKEY_STOP, self.stop_drawing)
        keyboard.add_hotkey(HOTKEY_TOGGLE_OVERLAY, self.toggle_overlay)

    def on_unmap(self, *event):
        if self.root.state() == "iconic":
            if self.drawing_engine.is_paused and not self.ui_hidden:
                self.overlay = ProgressOverlay(
                    self.root, title=self.root.title())
                if self.overlay:
                    self.overlay.update_status("Đang vẽ", "#00ff00")
                self.root.withdraw()
                self.ui_hidden = True

    def toggle_overlay(self):
        if not self.overlay:
            self.overlay = ProgressOverlay(self.root, title=self.root.title())
            self.root.withdraw()
            self.ui_hidden = True
        else:
            self.overlay.destroy()
            self.root.deiconify()
            self.overlay = None
            self.ui_hidden = False

    def update_speed_label(self, *args):
        self.speed_label.config(text=f"{self.speed.get():.4f}s")

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=IMAGE_FILE_TYPES)
        if file_path:
            self.image = Image.open(file_path)
            self.color_image = self.image.convert('RGB')

            # Display image
            self.display_image = self.image.copy()
            self.display_image.thumbnail(
                THUMBNAIL_SIZE, Image.Resampling.LANCZOS)

            photo = ImageTk.PhotoImage(self.display_image)
            self.image_label.config(image=photo, text="")
            self.image_label.image = photo

            self.status_label.config(
                text=STATUS_IMAGE_LOADED.format(
                    self.image.size[0], self.image.size[1]),
                fg='green'
            )
            self.progress.set(0)
            self.progress_label.config(text="0%")
            self.start_button.config(text="▶ Bắt đầu (F5)")

    def select_drawing_area(self):
        if not self.image:
            self.status_label.config(text=STATUS_NO_IMAGE, fg='red')
            return

        self.root.withdraw()

        def on_done(x1, y1, x2, y2):
            self.target_coords = {
                "x1": x1, "y1": y1,
                "x2": x2, "y2": y2,
                "width": x2 - x1,
                "height": y2 - y1
            }

            self.coords_label.config(
                text=f"Vùng vẽ: ({x1}, {y1}) → ({x2}, {y2}) | {x2-x1}x{y2-y1}px"
            )
            self.status_label.config(
                text="✅ Đã chọn vùng vẽ. Nhấn F5 để bắt đầu.", fg='green'
            )
            self.root.deiconify()

        ScreenSelector(on_done, "Chọn vùng vẽ ảnh")

    def select_palette_area(self):
        self.root.withdraw()

        def on_done(x1, y1, x2, y2):
            self.palette_area_coords = {
                "x1": x1, "y1": y1,
                "x2": x2, "y2": y2,
                "width": x2 - x1,
                "height": y2 - y1
            }
            self.status_label.config(
                text=f"✅ Đã chọn vùng bảng màu: {x2-x1}x{y2-y1}px", fg='green'
            )
            self.root.deiconify()

        ScreenSelector(on_done, "Chọn vùng bảng màu")

    def analyze_colors(self):
        if not self.color_image:
            self.status_label.config(text=STATUS_NO_IMAGE, fg='red')
            return

        self.status_label.config(text="🔄 Đang phân tích màu...", fg='orange')

        self.color_clusters = ColorAnalyzer.analyze_colors(
            self.color_image, self.num_colors.get()
        )

        self.display_colors()

        self.status_label.config(
            text=f"✅ Đã phân tích {len(self.color_clusters)} màu", fg='green'
        )

    def display_colors(self):
        for widget in self.color_display_frame.winfo_children():
            widget.destroy()

        colors_container = tk.Frame(self.color_display_frame, bg='white')
        colors_container.pack(pady=10, padx=10)

        for i, color in enumerate(self.color_clusters):
            from utils.helpers import rgb_to_hex
            hex_color = rgb_to_hex(color)

            color_frame = tk.Frame(colors_container, bg='white')
            color_frame.pack(side='left', padx=3)

            color_box = tk.Label(
                color_frame, text=f"{i+1}",
                bg=hex_color, width=4, height=2,
                relief='raised', borderwidth=2,
                font=('Arial', 10, 'bold'),
                fg='white' if sum(color) < 384 else 'black'
            )
            color_box.pack()

            tk.Label(
                color_frame, text=hex_color[:7],
                font=('Arial', 7), bg='white'
            ).pack()

    def on_color_mode_change(self):
        if self.color_mode.get() == COLOR_MODE_COLOR:
            self.notebook.select(1)
            self.status_label.config(
                text="Chế độ màu: Cần thiết lập bảng màu", fg='orange'
            )
        else:
            self.status_label.config(text="Chế độ đen trắng", fg='blue')

    def on_palette_type_change(self):
        if self.palette_type.get() == PALETTE_TYPE_1:
            self.open_steps_container.pack(fill='x', padx=10, pady=5)
            self.close_steps_container.pack(fill='x', padx=10, pady=5)
        else:
            self.open_steps_container.pack_forget()
            self.close_steps_container.pack_forget()

    def drawing_action(self):
        if not self.image:
            self.status_label.config(text=STATUS_NO_IMAGE, fg='red')
            return

        if not self.target_coords:
            self.status_label.config(text=STATUS_NO_DRAWING_AREA, fg='red')
            return

        # Kiểm tra điều kiện màu
        if self.color_mode.get() == COLOR_MODE_COLOR:
            if not self.palette_area_coords:
                self.status_label.config(text=STATUS_NO_PALETTE_AREA, fg='red')
                return

            if not self.color_clusters:
                self.status_label.config(
                    text=STATUS_NO_COLOR_ANALYSIS, fg='red')
                return

            if self.palette_type.get() == PALETTE_TYPE_1:
                valid, msg = self.open_palette_steps.validate_steps()
                if not valid:
                    self.status_label.config(
                        text=f"❌ Các bước mở: {msg}", fg='red')
                    return

        # Pause
        if self.drawing_engine.is_drawing and not self.drawing_engine.is_paused:
            self.drawing_engine.pause()
            self.status_label.config(text=STATUS_PAUSED, fg='orange')
            self.start_button.config(text="▶ Tiếp tục (F5)")
            if self.overlay:
                self.overlay.update_status("Tạm dừng", "orange")
            return

        # Resume
        if self.drawing_engine.is_drawing and self.drawing_engine.is_paused:
            self.drawing_engine.resume()
            self.status_label.config(text=STATUS_DRAWING, fg='green')
            self.start_button.config(text="⏸ Tạm dừng (F5)")
            if self.overlay:
                self.overlay.update_status("Đang vẽ", "#00ff00")
            return

        # Start
        self.progress.set(0)
        self.status_label.config(text=STATUS_DRAWING, fg='green')
        self.start_button.config(text="⏸ Tạm dừng (F5)")

        # Chuẩn bị settings
        settings = {
            'color_mode': self.color_mode.get(),
            'draw_mode': self.draw_mode.get(),
            'edge_thickness': self.edge_thickness.get(),
            'point_density': self.point_density.get(),
            'speed': self.speed.get(),
            'fast_mode': self.fast_mode.get(),
            'keep_aspect_ratio': self.keep_aspect_ratio.get(),
            'color_palette': self.color_clusters,
            'palette_area_coords': self.palette_area_coords,
            'palette_type': self.palette_type.get(),
            'open_palette_steps': self.open_palette_steps,
            'close_palette_steps': self.close_palette_steps,
        }

        # Chạy trong thread
        threading.Thread(
            target=self.drawing_engine.start_drawing,
            args=(self.image, self.color_image, self.target_coords, settings),
            daemon=True
        ).start()

    def stop_drawing(self):
        if not self.drawing_engine.is_drawing:
            return

        self.drawing_engine.stop()
        self.status_label.config(text=STATUS_STOPPED, fg='red')
        self.start_button.config(text="▶ Vẽ lại (F5)")
        self.progress.set(0)
        self.progress_label.config(text="0%")
        self.update_countdown(None)

        if self.overlay:
            self.overlay.update_status("Đã dừng", "red")
            self.overlay.destroy()
            self.overlay = None

        if self.ui_hidden:
            self.root.deiconify()
            self.ui_hidden = False

    def update_status(self, text, color='green'):
        self.root.after(
            0, lambda: self.status_label.config(text=text, fg=color))

    def update_progress(self, value):
        self.root.after(0, lambda: [
            self.progress.set(value),
            self.progress_label.config(text=f"{value:.1f}%"),
            self.overlay.update_progress(value) if self.overlay else None
        ])

    def update_countdown(self, remaining_seconds):
        from utils.helpers import format_time
        time_str = format_time(remaining_seconds)

        self.root.after(0, lambda: [
            self.countdown_label.config(text=f"⏰ {time_str}"),
            self.overlay.update_countdown(
                remaining_seconds) if self.overlay else None
        ])
