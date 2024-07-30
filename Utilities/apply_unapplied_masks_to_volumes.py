import os
import time
import tifffile
import cv2
import numpy as np

"""
This file applies the unapplied masks to the original volumes. The masks are png images where the non-zero pixels
indicate the region of the volume that should be kept. The masks are applied by thresholding them to 0 or 1
and multiplying the volume by the mask.
If save as tif is true, masked volumes are saved as .tif files with lzw compression. 
If save as jpg is true, it will save the masked volumes as jpg files with 95% quality.
The code will overwrite the files if they already exist.
"""

unapplied_masks_path = "https://dl.ash2txt.org/community-uploads/james/PHerc0332/volumes_masked/20231027191953_unapplied_masks/"
original_volume_path = "https://dl.ash2txt.org/full-scrolls/Scroll3/PHerc332.volpkg/volumes/20231027191953/"
output_path = "https://dl.ash2txt.org/community-uploads/james/PHerc0332/volumes_masked/20231027191953/"
save_as_tif = True
save_as_jpg = True

if save_as_tif:
    os.makedirs(output_path, exist_ok=True)
if save_as_jpg:
    os.makedirs(output_path + "_jpg", exist_ok=True)

unapplied_masks = os.listdir(unapplied_masks_path)
original_volumes = os.listdir(original_volume_path)
unapplied_masks.sort()
original_volumes.sort()

# Create a map of the original volume names to their paths
original_volume_map = {}
for volume in original_volumes:
    volume_name = os.path.splitext(volume)[0]
    volume_path = os.path.join(original_volume_path, volume)
    original_volume_map[volume_name] = volume_path

count = 0
for unapplied_mask in unapplied_masks:
    mask_name = os.path.splitext(unapplied_mask)[0]
    volume_path = original_volume_map[mask_name]
    volume = tifffile.imread(volume_path)
    mask = cv2.imread(os.path.join(unapplied_masks_path, unapplied_mask), cv2.IMREAD_GRAYSCALE)
    binary_mask = (mask >= 1).astype(bool)  # Threshold the mask to boolean values
    applied_mask = np.multiply(volume, binary_mask, dtype=volume.dtype)

    if save_as_tif:
        tifffile.imwrite(os.path.join(output_path, f"{mask_name}.tif"), applied_mask, compression='lzw')

    if save_as_jpg:
        if applied_mask.dtype == np.uint16:
            applied_mask = cv2.convertScaleAbs(applied_mask, alpha=(255.0/65535.0))
        cv2.imwrite(os.path.join(output_path + "_jpg", f"{mask_name}.jpg"), applied_mask, [int(cv2.IMWRITE_JPEG_QUALITY), 95])

    count += 1
    if count % 100 == 0:
        print(f"Processed {count} masks")
