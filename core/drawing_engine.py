import time
import pyautogui
import numpy as np
from PIL import Image
from config.settings import FAST_MODE_BATCH_SIZE, NORMAL_MODE_BATCH_SIZE
from core.image_processor import ImageProcessor
from core.color_analyzer import ColorAnalyzer
from utils.helpers import calculate_draw_dimensions, calculate_remaining_time


class DrawingEngine:
    def __init__(self, app):
        self.app = app
        self.is_drawing = False
        self.is_paused = False
        self.start_time = None
        self.total_points = 0
        self.processed_points = 0
        self.drawing_offset = {'x': 0, 'y': 0}
        self.actual_draw_size = {'width': 0, 'height': 0}

    def start_drawing(self, image, color_image, target_coords, settings):
        self.is_drawing = True
        self.is_paused = False
        self.start_time = time.time()
        self.processed_points = 0

        # Tính kích thước vẽ
        target_size = (target_coords['width'], target_coords['height'])
        img_size = image.size

        dimensions = calculate_draw_dimensions(
            img_size, target_size, settings['keep_aspect_ratio']
        )

        self.drawing_offset = {
            'x': dimensions['offset_x'],
            'y': dimensions['offset_y']
        }
        self.actual_draw_size = {
            'width': dimensions['width'],
            'height': dimensions['height']
        }

        new_size = (dimensions['width'], dimensions['height'])

        # Vẽ theo chế độ màu
        if settings['color_mode'] == "color":
            self._draw_color_image(
                color_image, new_size, target_coords, settings
            )
        else:
            self._draw_grayscale_image(
                image, new_size, target_coords, settings
            )

    def _draw_grayscale_image(self, image, size, target_coords, settings):
        resized_image = image.convert('L').resize(
            size, Image.Resampling.LANCZOS)
        pixels = np.array(resized_image)

        # Xử lý ảnh để lấy tọa độ
        draw_coords, info_text = ImageProcessor.process_image_for_drawing(
            pixels,
            settings['draw_mode'],
            settings['edge_thickness'],
            settings['point_density']
        )

        self.total_points = len(draw_coords)
        self.app.update_status(info_text, 'green')

        if self.total_points == 0:
            self.app.update_status("❌ Không có điểm để vẽ!", 'red')
            return

        time.sleep(1)

        # Vẽ
        try:
            self._draw_points_batch(
                draw_coords, target_coords, settings
            )
        except Exception as e:
            self.app.update_status(f"❌ Lỗi: {str(e)}", 'red')

    def _draw_color_image(self, color_image, size, target_coords, settings):
        resized_image = color_image.resize(size, Image.Resampling.LANCZOS)
        pixels = np.array(resized_image)

        self.app.update_status("🔄 Đang phân chia lớp màu...", 'orange')

        # Phân chia lớp màu
        color_layers = ColorAnalyzer.get_color_layers(
            pixels, settings['color_palette']
        )
        color_layers = {
            color: coords for color, coords in color_layers.items()
            if len(coords) > 0
        }

        total_colors = len(color_layers)
        self.total_points = sum(len(coords)
                                for coords in color_layers.values())

        self.app.update_status(
            f"🎨 Vẽ {total_colors} màu, tổng {self.total_points} điểm",
            'green'
        )

        time.sleep(1)

        # Vẽ từng lớp màu
        try:
            for color_idx, (color, coords) in enumerate(color_layers.items()):
                if not self.is_drawing:
                    break

                # Cập nhật overlay
                if self.app.overlay:
                    self.app.overlay.update_color(
                        color, f"Màu {color_idx + 1}/{total_colors}"
                    )

                # Click màu trong bảng
                self._click_color_in_palette(color, settings)

                # Áp dụng mật độ
                if settings['point_density'] < 1.0 and len(coords) > 0:
                    skip_factor = max(1, int(1 / settings['point_density']))
                    coords = coords[::skip_factor]

                # Vẽ lớp màu
                draw_coords = np.array(coords)
                self._draw_color_layer(
                    draw_coords, target_coords, settings,
                    color_idx, total_colors
                )

        except Exception as e:
            self.app.update_status(f"❌ Lỗi: {str(e)}", 'red')

    def _click_color_in_palette(self, color, settings):
        # Mở bảng màu (nếu có)
        if settings['palette_type'] == "type1":
            success, msg = settings['open_palette_steps'].execute_steps()
            if not success:
                raise Exception(f"Lỗi mở bảng màu: {msg}")

        # Chụp và tìm màu
        palette_coords = settings['palette_area_coords']
        x1, y1 = palette_coords['x1'], palette_coords['y1']
        x2, y2 = palette_coords['x2'], palette_coords['y2']

        palette_screenshot = pyautogui.screenshot(
            region=(x1, y1, x2-x1, y2-y1))
        palette_array = np.array(palette_screenshot)

        position = ColorAnalyzer.find_color_in_palette_area(
            color, palette_array)

        if position:
            click_x = x1 + position[0]
            click_y = y1 + position[1]
            pyautogui.click(click_x, click_y)
            time.sleep(0.3)
        else:
            raise Exception("Không tìm thấy màu trong bảng màu")

        # Đóng bảng màu (nếu có)
        if settings.get('close_palette_steps') and \
           settings['close_palette_steps'].get_steps_count() > 0:
            settings['close_palette_steps'].execute_steps()

    def _draw_points_batch(self, draw_coords, target_coords, settings):
        batch_size = FAST_MODE_BATCH_SIZE if settings['fast_mode'] else NORMAL_MODE_BATCH_SIZE
        speed_multiplier = 0.1 if settings['fast_mode'] else 0.5
        batch_points = []
        last_countdown_update = time.time()

        for idx, (y, x) in enumerate(draw_coords):
            if not self.is_drawing:
                break

            while self.is_paused:
                time.sleep(0.1)

            # Tính tọa độ màn hình
            screen_x = target_coords['x1'] + x + self.drawing_offset['x']
            screen_y = target_coords['y1'] + y + self.drawing_offset['y']
            batch_points.append((screen_x, screen_y))

            # Vẽ batch
            if len(batch_points) >= batch_size:
                for bx, by in batch_points:
                    pyautogui.click(bx, by)
                    if not settings['fast_mode']:
                        time.sleep(settings['speed'] * speed_multiplier)
                batch_points = []

            self.processed_points += 1

            # Cập nhật countdown
            current_time = time.time()
            if current_time - last_countdown_update >= 1:
                elapsed = current_time - self.start_time
                remaining = calculate_remaining_time(
                    self.processed_points, self.total_points, elapsed
                )
                self.app.update_countdown(remaining)
                last_countdown_update = current_time

            # Cập nhật progress
            if idx % 50 == 0 or idx == len(draw_coords) - 1:
                progress_val = ((idx + 1) / len(draw_coords)) * 100
                self.app.update_progress(progress_val)

            if not settings['fast_mode']:
                time.sleep(settings['speed'] * speed_multiplier)

        # Vẽ batch còn lại
        for bx, by in batch_points:
            if self.is_drawing:
                pyautogui.click(bx, by)
                self.processed_points += 1

    def _draw_color_layer(self, draw_coords, target_coords, settings,
                          color_idx, total_colors):
        batch_size = FAST_MODE_BATCH_SIZE if settings['fast_mode'] else NORMAL_MODE_BATCH_SIZE
        speed_multiplier = 0.1 if settings['fast_mode'] else 0.5
        batch_points = []
        last_countdown_update = time.time()
        layer_total = len(draw_coords)

        for idx, (y, x) in enumerate(draw_coords):
            if not self.is_drawing:
                break

            while self.is_paused:
                time.sleep(0.1)

            screen_x = target_coords['x1'] + x + self.drawing_offset['x']
            screen_y = target_coords['y1'] + y + self.drawing_offset['y']
            batch_points.append((screen_x, screen_y))

            if len(batch_points) >= batch_size:
                for bx, by in batch_points:
                    pyautogui.click(bx, by)
                    if not settings['fast_mode']:
                        time.sleep(settings['speed'] * speed_multiplier)
                batch_points = []

            self.processed_points += 1

            current_time = time.time()
            if current_time - last_countdown_update >= 1:
                elapsed = current_time - self.start_time
                remaining = calculate_remaining_time(
                    self.processed_points, self.total_points, elapsed
                )
                self.app.update_countdown(remaining)
                last_countdown_update = current_time

            if idx % 50 == 0 or idx == layer_total - 1:
                layer_progress = (idx + 1) / layer_total
                overall_progress = (
                    (color_idx + layer_progress) / total_colors) * 100
                self.app.update_progress(overall_progress)

            if not settings['fast_mode']:
                time.sleep(settings['speed'] * speed_multiplier)

        for bx, by in batch_points:
            if self.is_drawing:
                pyautogui.click(bx, by)
                self.processed_points += 1

    def stop(self):
        self.is_drawing = False
        self.is_paused = False

    def pause(self):
        self.is_paused = True

    def resume(self):
        self.is_paused = False
