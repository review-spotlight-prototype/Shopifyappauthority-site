#!/usr/bin/env python3
"""
Add purple circle background to favicon
"""

from PIL import Image, ImageDraw
import requests
import io

def add_purple_background(image_url, output_path):
    """Add a purple circle background to the favicon"""
    try:
        # Download the image
        response = requests.get(image_url)
        response.raise_for_status()

        # Open the image
        original = Image.open(io.BytesIO(response.content))

        # Convert to RGBA if not already
        if original.mode != 'RGBA':
            original = original.convert('RGBA')

        # Get image size - use the larger dimension for the circle
        width, height = original.size
        size = max(width, height)

        # Create a new image with the circle size
        new_image = Image.new('RGBA', (size, size), (0, 0, 0, 0))

        # Create a drawing context
        draw = ImageDraw.Draw(new_image)

        # Draw purple circle background
        # Using a nice purple color (#8B5CF6 - violet-500)
        purple_color = (139, 92, 246, 255)  # RGBA
        draw.ellipse([0, 0, size-1, size-1], fill=purple_color)

        # Calculate position to center the original image
        x = (size - width) // 2
        y = (size - height) // 2

        # Paste the original image on top of the purple circle
        new_image.paste(original, (x, y), original)

        # Save the result
        new_image.save(output_path, 'PNG', optimize=True)

        # Also create ICO format for favicon
        ico_path = output_path.replace('.png', '.ico')
        # Resize for favicon sizes
        favicon_sizes = [(16, 16), (32, 32), (48, 48)]
        favicon_images = []

        for favicon_size in favicon_sizes:
            resized = new_image.resize(favicon_size, Image.Resampling.LANCZOS)
            favicon_images.append(resized)

        # Save as ICO
        favicon_images[0].save(ico_path, format='ICO', sizes=[(img.size[0], img.size[1]) for img in favicon_images])

        print(f"Created favicon with purple background:")
        print(f"   PNG: {output_path}")
        print(f"   ICO: {ico_path}")

        return True

    except Exception as e:
        print(f"Error processing image: {e}")
        return False

def main():
    image_url = "https://imagedelivery.net/mYndgAUf_CYgFA1HoO_-GQ/43e7272a-fb53-44aa-f0f2-7656a83bc700/public"
    output_png = "favicon-with-background.png"

    print("Adding purple circle background to favicon...")

    if add_purple_background(image_url, output_png):
        print("\nFavicon background added successfully!")
        print("\nNext steps:")
        print("1. Review the generated favicon-with-background.png")
        print("2. If you like it, we can update all HTML files to use the new version")
        print("3. Or we can adjust the purple color if you prefer a different shade")
    else:
        print("Failed to process favicon")

if __name__ == "__main__":
    main()