import os
import shutil

"""
This file is to rename the sparesly downloaded tif files from 
0,N,N+1,...,N+M to 0,1,2,...,M so khartes can read them
The motivating usecase is to use khartes to identify which volume 
grids contain the scroll and then produce the mask.csv files
"""

def rename_and_remap_tifs(source_dir, file_nums, remap, destination_dir="*renamedTifs"):
    # Create the destination directory if it does not exist
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)
    
    # Construct a mapping from original filenames to new filenames
    filename_mapping = {f"{num:05}.tif": f"{remap[i]:05}.tif" for i, num in enumerate(file_nums)}
    
    # Iterate over files in the source directory
    for file in os.listdir(source_dir):
        if file.endswith(".tif") and file in filename_mapping:
            source_path = os.path.join(source_dir, file)
            destination_path = os.path.join(destination_dir, filename_mapping[file])
            # Copy and rename the .tif file to the new directory
            shutil.copy(source_path, destination_path)
            print(f"File {file} has been renamed to {filename_mapping[file]} and moved to {destination_dir}")

scrollZAxis = 14427 #scroll 2 z length 14427, scroll 4 z length 26390
step = 100 #every nth volume to sample

file_nums = []
remap = []
k = 0
for i in range(0, scrollZAxis, step):
    remap.append(k)
    file_nums.append(i)
    k += 1

# Example usage
source_dir = '/Users/jamesdarby/Documents/VesuviusScroll/GP/Vesuvius_Data_Download/Scroll2/volumes/20230210143520'  # Adjust to your directory path

# Call the function with the example parameters
rename_and_remap_tifs(source_dir, file_nums, remap)


