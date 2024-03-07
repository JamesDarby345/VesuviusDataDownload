"""
Scroll 1 length: 14375
Scroll 2 length: 14427
Scroll 3 canonical length: 22940
Scroll 4 canonical length: 26390
"""
import numpy as np
import tifffile
import csv


scrollZAxis = 14427 #Scroll length/number of volumes/scroll Z axis

masked_volume_path = '/Volumes/Corsair_8TB/Scroll2/masked_volumes/20230210143520'
cube_size = 500 #standard Vesuvius challenge cube size
step = 100 #number of volumes to skip
file_nums = [i for i in range(0, scrollZAxis, step)] #every nth (step) volume to sample

# Create a list of file names to download, use the number of digits in the scrollZAxis to format the file names
num_digits = len(str(scrollZAxis))
file_list = [f"{num:0{num_digits}}.tif" for num in file_nums]

# Defines the 'fidelity' of the cube mask, more often samples will allow for more accurate masks
# But will take longer to process and requires more data to be downloaded and masked
volumes_per_cube = int(cube_size/step)  # Number of volumes per 500x500x500 cube

#TODO deal with the 1-indexing properly
imgMaxY, imgMaxX = tifffile.imread(f"{masked_volume_path}/{file_list[0]}").shape[0:3]  # Get the x and y dimensions of the first volume
cubeMaxX, cubeMaxY, cubeMaxZ = (imgMaxX//cube_size)+1, (imgMaxY//cube_size)+1, (scrollZAxis//cube_size)+1 # Calculate the maximum x, y, and z coordinates of the cubes, 1-indexed

# Create a 3D array to store the cube masks, initilize to True for all elements
# True (1) will mean the cube is not blank, thus is part of the scroll
# False (0) means the cube is blank, thus not part of the scroll
cube_mask = np.ones((cubeMaxY, cubeMaxX, cubeMaxZ), dtype=bool) #y,x,z coords to match vol cube names
mask_sum = np.sum(cube_mask)
print(f"Initial cube mask sum: {mask_sum}")

blank_sum = 0
duplicate_blank_sum = 0
# Load in {volumes_per_cube} volumes at a time from the masked volume directory
# Stack them into a x*y*{volumes_per_cube} array
# Then use a sliding window of cube_size x cube_size x volumes_per_cube to check for blank cubes
# TODO ensure/test that the x,y,z coordinates are correct
for i in range(0, len(file_list), volumes_per_cube):
    print(f"Processing images {i} to {i+volumes_per_cube}, aka volume range {i*step} to {(i+volumes_per_cube)*step}")
    volume = tifffile.imread(f"{masked_volume_path}/{file_list[i]}")  # Read the volume from the masked volume directory
    volume = np.moveaxis(volume, 0, -1)  # Move the axis to the end, so that the shape is (x, y)
    for j in range(1, volumes_per_cube):
        volume = np.dstack((volume, np.moveaxis(tifffile.imread(f"{masked_volume_path}/{file_list[i+j]}"), 0, -1)))  # Stack the volumes along the z-axis
    for x in range(0, volume.shape[0], cube_size):
        for y in range(0, volume.shape[1], cube_size):
            for z in range(0, volume.shape[2], volumes_per_cube):
                cube = volume[x:x+cube_size, y:y+cube_size, z:z+volumes_per_cube]  # Extract a 500x500x{volumes_per_cube} cube from the volume
                if np.all(cube == 0):  # Check if the cube is blank/masked (all elements are 0)
                    blank_sum += 1
                    cube_mask[y//cube_size,x//cube_size,i//volumes_per_cube] = False # Set the cube mask y,x,z coord to False if the cube is blank/masked

print(f"Initial cube mask sum: {mask_sum}")
print(f"Blank cube sum: {blank_sum}")
print(f"Final cube mask sum: {np.sum(cube_mask)}")

#Transform the True element indicies of cube_mask into a .csv file with header jy, jx, jz
#This will be the cube mask file
csv_file_path = f'../Volume_Cube_Masks/{masked_volume_path.split("/")[-1]}_full_scroll_cube_mask.csv'
sorted_cube_coords = np.argwhere(cube_mask)  # Get the indices of the True elements in the cube_mask
sorted_cube_coords = sorted_cube_coords.tolist()  # Convert the indices to a list
# print(sorted_cube_coords)
with open(csv_file_path, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    
    # Write the header
    writer.writerow(['jy', 'jx', 'jz'])
    
    # Iterate through the sorted set and write each tuple to the csv file
    for coord in sorted_cube_coords:
        writer.writerow(coord)
