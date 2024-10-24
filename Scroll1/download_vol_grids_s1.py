import os
import subprocess
import csv
from tempfile import NamedTemporaryFile

def strip_quotes(value):
    return value.replace("'", "").replace('"', "")


#used to provide multi threaded download of individually specified files
def download_files_from_list(file_list, local_path, remote_path, threads):
    # Create a temporary file to list the files to download
    with NamedTemporaryFile(mode='w', delete=False) as temp_file:
        for file in file_list:
            temp_file.write(f"{file}\n")
        temp_file_path = temp_file.name

    try:
        # Use the temporary file with the --files-from option in rclone
        subprocess.run(["rclone", "copy", f":http:{remote_path}", f"{local_path}",
                        "--http-url", f"https://dl.ash2txt.org/",
                        "--files-from", temp_file_path, "--progress", 
                        f"--multi-thread-streams={threads}", f"--transfers={threads}"], check=True)
    finally:
        os.remove(temp_file_path)  # Clean up the temporary file

def download_file(remote_path, local_path, threads):
    subprocess.run(["rclone", "copy", f":http:{remote_path}", f"{local_path}",
                    "--http-url", f"https://dl.ash2txt.org/", "--progress",
                    f"--multi-thread-streams={threads}", f"--transfers={threads}"], check=True)

def main():
    masked = input("Would you like to download just the useful (masked) cubes, the cubes intersecting the gp section, or all the cubes? (masked/gp/all): ")

    base_url = "/full-scrolls/Scroll1/PHercParis4.volpkg/volume_grids/20230205180739/"
    target_dir = "./volume_grids/20230205180739/"

    #Default scroll only mask.csv file, (mask the non-scroll cubes)
    #change the path here if you want to use a different mask.csv file
    #code assumes the yxz coordinates in the .csv are the grids you want to download
    mask_csv_file = "../Volume_Cube_Masks/scroll_1_54_mask.csv"
    gp_mask_csv_file = "../Volume_Cube_Masks/Scroll_gp_grid_mask.csv"

    # Number of threads to use for downloading, 
    # ideally enough to saturate the network but not more
    # to prevent unnecessary switching overhead
    threads = 8

    if masked.lower().strip() == "all":
        download_file(base_url, target_dir, threads)
    elif masked.lower().strip() == "gp":
        files = []

        with open(gp_mask_csv_file, newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)

            for jy, jx, jz in reader:
                        filename = f"cell_yxz_{int(jy):03d}_{int(jx):03d}_{int(jz):03d}.tif"
                        files.append(filename)
    else:
        files = []

        with open(mask_csv_file, newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip header row
            for jy, jx, jz in reader:
                filename = f"cell_yxz_{int(jy):03d}_{int(jx):03d}_{int(jz):03d}.tif"
                files.append(filename)



        download_files_from_list(files, target_dir, base_url, threads)


if __name__ == "__main__":
    main()
