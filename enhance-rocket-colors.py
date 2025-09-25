#!/usr/bin/env python3
"""
Enhance rocket colors for better contrast against dark purple background
"""

from PIL import Image, ImageDraw, ImageEnhance
import requests
import io
import numpy as np

def enhance_rocket_colors(image_url, output_path):
    """Enhance the rocket colors for better visibility against dark purple background"""
    try:
        # Download the original image
        response = requests.get(image_url)
        response.raise_for_status()

        # Open the image
        original = Image.open(io.BytesIO(response.content))

        # Convert to RGBA if not already
        if original.mode != 'RGBA':
            original = original.convert('RGBA')

        # Get image size
        width, height = original.size
        size = max(width, height)

        # Create enhanced version of the rocket
        enhanced_rocket = original.copy()

        # Convert to numpy array for color manipulation
        data = np.array(enhanced_rocket)

        # Define color mappings for better contrast
        # We'll make the rocket brighter and more vibrant

        # Enhance existing colors to be more vibrant
        # Increase saturation and brightness for non-transparent pixels
        for y in range(data.shape[0]):
            for x in range(data.shape[1]):
                pixel = data[y, x]
                if pixel[3] > 0:  # If not transparent
                    r, g, b, a = pixel

                    # Convert to HSV-like adjustments
                    # Brighten overall
                    r = min(255, int(r * 1.3))
                    g = min(255, int(g * 1.3))
                    b = min(255, int(b * 1.3))

                    # Make specific color enhancements
                    # If it's greenish (rocket body), make it more cyan/bright green
                    if g > r and g > b:
                        g = min(255, int(g * 1.4))
                        b = min(255, int(b * 1.2))

                    # If it's orangish/reddish (flames), make it more vibrant
                    elif r > g and r > b:
                        r = min(255, int(r * 1.4))
                        g = min(255, int(g * 1.1))

                    # If it's bluish, make it brighter blue
                    elif b > r and b > g:
                        b = min(255, int(b * 1.4))
                        g = min(255, int(g * 1.1))

                    data[y, x] = [r, g, b, a]

        # Convert back to PIL Image
        enhanced_rocket = Image.fromarray(data, 'RGBA')

        # Apply additional enhancements
        # Increase contrast
        contrast_enhancer = ImageEnhance.Contrast(enhanced_rocket)
        enhanced_rocket = contrast_enhancer.enhance(1.3)

        # Increase saturation
        color_enhancer = ImageEnhance.Color(enhanced_rocket)
        enhanced_rocket = color_enhancer.enhance(1.4)

        # Create a new image with the dark purple circle background
        new_image = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(new_image)

        # Draw dark emerald green circle background
        emerald_color = (6, 78, 59, 255)  # #064E3B (dark emerald green)
        draw.ellipse([0, 0, size-1, size-1], fill=emerald_color)

        # Add a subtle bright border to help separation
        border_color = (16, 108, 89, 255)  # Slightly lighter emerald green
        draw.ellipse([2, 2, size-3, size-3], outline=border_color, width=3)

        # Calculate position to center the enhanced rocket
        x = (size - width) // 2
        y = (size - height) // 2

        # Paste the enhanced rocket on top
        new_image.paste(enhanced_rocket, (x, y), enhanced_rocket)

        # Save the result
        new_image.save(output_path, 'PNG', optimize=True)

        # Also create ICO format
        ico_path = output_path.replace('.png', '.ico')
        favicon_sizes = [(16, 16), (32, 32), (48, 48)]
        favicon_images = []

        for favicon_size in favicon_sizes:
            resized = new_image.resize(favicon_size, Image.Resampling.LANCZOS)
            favicon_images.append(resized)

        # Save as ICO
        favicon_images[0].save(ico_path, format='ICO', sizes=[(img.size[0], img.size[1]) for img in favicon_images])

        print(f"Enhanced rocket favicon created:")
        print(f"   PNG: {output_path}")
        print(f"   ICO: {ico_path}")

        return True

    except Exception as e:
        print(f"Error enhancing rocket colors: {e}")
        return False

def main():
    image_url = "https://imagedelivery.net/mYndgAUf_CYgFA1HoO_-GQ/43e7272a-fb53-44aa-f0f2-7656a83bc700/public"
    output_png = "favicon-enhanced.png"

    print("Enhancing rocket colors for better contrast...")

    if enhance_rocket_colors(image_url, output_png):
        print("\nRocket color enhancement complete!")
        print("The rocket should now have much better visibility against the dark purple background.")
        print("Colors have been brightened and made more vibrant while maintaining the original design.")
    else:
        print("Failed to enhance rocket colors")

if __name__ == "__main__":
    main()