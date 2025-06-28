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
from pdf2image import convert_from_path

def pdf_to_png(pdf_path, dpi=300):
    """
    Converts each page of a PDF into high-resolution PNG images.

    Parameters:
        pdf_path (str): Path to the input PDF file.
        dpi (int): Resolution in dots per inch (default 300).
    """
    base_name = os.path.splitext(os.path.basename(pdf_path))[0]
    output_folder = base_name.replace(" ", "_")

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    print(f"Converting '{pdf_path}' to PNG images at {dpi} DPI...")
    print(f"Output directory: {output_folder}")

    try:
        images = convert_from_path(pdf_path, dpi=dpi)
        for i, img in enumerate(images):
            output_path = os.path.join(output_folder, f"page_{i+1:03d}.png")
            img.save(output_path, "PNG")
            print(f"Saved {output_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert PDF to high-resolution PNG images.")
    parser.add_argument("pdf_path", help="Path to the input PDF file.")
    parser.add_argument("--dpi", type=int, default=300, help="Image resolution in DPI (default: 300).")
    args = parser.parse_args()

    if not os.path.isfile(args.pdf_path):
        print(f"Error: File '{args.pdf_path}' does not exist.")
        sys.exit(1)

    pdf_to_png(args.pdf_path, dpi=args.dpi)
