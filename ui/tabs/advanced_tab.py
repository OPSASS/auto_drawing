import tkinter as tk
from tkinter import ttk


class AdvancedTab:
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
        # Keyboard shortcuts
        self.create_section("⌨️ Phím tắt")

        shortcuts_frame = tk.Frame(
            self.scrollable_frame, bg='white', relief='solid', bd=1
        )
        shortcuts_frame.pack(fill='x', padx=10, pady=5)

        shortcuts = [
            ("F5", "Tạm dừng/Tiếp tục"),
            ("F6", "Kết thúc"),
            ("F7", "Ẩn/Hiện giao diện"),
        ]

        for key, desc in shortcuts:
            row = tk.Frame(shortcuts_frame, bg='white')
            row.pack(fill='x', padx=10, pady=3)

            tk.Label(
                row, text=key, font=('Arial', 9, 'bold'),
                bg='#e3f2fd', fg='#1976D2', width=6,
                relief='raised', bd=1
            ).pack(side='left', padx=5)

            tk.Label(
                row, text=desc, font=('Arial', 9),
                bg='white', anchor='w'
            ).pack(side='left', padx=5)

        # Usage guide
        self.create_section("📖 Hướng dẫn sử dụng")

        guide_frame = tk.Frame(
            self.scrollable_frame, bg='white', relief='solid', bd=1
        )
        guide_frame.pack(fill='x', padx=10, pady=5)

        guide_text = """
        1. Tải ảnh cần vẽ
        2. Chọn vùng vẽ trên màn hình
        3. Chọn chế độ màu (đen trắng hoặc màu sắc)
        4. Nếu chọn màu sắc, thiết lập bảng màu:
            - Chọn vùng bảng màu
            - Phân tích màu từ ảnh
            - Thiết lập các bước mở/đóng bảng màu (nếu cần)
        5. Điều chỉnh tốc độ và mật độ
        6. Nhấn F5 để bắt đầu vẽ
        7. Nhấn F7 để ẩn giao diện khi vẽ
        8. Nhấn F6 để dừng
        """

        tk.Label(
            guide_frame, text=guide_text.strip(), font=('Arial', 9),
            bg='white', justify='left', anchor='w'
        ).pack(padx=10, pady=10, fill='x')

        # Tips
        self.create_section("💡 Mẹo sử dụng")

        tips_frame = tk.Frame(
            self.scrollable_frame, bg='white', relief='solid', bd=1
        )
        tips_frame.pack(fill='x', padx=10, pady=5)

        tips_text = """
        • Chế độ "Chỉ viền": Nhanh nhất, phù hợp vẽ outline
        • Chế độ "Fill đầy": Vẽ cả viền và fill, mất thời gian hơn
        • Chế độ "Smart": Tự động chọn điểm quan trọng
        • Giảm mật độ để vẽ nhanh hơn
        • Bật "Chế độ siêu tốc" để tăng tốc độ tối đa
        • Giữ tỷ lệ ảnh để không bị méo
        """

        tk.Label(
            tips_frame, text=tips_text.strip(), font=('Arial', 9),
            bg='white', justify='left', anchor='w'
        ).pack(padx=10, pady=10, fill='x')

        # About
        self.create_section("ℹ️ Thông tin")

        about_frame = tk.Frame(
            self.scrollable_frame, bg='white', relief='solid', bd=1
        )
        about_frame.pack(fill='x', padx=10, pady=5)

        tk.Label(
            about_frame, text="Auto Drawing App V2.0",
            font=('Arial', 11, 'bold'), bg='white'
        ).pack(pady=5)

        tk.Label(
            about_frame, text="Công cụ tự động vẽ tranh từ ảnh",
            font=('Arial', 9), bg='white', fg='#666666'
        ).pack(pady=2)

        tk.Label(
            about_frame, text="Phát triển bởi Python + OpenCV + PyAutoGUI",
            font=('Arial', 8), bg='white', fg='#999999'
        ).pack(pady=(5, 10))

    def create_section(self, title):
        tk.Label(
            self.scrollable_frame, text=title, font=('Arial', 10, 'bold'),
            bg='#f5f5f5', fg='#333333', anchor='w'
        ).pack(fill='x', padx=10, pady=(10, 5))

    def get_frame(self):
        return self.frame
