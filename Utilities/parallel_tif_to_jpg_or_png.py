import os
import sys
import tifffile
from PIL import Image
from concurrent.futures import ProcessPoolExecutor
import time

def convert_single_tif(file_path, dest_folder, output_format='jpg', quality=85):
    try:
        img_array = tifffile.imread(file_path)
        if img_array.dtype != 'uint8':
            img_array = (img_array / 256).astype('uint8')
        img = Image.fromarray(img_array)
        filename = os.path.basename(file_path)
        dest_file_path = os.path.join(dest_folder, f"{os.path.splitext(filename)[0]}.{output_format}")
        if output_format == 'jpg':
            img.save(dest_file_path, "JPEG", quality=quality)
        elif output_format == 'png':
            img.save(dest_file_path, "PNG")
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

def convert_tif(source_folder, output_format='jpg', quality=85, overwrite=True):
    dest_folder_suffix = '_jpg' if output_format == 'jpg' else '_png'
    dest_folder = f"{source_folder}{dest_folder_suffix}"
    
    if not overwrite and os.path.exists(dest_folder):
        print(f"Skipping conversion in {source_folder} as {dest_folder} exists.")
        return
    
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    
    tif_files = [os.path.join(source_folder, f) for f in os.listdir(source_folder) if f.lower().endswith(('.tif', '.tiff'))]

    with ProcessPoolExecutor() as executor:
        futures = [executor.submit(convert_single_tif, file_path, dest_folder, output_format, quality) for file_path in tif_files]
        for future in futures:
            future.result()

def process_specific_folders(root_directory, target_types, output_format='jpg', quality=85, overwrite=True):
    for root, dirs, files in os.walk(root_directory):
        if os.path.basename(root) in target_types:
            # Process direct subdirectories of a matching folder
            for sub_dir in dirs:
                specific_folder_path = os.path.join(root, sub_dir)
                print(f"Processing .tif files in {specific_folder_path} to {output_format.upper()} with quality {quality}")
                convert_tif(specific_folder_path, output_format=output_format, quality=quality, overwrite=overwrite)

if __name__ == '__main__':
    root_directory_path = '/path/to/directory'
    target_types = ['volumes', 'masked_volumes', 'segments']  # Default types to check
    output_format = 'jpg'  # Default output format
    quality = 85  # Default quality
    overwrite = False  # Default overwrite

    if len(sys.argv) > 1:
        root_directory_path = sys.argv[1]
    if len(sys.argv) > 2:
        target_types = [sys.argv[2]]  # Accepts one target type or 'all'
        if target_types[0] == 'all':
            target_types = ['volumes', 'masked_volumes', 'segments']
    if len(sys.argv) > 3:
        output_format = sys.argv[3]  # 'jpg' or 'png'
    if len(sys.argv) > 4:
        quality = int(sys.argv[4])
    print(f"Converting .tif files in {root_directory_path} to {output_format.upper()} with quality {quality}")
    print(f"Target data types: {target_types}")

    process_specific_folders(root_directory_path, target_types, output_format=output_format, quality=quality, overwrite=overwrite)
