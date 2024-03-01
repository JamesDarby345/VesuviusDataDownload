import os
import re
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

def download_range_or_file(start, end, base_url, target_dir, username, password):
    if start == end:
        filename = f"{start:05}.tif"
        print(f"Downloading {filename}...")
        subprocess.run(["rclone", "copy", f":http:{base_url}{filename}", f"{target_dir}",
                "--http-url", f"http://{username}:{password}@dl.ash2txt.org/", "--progress",
                "--multi-thread-streams=8", "--transfers=8"], check=True)

    else:
        for i in range(start, end + 1):
            filename = f"{i:05}.tif"
            subprocess.run(["rclone", "copy", f":http:{base_url}{filename}", f"{target_dir}",
                            "--http-url", f"http://{username}:{password}@dl.ash2txt.org/", "--progress",
                            "--multi-thread-streams=8", "--transfers=8"], check=True)

def main():
    load_env_variables()
    username = get_env_variable("USERNAME", "username? ")
    password = get_env_variable("PASSWORD", "password? ")

    range_input = input("Specify a range of .tifs volumes to download, or all (Ex: [0-1000,3000,4000-5000] or all): ")

    if range_input != "all" and not re.match(r'^(\[[0-9]+(-[0-9]+)?(,[0-9]+(-[0-9]+)?)*\])$', range_input):
        print(f"Unexpected format: {range_input}")
        print("Please use the format [start-end,start-end,number] or all")
        return

    base_url = "/full-scrolls/Scroll1.volpkg/volumes/20230205180739/"
    target_dir = "./volumes/20230205180739/"

    if range_input == "all":
        subprocess.run(["rclone", "copy", f":http:{base_url}", f"{target_dir}",
                        "--http-url", f"http://{username}:{password}@dl.ash2txt.org/", "--progress",
                        "--multi-thread-streams=8", "--transfers=8"], check=True)
    else:
        ranges = re.findall(r'([0-9]+)-?([0-9]*)', range_input.strip('[]'))
        for start, end in ranges:
            start = int(start)
            end = int(end) if end else start
            download_range_or_file(start, end, base_url, target_dir, username, password)

if __name__ == "__main__":
    main()
