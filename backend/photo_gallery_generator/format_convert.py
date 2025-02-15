"""
This script converts BMP images to JPG format in a folder and deletes non-image files.
This is because the image embedding model only supports JPG, PNG, and GIF formats.
"""

import os
from PIL import Image

def convert_bmp_to_jpg(file_path):
    """
    param: file_path: path of the file
    return: None
    exception: None
    description: Convert BMP images to JPG format
    """    
    try:
        img = Image.open(file_path)
        new_file_path = file_path.rsplit(".", 1)[0] + ".jpg"
        img.convert("RGB").save(new_file_path, "JPEG")
        os.remove(file_path)  # Delete original BMP file
        print(f"Converted: {file_path} → {new_file_path}")
    except Exception as e:
        print(f"Failed to convert {file_path}: {e}")

def process_folder(target_folder):
    """
    param: target_folder: path of the target folder
    return: None
    exception: None
    description: Process all files in the target folder
    """
    valid_extensions = {".jpg", ".jpeg", ".png"}  # Keep these image formats
    
    for root, _, files in os.walk(target_folder):
        for file in files:
            file_path = os.path.join(root, file)
            ext = os.path.splitext(file)[-1].lower()
            
            if ext == ".bmp":
                convert_bmp_to_jpg(file_path)
            elif ext not in valid_extensions:
                os.remove(file_path)  # Delete non-image files
                print(f"Deleted: {file_path}")

if __name__ == "__main__":
    target_folder = "photo-gallery"  # Modify to your target folder
    print(os.path.abspath(target_folder))
    process_folder(target_folder)
