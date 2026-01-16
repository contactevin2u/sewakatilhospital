#!/usr/bin/env python3
"""
Convert all PNG/JPEG images to WebP format for better performance.
Also updates HTML files to use the new webp images.
"""

import os
import glob
from PIL import Image

def convert_to_webp(input_path, quality=85):
    """Convert an image to WebP format"""
    try:
        # Skip if already webp
        if input_path.lower().endswith('.webp'):
            return None

        # Create output path
        base = os.path.splitext(input_path)[0]
        output_path = base + '.webp'

        # Skip if webp already exists
        if os.path.exists(output_path):
            print(f"  Skipping (exists): {output_path}")
            return output_path

        # Open and convert
        with Image.open(input_path) as img:
            # Convert to RGB if necessary (for PNG with transparency)
            if img.mode in ('RGBA', 'P'):
                # Keep transparency for webp
                img.save(output_path, 'WEBP', quality=quality, lossless=False)
            else:
                img = img.convert('RGB')
                img.save(output_path, 'WEBP', quality=quality)

        # Get file sizes
        original_size = os.path.getsize(input_path)
        new_size = os.path.getsize(output_path)
        savings = ((original_size - new_size) / original_size) * 100

        print(f"  Converted: {os.path.basename(input_path)} -> {os.path.basename(output_path)}")
        print(f"    Size: {original_size/1024:.1f}KB -> {new_size/1024:.1f}KB ({savings:.1f}% smaller)")

        return output_path
    except Exception as e:
        print(f"  Error converting {input_path}: {e}")
        return None

def update_html_files(html_dir, image_mappings):
    """Update HTML files to use webp images"""
    html_files = glob.glob(os.path.join(html_dir, '**/*.html'), recursive=True)

    updated_count = 0
    for html_file in html_files:
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()

            original_content = content

            # Replace image references
            for old_ext in ['.png', '.PNG', '.jpg', '.JPG', '.jpeg', '.JPEG']:
                # Replace in src attributes
                content = content.replace(f'{old_ext}"', '.webp"')
                content = content.replace(f'{old_ext})', '.webp)')
                content = content.replace(f"{old_ext}'", ".webp'")

            if content != original_content:
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                updated_count += 1

        except Exception as e:
            print(f"  Error updating {html_file}: {e}")

    return updated_count

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    images_dir = os.path.join(base_dir, 'images')

    print("=" * 50)
    print("Converting images to WebP format")
    print("=" * 50)

    # Find all images
    image_extensions = ['*.png', '*.PNG', '*.jpg', '*.JPG', '*.jpeg', '*.JPEG']
    all_images = []

    for ext in image_extensions:
        all_images.extend(glob.glob(os.path.join(images_dir, '**', ext), recursive=True))

    print(f"\nFound {len(all_images)} images to convert\n")

    # Convert images
    converted = 0
    for img_path in all_images:
        result = convert_to_webp(img_path)
        if result:
            converted += 1

    print(f"\n{'=' * 50}")
    print(f"Converted {converted} images to WebP")
    print("=" * 50)

    # Update HTML files
    print("\nUpdating HTML files...")

    # Update location pages
    locations_dir = os.path.join(base_dir, 'locations')
    loc_updated = update_html_files(locations_dir, {})
    print(f"  Updated {loc_updated} location pages")

    # Update main pages
    main_updated = update_html_files(base_dir, {})
    print(f"  Updated {main_updated} main pages")

    print(f"\n{'=' * 50}")
    print("Done! All images converted and HTML files updated.")
    print("=" * 50)

if __name__ == '__main__':
    main()
