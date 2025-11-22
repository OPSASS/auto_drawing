import numpy as np
from PIL import Image
from sklearn.cluster import KMeans
from config.settings import COLOR_ANALYSIS_SIZE


class ColorAnalyzer:
    @staticmethod
    def analyze_colors(image, num_colors=8):
        # Resize ảnh nhỏ để tăng tốc
        small_img = image.resize(COLOR_ANALYSIS_SIZE, Image.Resampling.LANCZOS)
        pixels = np.array(small_img).reshape(-1, 3)

        # Clustering
        kmeans = KMeans(n_clusters=num_colors, random_state=42, n_init=10)
        kmeans.fit(pixels)

        colors = kmeans.cluster_centers_.astype(int)

        # Sắp xếp theo độ sáng
        brightness = np.sum(colors, axis=1)
        sorted_indices = np.argsort(brightness)

        return [tuple(colors[i]) for i in sorted_indices]

    @staticmethod
    def find_closest_color(target_color, color_palette):
        min_dist = float('inf')
        closest_color = color_palette[0]

        for color in color_palette:
            dist = np.sqrt(
                sum((a - b) ** 2 for a, b in zip(target_color, color)))
            if dist < min_dist:
                min_dist = dist
                closest_color = color

        return closest_color

    @staticmethod
    def get_color_layers(pixels, color_palette):
        height, width, _ = pixels.shape
        color_layers = {color: [] for color in color_palette}

        for y in range(height):
            for x in range(width):
                pixel_color = tuple(pixels[y, x, :3])
                closest_color = ColorAnalyzer.find_closest_color(
                    pixel_color, color_palette
                )
                color_layers[closest_color].append((y, x))

        return color_layers

    @staticmethod
    def find_color_in_palette_area(target_color, palette_screenshot_array):
        target_color = np.array(target_color)
        min_distance = float('inf')
        best_position = None

        step = 2  # Bỏ qua một số pixel để tăng tốc
        for y in range(0, palette_screenshot_array.shape[0], step):
            for x in range(0, palette_screenshot_array.shape[1], step):
                pixel_color = palette_screenshot_array[y, x, :3]
                distance = np.sqrt(np.sum((pixel_color - target_color) ** 2))
                if distance < min_distance:
                    min_distance = distance
                    best_position = (x, y)

        return best_position
