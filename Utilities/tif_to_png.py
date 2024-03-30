import os
from PIL import Image

def convert_tif_to_png(input_dir, output_dir, start_range=None, end_range=None, compress=False, downsample=1, overwrite=False):
    tif_files = [f for f in os.listdir(input_dir) if f.endswith('.tif')]
    tif_files.sort()

    for file in tif_files[start_range:end_range]:
        tif_path = os.path.join(input_dir, file)
        png_path = os.path.join(output_dir, file.replace('.tif', '.png'))

        if os.path.exists(png_path) and not overwrite:
            print(f'Skipping {tif_path.split("/")[-1]} (PNG already exists)')
            continue
        print(f'Converting {tif_path.split("/")[-1]}')

        with Image.open(tif_path) as img:
            if downsample > 1:
                img = img.resize((img.width // downsample, img.height // downsample))

            if compress:
                img.save(png_path, 'PNG', compress_level=9)
            else:
                img.save(png_path, 'PNG')

"""
This file is to help create png files from tif files

Scroll 1 length: 14375
Scroll 2 length: 14427
Scroll 3 canonical length: 22940
Scroll 4 canonical length: 26390
"""

input_dir = '/Users/jamesdarby/Desktop/finetune_detect-a-scroll/to_pngify'
output_dir = '/Users/jamesdarby/Desktop/finetune_detect-a-scroll/to_annotate'
start_range = 0  # Start range index 
end_range = 20000  # End range index (range doesnt need to include all numbers to work)
compress = True #lossless compression, False for no compression, will make file smaller but increase r/w times
downsample = 1 # Downsample factor (1 for no downsampling)
overwrite = False # Overwrite existing files

convert_tif_to_png(input_dir, output_dir, start_range, end_range, compress, downsample, overwrite)
