import os
import subprocess
import csv

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

def download_file(remote_path, local_path, username, password):
    subprocess.run(["rclone", "copy", f":http:{remote_path}", f"{local_path}",
                    "--http-url", f"http://{username}:{password}@dl.ash2txt.org/", "--progress",
                    "--multi-thread-streams=8", "--transfers=8"], check=True)

def main():
    load_env_variables()
    username = get_env_variable("USERNAME", "username? ")
    password = get_env_variable("PASSWORD", "password? ")
    masked = input("Would you like to download the masked cubes or all the cubes? (masked/all): ")

    base_url = "/full-scrolls/Scroll1.volpkg/volume_grids/20230205180739/"
    target_dir = "./volume_grids/20230205180739/"

    if masked == "all":
        download_file(base_url, target_dir, username, password)
    else:
        #Default scroll only mask.csv file, (mask the non-scroll cubes)
        #change the path here if you want to use a different mask.csv file
        #code assumes the yxz coordinates in the .csv are the grids you want to download
        mask_csv_file = "../Volume_Cube_Masks/scroll_1_54_mask.csv"
        with open(mask_csv_file, newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip header row
            for jy, jx, jz in reader:
                filename = f"cell_yxz_{int(jy):03d}_{int(jx):03d}_{int(jz):03d}.tif"
                remote_path = f"{base_url}{filename}"
                download_file(remote_path, target_dir, username, password)

if __name__ == "__main__":
    main()
