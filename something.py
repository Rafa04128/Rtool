from PIL import Image
import os

def convert_jpeg_to_png(jpeg_file):
    try:
        # Open the JPEG image
        with Image.open(jpeg_file) as img:
            # Construct the output path with a .png extension
            png_file = os.path.splitext(jpeg_file)[0] + '.png'
            
            # Save the image as PNG in the same directory
            img.save(png_file, 'PNG')
            
            print(f"Converted: {jpeg_file} to {png_file}")
    except Exception as e:
        print(f"Error converting {jpeg_file}: {e}")

# Example usage
jpeg_file_path = r'C:\Users\LINES\Desktop\project\rtool\favicon.jpeg'
convert_jpeg_to_png(jpeg_file_path)
