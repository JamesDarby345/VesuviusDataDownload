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
    base_url = "/full-scrolls/Scroll4/PHerc1667.volpkg/volume_grids/20231107190228/"
    target_dir = "./volume_grids/20231107190228/"

    mask_csv_file = "../Volume_Cube_Masks/Scroll4_full_scroll_cube_mask.csv"

    # Number of threads to use for downloading, 
    # ideally enough to saturate the network but not more
    # to prevent unnecessary switching overhead
    threads = 8

    if mask_csv_file == "":
        download_file(base_url, target_dir, threads)
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
