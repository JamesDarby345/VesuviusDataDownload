import os
import tifffile
from PIL import Image
import time

"""
old unparralelized code, use parallel_tif_to_jpg instead
"""

def convert_tif_to_jpg(source_folder):
    # Check if the source folder exists
    if not os.path.isdir(source_folder):
        print("Source folder does not exist.")
        return
    
    # Create the destination folder name by appending '_jpg' to the source folder name
    dest_folder = f"{source_folder}_jpg"
    
    # Create the destination folder if it doesn't exist
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    
    # Loop through all files in the source folder
    for filename in os.listdir(source_folder):
        if filename.lower().endswith('.tif') or filename.lower().endswith('.tiff'):
            # Construct full file path
            file_path = os.path.join(source_folder, filename)
            # Read the .tif file
            img_array = tifffile.imread(file_path) 
            # Convert the image array to 8-bit if not already
            if img_array.dtype != 'uint8':
                img_array = (img_array / 256).astype('uint8')
            # Convert the numpy array to a PIL Image
            img = Image.fromarray(img_array)
            # Construct the destination file path
            dest_file_path = os.path.join(dest_folder, f"{os.path.splitext(filename)[0]}.jpg")
            # Save the image as a compressed JPEG
            img.save(dest_file_path, "JPEG", quality=60) # Adjust quality as needed

def process_directory_structure(root_directory):
    for root, dirs, files in os.walk(root_directory):
        for name in dirs:
            if name == 'layers':
                layers_folder_path = os.path.join(root, name)
                print(f"Converting .tif files in {layers_folder_path}")
                convert_tif_to_jpg(layers_folder_path)

# Example usage
root_directory_path = '/Volumes/16TB_RAID_0/Scroll4/segments/20231111135340'
start_time = time.time()

process_directory_structure(root_directory_path)

end_time = time.time()
execution_time = end_time - start_time
print(f"Time to complete: {execution_time} seconds")
