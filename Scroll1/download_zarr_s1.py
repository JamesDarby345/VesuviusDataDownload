import subprocess

def strip_quotes(value):
    return value.replace("'", "").replace('"', "")


def main():
    scrollName = "Scroll1"
    scrollVolpkg = "PHercParis4.volpkg"

    base_url = f"/full-scrolls/{scrollName}/{scrollVolpkg}"
    temp_base_url = f"/community-uploads/james/{scrollName}/"
    base_url = temp_base_url
    target_dir = f"./{scrollName}_8um.zarr/"
    threads = 8
    filename = f"{scrollName}_8um.zarr"

    print(f"Downloading {filename}...")
    print(f":http:{base_url}{filename}")

    subprocess.run(["rclone", "copy", f":http:{base_url}{filename}", f"{target_dir}",
                "--http-url", f"https://dl.ash2txt.org/", "--progress",
                f"--multi-thread-streams={threads}", f"--transfers={threads}"], check=True)
    
if __name__ == "__main__":
    main()
    