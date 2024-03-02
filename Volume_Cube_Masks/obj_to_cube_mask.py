import os
import csv

"""
This code was created to help download the volume grids that contain a segmentation
to download labeled data for training an autosegmentation model.

This file takes a path to a .obj file as input, then reads all the 3D points from it
It then converts the 3D points to volume grid coordinates and writes them to a CSV mask file
It was tested that the coordinates lined up on Scroll 1
Thus from the .obj file we can download the volume grids that contains it
"""


# Path to the directory containing the .obj file
file_path = '/Users/jamesdarby/Documents/VesuviusScroll/GP/Ink_Model/Vesuvius-Grandprize-Winner/train_scrolls/20231210121321/20231210121321.obj'

grid_coords = set() #in y, x, z order

grid_coords = set()  # in y, x, z order

with open(file_path, "r") as fd:
    for line in fd:
        line = line.strip()
        words = line.split()
        if words[0] == 'v':
            # Extract the 3D coordinates of the vertex
            vertex = line.split()
            x, y, z = map(float, vertex[1:])

            # Convert the 3D coordinates to grid coordinates
            grid_coords.add((int(y / 500) + 1, int(x / 500) + 1, int(z / 500) + 1))
            

sorted_grid_coords = sorted(grid_coords)

#extract the id from the path .obj file
id = file_path.split('/')[-1].split('.')[0]
csv_file_path = f'{id}_grid_mask.csv'

# Write to the CSV file
with open(csv_file_path, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    
    # Write the header
    writer.writerow(['jy', 'jx', 'jz'])
    
    # Iterate through the sorted set and write each tuple
    for coord in sorted_grid_coords:
        writer.writerow(coord)

print(f'CSV volume cube mask file "{csv_file_path}" created successfully.')

