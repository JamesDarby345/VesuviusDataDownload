import subprocess

def strip_quotes(value):
    return value.replace("'", "").replace('"', "")

def main():
    scrollName = "Scroll2"
    scrollNum = 2

    base_url = f"/full-scrolls/{scrollName}/"
    temp_base_url = f"/community-uploads/james/{scrollName}/"
    base_url = temp_base_url
    target_dir = f"./Scroll{scrollNum}_8um.zarr/"
    threads = 8
    filename = f"Scroll{scrollNum}_8um.zarr"

    print(f"Downloading {filename}...")
    print(f":http:{base_url}{filename}")

    subprocess.run(["rclone", "copy", f":http:{base_url}{filename}", f"{target_dir}",
                "--http-url", f"https://dl.ash2txt.org/", "--progress",
                f"--multi-thread-streams={threads}", f"--transfers={threads}"], check=True)
    
if __name__ == "__main__":
    main()