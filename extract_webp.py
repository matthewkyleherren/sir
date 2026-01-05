#!/usr/bin/env python3
"""
Extract WebP image from base64 data URI
"""

import base64
import sys
from pathlib import Path


def extract_webp(input_file, output_file=None):
    """
    Read a file containing base64-encoded WebP data and save it as a WebP file
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
        output_file = input_path.with_suffix(".webp")

    # Write the binary data to a WebP file
    with open(output_file, "wb") as f:
        f.write(binary_data)

    print(f"✓ Successfully extracted WebP image to: {output_file}")
    print(f"  File size: {len(binary_data):,} bytes")

    return True


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extract_webp.py <input_file> [output_file]")
        print("\nExample:")
        print(
            "  python extract_webp.py cdn.prod.website-files.com/683fa5578c4365b4bb69fade/img output.webp"
        )
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    extract_webp(input_file, output_file)
