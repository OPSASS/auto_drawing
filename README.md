# Auto Drawing V1.0

Công cụ tự động vẽ tranh từ ảnh với Python.

## 📁 Cấu trúc dự án

```
auto_drawing/
│
├── config/
│   ├── __init__.py
|   ├── constants.py             # Hằng số
│   └── settings.py              # Cấu hình toàn cục
│
├── core/
│   ├── __init__.py
│   ├── color_analyzer.py        # Phân tích màu
│   ├── drawing_engine.py        # Logic vẽ chính
│   └── image_processor.py       # Xử lý ảnh
│
├── ui/
│   ├── __init__.py
│   ├── main_window.py           # Cửa sổ chính
│   ├── components/
│   │   ├── __init__.py
│   |   ├── progress_overlay.py      # ProgressOverlay
│   |   ├── selector_dialogs.py      # ScreenSelector, PointSelector
│   │   └── step_manager.py      # StepManager component
│   └── tabs/
│       ├── __init__.py
│       ├── advanced_tab.py      # Tab nâng cao
│       ├── basic_tab.py         # Tab cơ bản
│       └── color_tab.py         # Tab màu sắc
│
├── utils/
│   ├── __init__.py
│   └── helpers.py               # Hàm tiện ích
│
├── main.py                      # File chính để chạy ứng dụng
├── requirements.txt             # Thư viện cần thiết
└── README.md                    # Hướng dẫn
```

## 🚀 Cài đặt

### 1. Tạo cấu trúc thư mục

```bash
mkdir auto_drawing
cd auto_drawing

mkdir config core ui utils
mkdir ui/components ui/tabs
```

### 2. Copy các file vào đúng vị trí

- Copy nội dung các file từ artifacts vào các file tương ứng
- Tạo các file `__init__.py` trong mỗi folder

### 3. Cài đặt thư viện

```bash
pip install -r requirements.txt
```

### 4. Chạy ứng dụng

```bash
python main.py
```

## 📖 Hướng dẫn sử dụng

### Chế độ Đen Trắng

1. **Tải ảnh**: Nhấn "📁 Chọn ảnh mẫu"
2. **Chọn vùng vẽ**: Nhấn "📍 Vùng vẽ" và chọn vùng trên màn hình
3. **Chọn chế độ vẽ**:
   - 📐 Chỉ viền: Nhanh nhất
   - 🖌️ Fill đầy: Vẽ cả viền và fill
   - 🎯 Smart: Tự động chọn điểm quan trọng
4. **Điều chỉnh tốc độ và mật độ**
5. **Nhấn F5 để bắt đầu**

### Chế độ Màu Sắc

1. **Tải ảnh và chọn vùng vẽ** (giống chế độ đen trắng)
2. **Chọn chế độ màu**: 🌈 Màu sắc
3. **Thiết lập bảng màu**:
   - Chọn loại bảng màu (Type 1 hoặc Type 2)
   - Nhấn "📍 Chọn vùng bảng màu"
   - Nhấn "🔍 Phân tích màu" để tự động trích xuất màu từ ảnh
4. **Thiết lập các bước mở/đóng bảng màu** (nếu dùng Type 1):
   - Tab "🔓 MỞ bảng màu": Thêm các bước để mở bảng màu
   - Tab "🔒 ĐÓNG bảng màu": Thêm các bước để đóng (tùy chọn)
5. **Nhấn F5 để bắt đầu**

## ⌨️ Phím tắt

- **F5**: Tạm dừng / Tiếp tục
- **F6**: Kết thúc vẽ
- **F7**: Ẩn/Hiện giao diện

## 💡 Mẹo sử dụng

- Giảm mật độ (0.3-0.5) để vẽ nhanh hơn
- Bật "⚡ Chế độ siêu tốc" để tăng tốc độ tối đa
- Bật "📏 Giữ tỷ lệ ảnh" để tránh méo ảnh
- Chế độ "Chỉ viền" thích hợp cho outline
- Chế độ "Smart" tự động chọn điểm quan trọng

## 🔧 Cấu hình

Các cấu hình có thể thay đổi trong `config/settings.py`:

- `DEFAULT_SPEED`: Tốc độ vẽ mặc định
- `DEFAULT_POINT_DENSITY`: Mật độ điểm mặc định
- `DEFAULT_NUM_COLORS`: Số màu mặc định khi phân tích
- Màu sắc giao diện (COLOR_PRIMARY, COLOR_SECONDARY, etc.)
- Phím tắt (HOTKEY\_\*)

## 📦 Thư viện sử dụng

- **Pillow**: Xử lý ảnh
- **PyAutoGUI**: Tự động điều khiển chuột
- **OpenCV**: Phát hiện viền và xử lý ảnh nâng cao
- **scikit-learn**: Phân cụm màu với K-Means
- **NumPy**: Xử lý mảng và tính toán
- **keyboard**: Xử lý phím tắt

## 🎯 Tính năng

- ✅ Vẽ ảnh đen trắng với 3 chế độ (viền, fill, smart)
- ✅ Vẽ ảnh màu với phân tích màu tự động
- ✅ Hỗ trợ bảng màu với các bước mở/đóng tùy chỉnh
- ✅ Điều chỉnh tốc độ và mật độ vẽ
- ✅ Hiển thị tiến độ và thời gian còn lại
- ✅ Phím tắt tiện lợi
- ✅ Giao diện tab với nhiều tùy chọn
- ✅ Overlay hiển thị tiến độ khi ẩn giao diện

## 🐛 Xử lý lỗi

Nếu gặp lỗi:

1. Kiểm tra đã cài đặt đủ thư viện chưa
2. Đảm bảo Python version >= 3.8
3. Kiểm tra quyền truy cập màn hình của PyAutoGUI
4. Tắt chế độ fail-safe nếu cần: `pyautogui.FAILSAFE = False`

## 📝 License

MIT License

## 👨‍💻 Phát triển

Dự án được cấu trúc module hóa để dễ dàng:

- Thêm chế độ vẽ mới trong `core/image_processor.py`
- Thêm thuật toán phân tích màu trong `core/color_analyzer.py`
- Thêm tab mới trong `ui/tabs/`
- Tùy chỉnh giao diện trong các file UI

## 🤝 Đóng góp

Mọi đóng góp đều được chào đón! Hãy tạo pull request hoặc issue.
