#!/usr/bin/env python3
"""
Convert WebP image data to JPG format
"""

import base64
import sys
from pathlib import Path


def convert_webp_to_jpg(input_file, output_file=None):
    """
    Read a file containing base64-encoded WebP data and convert it to JPG
    """
    # Read the input file
    with open(input_file, "r") as f:
        content = f.read()

    # Extract base64 data (remove the data:image/jpeg;base64, prefix if present)
    if content.startswith("data:"):
        # Find where the actual base64 data starts
        base64_data = content.split(",", 1)[1] if "," in content else content
    else:
        base64_data = content

    # Decode base64 to binary
    try:
        binary_data = base64.b64decode(base64_data)
    except Exception as e:
        print(f"Error decoding base64: {e}")
        return False

    # Determine output filename
    if output_file is None:
        input_path = Path(input_file)
        output_file = input_path.with_suffix(".jpg")

    # Write the binary data to a temporary WebP file
    temp_webp = Path(output_file).with_suffix(".webp")
    with open(temp_webp, "wb") as f:
        f.write(binary_data)

    print(f"WebP file created: {temp_webp}")

    # Try to convert using PIL/Pillow
    try:
        from PIL import Image

        # Open WebP and convert to JPG
        img = Image.open(temp_webp)

        # Convert to RGB if necessary (JPG doesn't support transparency)
        if img.mode in ("RGBA", "LA", "P"):
            # Create white background
            background = Image.new("RGB", img.size, (255, 255, 255))
            if img.mode == "P":
                img = img.convert("RGBA")
            background.paste(
                img, mask=img.split()[-1] if img.mode in ("RGBA", "LA") else None
            )
            img = background
        elif img.mode != "RGB":
            img = img.convert("RGB")

        # Save as JPG
        img.save(output_file, "JPEG", quality=95)
        print(f"✓ Successfully converted to: {output_file}")

        # Clean up temp file
        temp_webp.unlink()

        return True

    except ImportError:
        print("\nPillow library not found. Please install it:")
        print("  pip install Pillow")
        print(f"\nAlternatively, you can use the WebP file directly: {temp_webp}")
        return False
    except Exception as e:
        print(f"Error converting image: {e}")
        print(f"WebP file is available at: {temp_webp}")
        return False


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python convert_to_jpg.py <input_file> [output_file]")
        print("\nExample:")
        print(
            "  python convert_to_jpg.py cdn.prod.website-files.com/683fa5578c4365b4bb69fade/img"
        )
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    convert_webp_to_jpg(input_file, output_file)
