import os
import sys
import tifffile
from PIL import Image
from concurrent.futures import ProcessPoolExecutor
import time

def convert_single_tif_to_jpg(file_path, dest_folder, quality=85):
    try:
        # Attempt to read and convert the TIFF file
        img_array = tifffile.imread(file_path)
        if img_array.dtype != 'uint8':
            img_array = (img_array / 256).astype('uint8')
        img = Image.fromarray(img_array)
        filename = os.path.basename(file_path)
        dest_file_path = os.path.join(dest_folder, f"{os.path.splitext(filename)[0]}.jpg")
        img.save(dest_file_path, "JPEG", quality=quality)
    except Exception as e:
        # Log the error and skip this file
        print(f"Error processing {file_path}: {e}")

def convert_tif_to_jpg(source_folder, quality=85, overwrite=True):
    dest_folder = f"{source_folder}_jpg"
    
    # If overwrite is False and the destination folder already exists, skip processing
    if not overwrite and os.path.exists(dest_folder):
        print(f"Skipping {source_folder} as overwrite is False and {dest_folder} exists.")
        return
    
    # Otherwise, proceed with creating the destination folder if it doesn't already exist
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    
    # List of all TIFF files to be converted
    tif_files = [os.path.join(source_folder, f) for f in os.listdir(source_folder) if f.lower().endswith(('.tif', '.tiff'))]

    # Use ProcessPoolExecutor to parallelize conversion
    with ProcessPoolExecutor() as executor:
        # Map each TIFF file to the convert_single_tif_to_jpg function
        futures = [executor.submit(convert_single_tif_to_jpg, file_path, dest_folder, quality) for file_path in tif_files]

        # Wait for all futures to complete (optional, for tracking progress or handling exceptions)
        for future in futures:
            future.result()  # This will re-raise any exception that occurred in a worker

def process_directory_structure(root_directory, quality=85, overwrite=True):
    for root, dirs, files in os.walk(root_directory):
        for name in dirs:
            if name == 'layers':
                layers_folder_path = os.path.join(root, name)
                print(f"Processing .tif files in {layers_folder_path} to quality {quality} JPEGs")
                start_time = time.time()
                convert_tif_to_jpg(layers_folder_path, quality=quality, overwrite=overwrite)
                end_time = time.time()
                execution_time = end_time - start_time
                print(f"Time to complete folder: {execution_time} seconds")

if __name__ == '__main__':
    # Default root directory path
    root_directory_path = '/Volumes/16TB_RAID_0/Scroll4/'

    # Check if a command line argument is provided to overwrite root_directory_path
    if len(sys.argv) > 1:
        root_directory_path = sys.argv[1]
    
    process_directory_structure(root_directory_path, quality=60, overwrite=False)
