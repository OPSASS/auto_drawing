import tkinter as tk
from tkinter import ttk
import pyautogui
import time
from ui.components.selector_dialogs import ScreenSelector, PointSelector


class StepManager(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, relief='flat', borderwidth=0, bg='#f5f5f5')
        self.app = app
        self.steps = []
        self.step_widgets = []

        self.setup_ui()

    def setup_ui(self):
        # Header
        header_frame = tk.Frame(self, bg='#f5f5f5')
        header_frame.pack(fill='x', padx=5, pady=5)

        tk.Button(
            header_frame, text="➕ Thêm bước",
            command=self.add_step,
            bg='#4CAF50', fg='white',
            font=('Arial', 8, 'bold'),
            cursor='hand2', relief='flat',
            padx=10, pady=3
        ).pack(side='right', padx=2)

        # Scrollable container
        self.steps_container = tk.Frame(self, bg='#f5f5f5')
        self.steps_container.pack(fill='both', expand=True, padx=5, pady=5)

        self.canvas = tk.Canvas(
            self.steps_container, bg='#f5f5f5',
            highlightthickness=0, height=150
        )
        scrollbar = ttk.Scrollbar(
            self.steps_container, orient="vertical",
            command=self.canvas.yview
        )
        self.scrollable_frame = tk.Frame(self.canvas, bg='#f5f5f5')

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window(
            (0, 0), window=self.scrollable_frame, anchor="nw"
        )
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def add_step(self):
        step_index = len(self.steps)

        step_data = {
            'type': 'click',
            'coords': None,
            'delay': 0.2,
            'description': f'Bước {step_index + 1}'
        }

        self.steps.append(step_data)

        # Step frame
        step_frame = tk.Frame(
            self.scrollable_frame, relief='solid',
            borderwidth=1, bg='white'
        )
        step_frame.pack(fill='x', pady=3, padx=2)

        # Header
        header = tk.Frame(step_frame, bg='#e3f2fd')
        header.pack(fill='x')

        tk.Label(
            header, text=f"🔸 Bước {step_index + 1}",
            font=('Arial', 9, 'bold'), bg='#e3f2fd'
        ).pack(side='left', padx=8, pady=5)

        btn_frame = tk.Frame(header, bg='#e3f2fd')
        btn_frame.pack(side='right', padx=5)

        tk.Button(
            btn_frame, text="⬆️",
            command=lambda: self.move_step_up(step_index),
            bg='#2196F3', fg='white', font=('Arial', 8, 'bold'),
            width=3, relief='flat', cursor='hand2'
        ).pack(side='left', padx=1)

        tk.Button(
            btn_frame, text="⬇️",
            command=lambda: self.move_step_down(step_index),
            bg='#2196F3', fg='white', font=('Arial', 8, 'bold'),
            width=3, relief='flat', cursor='hand2'
        ).pack(side='left', padx=1)

        tk.Button(
            btn_frame, text="🗑️",
            command=lambda: self.remove_step(step_index),
            bg='#F44336', fg='white', font=('Arial', 8, 'bold'),
            width=3, relief='flat', cursor='hand2'
        ).pack(side='left', padx=1)

        # Body
        body = tk.Frame(step_frame, bg='white')
        body.pack(fill='x', padx=8, pady=5)

        # Type selection
        type_frame = tk.Frame(body, bg='white')
        type_frame.pack(fill='x', pady=3)

        tk.Label(
            type_frame, text="Loại:", font=('Arial', 9),
            bg='white', width=12, anchor='w'
        ).pack(side='left')

        step_type_var = tk.StringVar(value='click')
        tk.Radiobutton(
            type_frame, text="Click điểm", variable=step_type_var,
            value='click', font=('Arial', 9), bg='white',
            command=lambda: self.update_step_type(step_index, 'click')
        ).pack(side='left', padx=5)

        tk.Radiobutton(
            type_frame, text="Chọn vùng", variable=step_type_var,
            value='area', font=('Arial', 9), bg='white',
            command=lambda: self.update_step_type(step_index, 'area')
        ).pack(side='left')

        # Coordinates
        coord_frame = tk.Frame(body, bg='white')
        coord_frame.pack(fill='x', pady=3)

        tk.Label(
            coord_frame, text="Tọa độ:", font=('Arial', 9),
            bg='white', width=12, anchor='w'
        ).pack(side='left')

        btn_select = tk.Button(
            coord_frame, text="📍 Chọn",
            command=lambda: self.select_step_coords(step_index),
            bg='#FF9800', fg='white', font=('Arial', 8, 'bold'),
            relief='flat', cursor='hand2', padx=8
        )
        btn_select.pack(side='left', padx=5)

        coords_label = tk.Label(
            coord_frame, text="Chưa chọn",
            font=('Arial', 9), fg='red', bg='white'
        )
        coords_label.pack(side='left')

        # Delay
        delay_frame = tk.Frame(body, bg='white')
        delay_frame.pack(fill='x', pady=3)

        tk.Label(
            delay_frame, text="Delay (s):", font=('Arial', 9),
            bg='white', width=12, anchor='w'
        ).pack(side='left')

        delay_var = tk.DoubleVar(value=0.2)
        tk.Scale(
            delay_frame, from_=0.0, to=2.0, resolution=0.1,
            orient='horizontal', variable=delay_var, length=180,
            command=lambda v: self.update_step_delay(step_index, float(v)),
            bg='white', highlightthickness=0
        ).pack(side='left', padx=5)

        # Description
        desc_frame = tk.Frame(body, bg='white')
        desc_frame.pack(fill='x', pady=3)

        tk.Label(
            desc_frame, text="Mô tả:", font=('Arial', 9),
            bg='white', width=12, anchor='w'
        ).pack(side='left')

        desc_entry = tk.Entry(desc_frame, font=('Arial', 9), width=25)
        desc_entry.insert(0, f'Bước {step_index + 1}')
        desc_entry.bind(
            '<KeyRelease>',
            lambda e: self.update_step_description(
                step_index, desc_entry.get())
        )
        desc_entry.pack(side='left', padx=5, fill='x', expand=True)

        self.step_widgets.append({
            'frame': step_frame,
            'type_var': step_type_var,
            'coords_label': coords_label,
            'delay_var': delay_var,
            'desc_entry': desc_entry
        })

    def select_step_coords(self, step_index):
        if step_index >= len(self.steps):
            return

        step = self.steps[step_index]
        self.app.root.withdraw()

        if step['type'] == 'click':
            def on_point_selected(x, y):
                step['coords'] = {'x': x, 'y': y}
                self.step_widgets[step_index]['coords_label'].config(
                    text=f"({x}, {y})", fg='green'
                )
                self.app.root.deiconify()

            PointSelector(on_point_selected,
                          f"Chọn điểm cho {step['description']}")
        else:
            def on_area_selected(x1, y1, x2, y2):
                step['coords'] = {'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2}
                self.step_widgets[step_index]['coords_label'].config(
                    text=f"({x1},{y1}→{x2},{y2})", fg='green'
                )
                self.app.root.deiconify()

            ScreenSelector(on_area_selected,
                           f"Chọn vùng cho {step['description']}")

    def update_step_type(self, step_index, step_type):
        if step_index < len(self.steps):
            self.steps[step_index]['type'] = step_type
            self.steps[step_index]['coords'] = None
            self.step_widgets[step_index]['coords_label'].config(
                text="Chưa chọn", fg='red'
            )

    def update_step_delay(self, step_index, delay):
        if step_index < len(self.steps):
            self.steps[step_index]['delay'] = delay

    def update_step_description(self, step_index, description):
        if step_index < len(self.steps):
            self.steps[step_index]['description'] = description

    def remove_step(self, step_index):
        if step_index < len(self.steps):
            self.steps.pop(step_index)
            self.step_widgets[step_index]['frame'].destroy()
            self.step_widgets.pop(step_index)
            self.refresh_step_numbers()

    def move_step_up(self, step_index):
        if step_index > 0:
            self.steps[step_index], self.steps[step_index - 1] = \
                self.steps[step_index - 1], self.steps[step_index]
            self.step_widgets[step_index], self.step_widgets[step_index - 1] = \
                self.step_widgets[step_index -
                                  1], self.step_widgets[step_index]

            self.step_widgets[step_index]['frame'].pack_forget()
            self.step_widgets[step_index - 1]['frame'].pack_forget()
            self.step_widgets[step_index -
                              1]['frame'].pack(fill='x', pady=3, padx=2)
            self.step_widgets[step_index]['frame'].pack(
                fill='x', pady=3, padx=2)

            self.refresh_step_numbers()

    def move_step_down(self, step_index):
        if step_index < len(self.steps) - 1:
            self.steps[step_index], self.steps[step_index + 1] = \
                self.steps[step_index + 1], self.steps[step_index]
            self.step_widgets[step_index], self.step_widgets[step_index + 1] = \
                self.step_widgets[step_index +
                                  1], self.step_widgets[step_index]

            self.step_widgets[step_index]['frame'].pack_forget()
            self.step_widgets[step_index + 1]['frame'].pack_forget()
            self.step_widgets[step_index]['frame'].pack(
                fill='x', pady=3, padx=2)
            self.step_widgets[step_index +
                              1]['frame'].pack(fill='x', pady=3, padx=2)

            self.refresh_step_numbers()

    def refresh_step_numbers(self):
        for i, widget in enumerate(self.step_widgets):
            header_label = widget['frame'].winfo_children()[
                0].winfo_children()[0]
            header_label.config(text=f"🔸 Bước {i + 1}")

    def execute_steps(self):
        for i, step in enumerate(self.steps):
            if not step['coords']:
                return False, f"Bước {i + 1} chưa được thiết lập tọa độ"

            try:
                if step['type'] == 'click':
                    pyautogui.click(step['coords']['x'], step['coords']['y'])
                else:
                    center_x = (step['coords']['x1'] +
                                step['coords']['x2']) // 2
                    center_y = (step['coords']['y1'] +
                                step['coords']['y2']) // 2
                    pyautogui.click(center_x, center_y)

                time.sleep(step['delay'])
            except Exception as e:
                return False, f"Lỗi tại bước {i + 1}: {str(e)}"

        return True, "Thành công"

    def get_steps_count(self):
        return len(self.steps)

    def validate_steps(self):
        if len(self.steps) == 0:
            return True, "Không có bước nào"

        for i, step in enumerate(self.steps):
            if not step['coords']:
                return False, f"Bước {i + 1} chưa thiết lập tọa độ"

        return True, "Hợp lệ"
