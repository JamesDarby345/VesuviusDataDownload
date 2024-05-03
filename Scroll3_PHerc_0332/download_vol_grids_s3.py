import os
import subprocess
import csv
from tempfile import NamedTemporaryFile

def strip_quotes(value):
    return value.replace("'", "").replace('"', "")

def load_env_variables():
    with open("../config.env", "r") as file:
        for line in file:
            key, value = line.strip().split("=", 1)
            os.environ[key] = strip_quotes(value)

def get_env_variable(name, prompt):
    value = os.getenv(name)
    if not value:
        value = input(prompt)
    return value

#used to provide multi threaded download of individually specified files
def download_files_from_list(file_list, local_path, username, password, remote_path, threads):
    # Create a temporary file to list the files to download
    with NamedTemporaryFile(mode='w', delete=False) as temp_file:
        for file in file_list:
            temp_file.write(f"{file}\n")
        temp_file_path = temp_file.name

    try:
        # Use the temporary file with the --files-from option in rclone
        subprocess.run(["rclone", "copy", f":http:{remote_path}", f"{local_path}",
                        "--http-url", f"https://{username}:{password}@dl.ash2txt.org/",
                        "--files-from", temp_file_path, "--progress", 
                        f"--multi-thread-streams={threads}", f"--transfers={threads}"], check=True)
    finally:
        os.remove(temp_file_path)  # Clean up the temporary file

def download_file(remote_path, local_path, username, password, threads):
    subprocess.run(["rclone", "copy", f":http:{remote_path}", f"{local_path}",
                    "--http-url", f"https://{username}:{password}@dl.ash2txt.org/", "--progress",
                    f"--multi-thread-streams={threads}", f"--transfers={threads}"], check=True)

def main():
    load_env_variables()
    username = get_env_variable("USERNAME", "username? ")
    password = get_env_variable("PASSWORD", "password? ")
    masked = input("Would you like to download just the useful (masked) cubes or all the cubes? (masked/all): ")

    base_url = "/full-scrolls/PHerc0332.volpkg/volume_grids/20231027191953/"
    target_dir = "./volume_grids/20231027191953/"

    #Default scroll only mask.csv file, (mask the non-scroll cubes)
    #change the path here if you want to use a different mask.csv file
    #code assumes the yxz coordinates in the .csv are the grids you want to download
    mask_csv_file = "../Volume_Cube_Masks/pherc_0332_53.csv"

    # Number of threads to use for downloading, 
    # ideally enough to saturate the network but not more
    # to prevent unnecessary switching overhead
    threads = 8

    if masked == "all":
        download_file(base_url, target_dir, username, password, threads)
    else:
        files = []

        with open(mask_csv_file, newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip header row
            for jy, jx, jz in reader:
                filename = f"cell_yxz_{int(jy):03d}_{int(jx):03d}_{int(jz):03d}.tif"
                files.append(filename)



        download_files_from_list(files, target_dir, username, password, base_url, threads)


if __name__ == "__main__":
    main()
