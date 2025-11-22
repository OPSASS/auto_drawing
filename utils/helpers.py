from math import gcd
import numpy as np


def calculate_aspect_ratio(width, height):
    if width == 0 or height == 0:
        return "N/A"
    g = gcd(width, height)
    return f"{width//g}:{height//g}"


def rgb_to_hex(rgb):
    return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"


def calculate_brightness(color):
    return sum(color)


def format_time(seconds):
    if seconds is None or seconds <= 0:
        return "--:--:--"

    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


def calculate_remaining_time(processed, total, elapsed_time):
    if processed <= 0 or elapsed_time <= 0:
        return None

    points_per_second = processed / elapsed_time
    if points_per_second <= 0:
        return None

    remaining_points = total - processed
    return remaining_points / points_per_second


def find_smart_points(points, target_density=0.3, grid_size=8):
    if len(points) <= 1000:
        return points

    if len(points) > 0:
        height = np.max(points[:, 0]) + 1
        width = np.max(points[:, 1]) + 1
    else:
        return points

    smart_points = []

    for i in range(grid_size):
        for j in range(grid_size):
            y_min = i * height // grid_size
            y_max = (i + 1) * height // grid_size
            x_min = j * width // grid_size
            x_max = (j + 1) * width // grid_size

            region_points = []
            for point in points:
                y, x = point
                if y_min <= y < y_max and x_min <= x < x_max:
                    region_points.append([y, x])

            if region_points:
                region_points = np.array(region_points)
                samples_from_region = max(
                    2, int(len(region_points) * target_density)
                )
                if len(region_points) > samples_from_region:
                    indices = np.random.choice(
                        len(region_points), samples_from_region, replace=False
                    )
                    smart_points.extend(region_points[indices])
                else:
                    smart_points.extend(region_points)

    return np.array(smart_points)


def calculate_draw_dimensions(img_size, target_size, keep_aspect_ratio):
    img_width, img_height = img_size
    target_width, target_height = target_size

    if keep_aspect_ratio:
        scale_width = target_width / img_width
        scale_height = target_height / img_height
        scale = min(scale_width, scale_height)

        new_width = int(img_width * scale)
        new_height = int(img_height * scale)

        offset_x = (target_width - new_width) // 2
        offset_y = (target_height - new_height) // 2

        return {
            'width': new_width,
            'height': new_height,
            'offset_x': offset_x,
            'offset_y': offset_y
        }
    else:
        return {
            'width': target_width,
            'height': target_height,
            'offset_x': 0,
            'offset_y': 0
        }
