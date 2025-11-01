import json
import csv
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw

class MosaicGenerator():
    def __init__(self, config_path, colors_csv_path):
        self.config = self._load_config(config_path)
        self.lego_colors = self._load_colors(colors_csv_path)

    def _load_config(self, config_path):
        with open(config_path, 'r') as file:
            config = json.load(file)

        # TODO
        # Handle wrong and missing values
        # Handle wrong and missing keys

        return config

    def _load_colors(self, colors_csv_path):
        colors = {}
        with open(colors_csv_path, 'r') as file:
            reader = csv.reader(file)

            # Header lines
            header = next(reader) 

            # TODO
            # Refactor???
            for color in reader:
                color_id = color[0]
                rgb_value = color[1]
                colors[color_id] = rgb_value

        # TODO:
        # Handle empty file
        if not colors:
            print("No colors in CSV")

    def _find_closest_color(self, rgb):
        # TODO
        # Calculate "closest" color
        # Euclidian distance ??
        pass

    def _process_image(self):
        
        img = Image.open(self.config['input_image'])
        img = img.convert('RGB')

        target_size = (self.config['width'], self.config['height'])
        img = img.resize(target_size)

        # 2D array
        img_array = np.array(img)

        mosaic = []
        for col in range(len(img_array)):
            current_row = []
            for row in range(len(img_array[0])):
                # TODO:
                # Check type
                pixel_rgb = img_array[col][row]
                color_id = self._find_closest_color(pixel_rgb)
                row.append(color_id)
            mosaic.append(row)

        return mosaic

    def _generate_preview(self, mosaic):
        width = self.config['width']
        height = self.config['height']
        # TODO
        # FIX MAGIC NUMBER
        pixels_per_tile = 10

        img_width = width * pixels_per_tile
        img_height = height * pixels_per_tile

        # Create "empty" image with black background
        img = Image.new('RGB', (img_width, img_height), color='black')

        draw = ImageDraw.Draw(img)

        radius = pixels_per_tile//2

        # TODO
        # Check height width --> col row for non-square images...
        for col in range(height):
            for row in range(width):
                color_id = mosaic[col][row]
                color_rgb = self.lego_colors[color_id]

                # TODO
                # Make space between tiles??
                center_x = row * pixels_per_tile + radius
                center_y = col * pixels_per_tile + radius

                circle_box = [
                    center_x - radius,
                    center_y - radius,
                    center_x + radius,
                    center_y + radius
                ]
                draw.ellipse(circle_box, fill=color_rgb)

        output_path = Path(self.config['output_preview'])
        output_path.parent.mkdir(parents=True, exist_ok=True)
        img.save(output_path,'JPG', quality=95)
        print(f'Image saved: {output_path}')

    def _generate_shopping_list(self):
        # TODO
        # Implement
        pass

    def generate(self):
        mosaic = self._process_image()
        
        self._generate_preview(mosaic)

if __name__ == '__main__':
    pass