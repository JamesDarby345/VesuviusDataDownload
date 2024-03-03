import os
import re
import subprocess
from tempfile import NamedTemporaryFile

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

def get_valid_range(s, e, scrollZAxis):
    # Ensure start is the lower of s or e, but not less than 0
    start = max(min(s, e), 0)
    
    # Ensure end is the higher of s or e, but not more than scrollZAxis
    end = min(max(s, e), scrollZAxis)
    
    return start, end

#faster to download individual files like this if there are only a few
def download_range_or_file(start, end, base_url, target_dir, username, password, threads, usingVC=True):
    if start == end:
        filename = f"{start:05}.tif"
        print(f"Downloading {filename}...")
        subprocess.run(["rclone", "copy", f":http:{base_url}{filename}", f"{target_dir}",
                "--http-url", f"http://{username}:{password}@dl.ash2txt.org/", "--progress",
                f"--multi-thread-streams={threads}", f"--transfers={threads}"], check=True)

    else:
        for i in range(start, end + 1):
            filename = f"{i:05}.tif"
            subprocess.run(["rclone", "copy", f":http:{base_url}{filename}", f"{target_dir}",
                            "--http-url", f"http://{username}:{password}@dl.ash2txt.org/", "--progress",
                            f"--multi-thread-streams={threads}", f"--transfers={threads}"], check=True)
            
    if usingVC:
        subprocess.run(["rclone", "copy", f":http:{base_url}meta.json", f"{target_dir}",
                        "--http-url", f"http://{username}:{password}@dl.ash2txt.org/", "--progress",
                        f"--multi-thread-streams={threads}", f"--transfers={threads}"], check=True)

# uses --files-from flag to download a list of files, 
# faster & better reporting than many individual file downloads <- unsure exactly where the threshold is
def download_range(remote_path, target_dir, file_list, username, password, threads, usingVC=True):
    # Create a temporary file to list the files to download
    with NamedTemporaryFile(mode='w', delete=False) as temp_file:
        for file in file_list:
            temp_file.write(f"{file}\n")
        if usingVC:
            temp_file.write("meta.json\n")
        temp_file_path = temp_file.name

    # Use the temporary file with the --files-from option in rclone
    # to leverage multi threaded downloads and better reporting than individual file downloads
    try:
        subprocess.run(["rclone", "copy", f":http:{remote_path}", f"{target_dir}",
                        "--http-url", f"http://{username}:{password}@dl.ash2txt.org/", 
                        "--files-from", temp_file_path, "--progress",
                        f"--multi-thread-streams={threads}", f"--transfers={threads}"], check=True)
    finally:
        os.remove(temp_file_path)

def main():
    load_env_variables()
    username = get_env_variable("USERNAME", "username? ")
    password = get_env_variable("PASSWORD", "password? ")

    scrollZAxis = 14375
    scrollNum = "1"
    scanId = "20230205180739"

    #TODO: decide if we just want to default to yes and not ask?
    #creates an extra prompt as is
    #but if a user didnt want to use VC, the VC format would be fine, but would create an extra .volpkg dir level
    #and download the config.json and meta.json files which isnt necessary, but also not a big deal
    #the all command downloads meta.json anyway
    #probably not worth the dev effor to switch from whats implemented tbh
    #this is the 80 of the 80/20

    usingVC = input("Are you planning to use these volumes for Volume Cartograher? (default yes) (yes/no): ")
    range_input = input("Specify a range of .tifs volumes to download, or all (Ex: [0-1000,3000,4000-5000] or all): ")

    if range_input != "all" and not re.match(r'^(\[[0-9]{1,5}(-[0-9]{1,5})?(,[0-9]{1,5}(-[0-9]{1,5})?)*\])$', range_input):
        print(f"Unexpected format: {range_input}")
        print(f"Please use 'all' or the format [start-end,start-end,number] with valid scroll1 .tif volume numbers (0-{scrollZAxis})")
        return

    base_url = f"/full-scrolls/Scroll1.volpkg/volumes/{scanId}/"

    # Number of threads to use for downloading, 
    # ideally enough to saturate the network but not more
    # to prevent unnecessary switching overhead
    threads = 8

    if usingVC.strip().lower() == "no" or usingVC.strip().lower() == "n":
        target_dir = f"./volumes/{scanId}/"
        usingVC = False
    else:
        # If using Volume Cartographer, download the config.json file and set target_dir to be a .volpkg directory
        subprocess.run(["rclone", "copy", f":http:/full-scrolls/Scroll{scrollNum}.volpkg/config.json", f"./Scroll{scrollNum}.volpkg/",
                        "--http-url", f"http://{username}:{password}@dl.ash2txt.org/", "--progress",
                    f"--multi-thread-streams={threads}", f"--transfers={threads}"], check=True)
        
        target_dir = f"./Scroll{scrollNum}.volpkg/volumes/{scanId}/"
        usingVC = True

    if range_input == "all":
        subprocess.run(["rclone", "copy", f":http:{base_url}", f"{target_dir}",
                        "--http-url", f"http://{username}:{password}@dl.ash2txt.org/", "--progress",
                        f"--multi-thread-streams={threads}", f"--transfers={threads}"], check=True)
    else:
        ranges = re.findall(r'([0-9]+)-?([0-9]*)', range_input.strip('[]'))
        file_list = []
        start_end_list = []
        for start, end in ranges:
            start = int(start)
            end = int(end) if end else start

            #checks for invalid range numbers that bypass regex, but doesnt stop the download
            if start > scrollZAxis or end > scrollZAxis or start < 0 or end < 0:
                print(f"Invalid range: {start}-{end}")
                print(f"Please use valid scroll {scrollNum} .tif volume numbers (0-{scrollZAxis})")
                start, end = get_valid_range(start, end, scrollZAxis)
                print(f"Using valid range: {start}-{end}")
            start_end_list.append((start, end))
            if start == end:
                filename = f"{start:05}.tif"
                file_list.append(filename)
            elif start < end:
                for i in range(start, end + 1):
                    filename = f"{i:05}.tif"
                    file_list.append(filename)
        
        # If the number of files to download is less than some threashold, default 100,
        # download each file individually to avoid the --files-from overhead
        if(len(file_list) < 100):
            for start, end in start_end_list:
                download_range_or_file(start, end, base_url, target_dir, username, password, threads, usingVC)
        else:
            download_range(base_url, target_dir, file_list, username, password, threads, usingVC)

if __name__ == "__main__":
    main()
