# Print Friendly LEGO
# Copyright (C) 2025 Ashley Morris

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import sys
import argparse
import numpy as np
from PIL import Image
from scipy.ndimage import binary_dilation, label

def hex_to_rgb(hex_color):
    """Convert hex color string like '#899093' to RGB tuple."""
    hex_color = hex_color.lstrip('#')
    if len(hex_color) != 6:
        raise ValueError("Invalid hex color format.")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def clean_image(input_path, output_path, background_rgb):
    image = Image.open(input_path).convert("RGBA")
    img_np = np.array(image)
    rgb = img_np[..., :3]
    alpha = img_np[..., 3]

    # Step 1: Identify white pixels
    white_mask = (rgb[..., 0] > 230) & (rgb[..., 1] > 230) & (rgb[..., 2] > 230) & (alpha > 0)

    # Step 2: Detect background pixels (user-defined)
    dist_to_bg = np.linalg.norm(rgb - background_rgb, axis=-1)
    bg_mask = dist_to_bg < 2

    # Step 3: Dilate background mask to find bordering white pixels
    near_bg = binary_dilation(bg_mask, structure=np.ones((3, 3)))
    seed_white = white_mask & near_bg

    # Step 4: Find connected white components
    labeled, num_features = label(white_mask)
    convert_to_black_mask = np.zeros_like(white_mask, dtype=bool)

    for i in range(1, num_features + 1):
        region = (labeled == i)
        if np.any(region & seed_white):
            convert_to_black_mask |= region

    # Step 5: Convert selected white pixels to black
    img_np[convert_to_black_mask] = [0, 0, 0, 255]

    # Step 6: Remove background (set to transparent)
    updated_rgb = img_np[..., :3]
    dist_to_bg = np.linalg.norm(updated_rgb - background_rgb, axis=-1)
    final_bg_mask = dist_to_bg < 20
    img_np[final_bg_mask] = [0, 0, 0, 0]

    result = Image.fromarray(img_np)
    result.save(output_path)
    print(f"Cleaned image saved: {output_path}")

def process_directory(input_dir, background_rgb):
    if not os.path.isdir(input_dir):
        print(f"Error: '{input_dir}' is not a valid directory.")
        sys.exit(1)

    output_dir = f"{input_dir.rstrip(os.sep)}_processed"
    os.makedirs(output_dir, exist_ok=True)

    for filename in os.listdir(input_dir):
        if filename.lower().endswith(".png"):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)
            clean_image(input_path, output_path, background_rgb)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Clean LEGO-style PNG images by converting white-on-background to black and removing the background.")
    parser.add_argument("input_directory", help="Path to directory containing PNG images.")
    parser.add_argument("--background-colour", type=str, default="#899093",
                        help="Hex code of background colour to remove (default: #899093)")
    args = parser.parse_args()

    try:
        background_rgb = np.array(hex_to_rgb(args.background_colour))
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    process_directory(args.input_directory, background_rgb)
    print(f"\n✅ All images cleaned. Output directory: {args.input_directory.rstrip(os.sep)}_processed")
