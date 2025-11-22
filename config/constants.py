# Draw modes
DRAW_MODE_OUTLINE = "outline"
DRAW_MODE_FILL = "fill"
DRAW_MODE_SMART = "smart"

# Color modes
COLOR_MODE_GRAYSCALE = "grayscale"
COLOR_MODE_COLOR = "color"

# Palette types
PALETTE_TYPE_1 = "type1"  # Có bước mở/đóng + vùng màu
PALETTE_TYPE_2 = "type2"  # Chỉ vùng màu

# Step types
STEP_TYPE_CLICK = "click"
STEP_TYPE_AREA = "area"

# Image file types
IMAGE_FILE_TYPES = [
    ("Image files", "*.png *.jpg *.jpeg *.bmp *.gif")
]

# Status messages
STATUS_NO_IMAGE = "Chưa tải ảnh"
STATUS_IMAGE_LOADED = "✅ Đã tải ảnh: {}x{} pixels"
STATUS_NO_DRAWING_AREA = "❌ Vui lòng chọn vùng vẽ trước!"
STATUS_NO_PALETTE_AREA = "❌ Vui lòng chọn vùng bảng màu!"
STATUS_NO_COLOR_ANALYSIS = "❌ Vui lòng phân tích màu trước!"
STATUS_DRAWING = "▶️ Đang vẽ... (F5: tạm dừng, F6: kết thúc)"
STATUS_PAUSED = "⏸ Đã tạm dừng (F5: tiếp tục)"
STATUS_STOPPED = "⏹ Đã dừng vẽ"
STATUS_COMPLETED = "✅ Hoàn thành!"
