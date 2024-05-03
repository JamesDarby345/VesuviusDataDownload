import os
import subprocess

def strip_quotes(value):
    return value.replace("'", "").replace('"', "")

def load_env_variables():
    # Attempt to load environment variables from a .env file
    with open("../../config.env", "r") as file:
        for line in file:
            key, value = line.strip().split("=", 1)
            os.environ[key] = strip_quotes(value)

def get_env_variable(name, prompt):
    value = os.getenv(name)
    if not value:
        value = input(prompt)
    return value

def main():
    load_env_variables()
    username = get_env_variable("USERNAME", "username? ")
    password = get_env_variable("PASSWORD", "password? ")

    base_url = "/fragments/PHerc1667Cr01Fr03.volpkg/working/PHerc1667Cr01Fr03_70keV_3.24um/surface_processing"
    target_dir = "./"

    # Number of threads to use for downloading, 
    # ideally enough to saturate the network but not more
    # to prevent unnecessary switching overhead
    threads = 8

    data_selection = input("would you like to download the final outputs, or all the fragment surface files? default to final outputs (all/final): ")

    if data_selection == "all":
        subprocess.run(["rclone", "copy", f":http:{base_url}", f"{target_dir}",
                        "--http-url", f"https://{username}:{password}@dl.ash2txt.org/", "--progress",
                        f"--multi-thread-streams={threads}", f"--transfers={threads}"], check=True)
    else:
        subprocess.run(["rclone", "copy", f":http:{base_url}/surface_volume", f"{target_dir}surface_volume",
                        "--http-url", f"https://{username}:{password}@dl.ash2txt.org/", "--progress",
                        f"--multi-thread-streams={threads}", f"--transfers={threads}"], check=True)
        
        additonal_files = ["ir.png","inklabels.png","result.tif","mask.png"]
        for file in additonal_files:
            subprocess.run(["rclone", "copy", f":http:{base_url}/{file}", f"{target_dir}",
                        "--http-url", f"https://{username}:{password}@dl.ash2txt.org/", "--progress",
                        f"--multi-thread-streams={threads}", f"--transfers={threads}"], check=True)
        


if __name__ == "__main__":
    main()
