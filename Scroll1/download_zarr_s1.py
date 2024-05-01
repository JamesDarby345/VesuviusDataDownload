import os
import subprocess

def strip_quotes(value):
    return value.replace("'", "").replace('"', "")

def load_env_variables():
    # Attempt to load environment variables from a .env file
    with open("../config.env", "r") as file:
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

    scrollName = "Scroll1"
    scrollNum = 1

    base_url = f"/full-scrolls/{scrollName}/"
    temp_base_url = f"/community-uploads/james-darby/{scrollName}/"
    base_url = temp_base_url
    target_dir = f"./Scroll{scrollNum}.zarr/"
    threads = 8
    filename = f"Scroll{scrollNum}.zarr"

    print(f"Downloading {filename}...")
    print(f":https:{base_url}{filename}")

    subprocess.run(["rclone", "copy", f":https:{base_url}{filename}", f"{target_dir}",
                "--https-url", f"https://{username}:{password}@dl.ash2txt.org/", "--progress",
                f"--multi-thread-streams={threads}", f"--transfers={threads}"], check=True)
    
if __name__ == "__main__":
    main()