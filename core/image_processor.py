import cv2
import numpy as np
from utils.helpers import find_smart_points


class ImageProcessor:

    @staticmethod
    def extract_edges(image_array, thickness=2):
        edges = cv2.Canny(image_array, 50, 150)

        if thickness > 1:
            kernel = np.ones((thickness, thickness), np.uint8)
            edges = cv2.dilate(edges, kernel, iterations=1)

        return edges

    @staticmethod
    def get_fill_points(image_array, edge_mask, threshold=128):
        inner_mask = image_array < threshold
        fill_mask = inner_mask & (~edge_mask.astype(bool))
        return fill_mask

    @staticmethod
    def get_outline_coords(pixels, edge_thickness):
        edges = ImageProcessor.extract_edges(pixels, edge_thickness)
        return np.argwhere(edges > 0)

    @staticmethod
    def get_fill_coords(pixels, edge_thickness, density=1.0):
        edges = ImageProcessor.extract_edges(pixels, edge_thickness)
        edge_coords = np.argwhere(edges > 0)

        fill_mask = ImageProcessor.get_fill_points(pixels, edges)
        fill_coords = np.argwhere(fill_mask)

        # Áp dụng mật độ
        if density < 1.0 and len(fill_coords) > 0:
            skip_factor = max(1, int(1 / density))
            fill_coords = fill_coords[::skip_factor]

        return edge_coords, fill_coords

    @staticmethod
    def get_smart_coords(pixels, density=1.0, threshold=128):
        draw_coords = np.argwhere(pixels < threshold)

        # Áp dụng mật độ
        if density < 1.0:
            skip_factor = max(1, int(1 / density))
            draw_coords = draw_coords[::skip_factor]

        # Smart sampling nếu quá nhiều điểm
        if len(draw_coords) > 100:
            draw_coords = find_smart_points(draw_coords, 0.4)

        return draw_coords

    @staticmethod
    def process_image_for_drawing(pixels, draw_mode, edge_thickness, point_density):
        if draw_mode == "outline":
            draw_coords = ImageProcessor.get_outline_coords(
                pixels, edge_thickness)
            info_text = f"🎨 Vẽ viền: {len(draw_coords)} điểm"

        elif draw_mode == "fill":
            edge_coords, fill_coords = ImageProcessor.get_fill_coords(
                pixels, edge_thickness, point_density
            )
            draw_coords = np.vstack([edge_coords, fill_coords])
            info_text = f"🎨 Viền: {len(edge_coords)} + Fill: {len(fill_coords)} điểm"

        else:  # smart mode
            draw_coords = ImageProcessor.get_smart_coords(
                pixels, point_density)
            info_text = f"🎨 Smart: {len(draw_coords)} điểm"

        return draw_coords, info_text
