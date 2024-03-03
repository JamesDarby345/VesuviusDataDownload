import os
import subprocess
import csv

def read_csv_to_array(file_path):
    """
    Reads a CSV file and returns its contents as a list of lists.
    
    :param file_path: Path to the CSV file.
    :return: List of lists, where each sublist represents a row in the CSV.
    """
    contents = []
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            contents.append(row)
    return contents

def comma_separated_string_to_array(s):
    return [element.strip() for element in s.split(',')]

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

    base_url = "/full-scrolls/PHerc0332.volpkg/paths/"
    target_dir = "./segments"

    # Number of threads to use for downloading, 
    # ideally enough to saturate the network but not more
    # to prevent unnecessary switching overhead
    threads = 8

    data_selection = input("Would you like to download just the layers (default), or also the .obj file, or all the segment files? (layers/obj/all): ")
    
    csv_file_path = "./segments_to_download.csv"
    specified_segments = read_csv_to_array(csv_file_path)
    
    if specified_segments == []:
        segments_to_download = input("\nEnter segment id's to download in a comma seperated format Ex: 20231030220150,20231031231220 or all for all segments\nfrom this scroll. You can also specify them in the neighbouring segments_to_download.csv file (all/id's): ")
    else: 
        segments_to_download = "csv_passed_in_segment_ids"

    if segments_to_download.strip().lower() == "all":
        if data_selection.strip().lower() == "all":
            subprocess.run(["rclone", "copy", f":http:{base_url}", f"{target_dir}",
                            "--http-url", f"http://{username}:{password}@dl.ash2txt.org/", "--progress",
                            f"--multi-thread-streams={threads}", f"--transfers={threads}"], check=True)
        elif data_selection.strip().lower() == "obj":
            subprocess.run(["rclone", "copy", f":http:{base_url}", f"{target_dir}",
                            "--http-url", f"http://{username}:{password}@dl.ash2txt.org/", "--progress",
                            f"--multi-thread-streams={threads}", f"--transfers={threads}", 
                            "--include", "**/layers/**", "--include","**/*.obj","--exclude", "**/*_*.obj"], check=True)
        else:
            subprocess.run(["rclone", "copy", f":http:{base_url}", f"{target_dir}",
                            "--http-url", f"http://{username}:{password}@dl.ash2txt.org/", "--progress",
                            f"--multi-thread-streams={threads}", f"--transfers={threads}", 
                            "--include", "**/layers/**"], check=True)
    else:
        print("passed in a list of segments to download")
        if segments_to_download != "csv_passed_in_segment_ids":
            specified_segments = comma_separated_string_to_array(segments_to_download)

        #add files to a temp file list to download with files from flag
        #similar to how download volumes works
        for segment in specified_segments:

            print(f"Downloading segment {segment}")
        


if __name__ == "__main__":
    main()
