import os
import subprocess
import csv
from tempfile import NamedTemporaryFile

def generate_layers_file_list(dir_ids, base_remote_path, type="layers"):
    file_list = []
    for dir_id in dir_ids:
        try:
            # Use rclone to list files in each layers directory, appending the directory ID to maintain structure
            # command = f"rclone lsf {remote_name}:{base_remote_path}{dir_id}/layers --recursive"
            file_paths = ""
            if type == "all":
                file_paths = subprocess.check_output(["rclone", "lsf", f":http:{base_remote_path}{dir_id}",
                            "--http-url", f"https://dl.ash2txt.org/","--recursive"],text=True)

            if type == "obj":
                file_paths = f"{dir_id}.obj"
              
            layer_paths = subprocess.check_output(["rclone", "lsf", f":http:{base_remote_path}{dir_id}/layers",
                            "--http-url", f"https://dl.ash2txt.org/","--recursive"],text=True)

            for layer_path in layer_paths.strip().split('\n'):
                # Check if the file_path is not empty
                if layer_path:
                    # Append the full remote path of each file to the file_list
                    full_path = f"{dir_id}/layers/{layer_path}"
                    file_list.append(full_path)

            for file_path in file_paths.strip().split('\n'):
                # Check if the file_path is not empty
                if file_path:
                    # Append the full remote path of each file to the file_list
                    full_path = f"{dir_id}/{file_path}"
                    file_list.append(full_path)
        except subprocess.CalledProcessError as e:
            print(f"Error listing files in {dir_id}/layers: {e}")
    return file_list

def download_from_file_list(base_url, target_dir, file_list, threads):
    # Create a temporary file to list the files to download
    with NamedTemporaryFile(mode='w', delete=False) as temp_file:
        for file in file_list:
            temp_file.write(f"{file}\n")
        temp_file_path = temp_file.name

    # Use the temporary file with the --files-from option in rclone
    # to leverage multi threaded downloads and better reporting than individual file downloads
    try:
        subprocess.run(["rclone", "copy", f":http:{base_url}", f"{target_dir}",
                    "--http-url", f"https://dl.ash2txt.org/", 
                    "--files-from", temp_file_path, "--progress",
                    f"--multi-thread-streams={threads}", f"--transfers={threads}"], check=True)
    finally:
        os.remove(temp_file_path)

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
            for segmentId in row:
                contents.append(segmentId.strip())
    return contents

def comma_separated_string_to_array(s):
    return [element.strip() for element in s.split(',')]

def strip_quotes(value):
    return value.replace("'", "").replace('"', "")

def main():
    base_url = "/full-scrolls/Scroll3/PHerc332.volpkg/paths/"
    target_dir = "./segments"

    # Number of threads to use for downloading, 
    # ideally enough to saturate the network but not more
    # to prevent unnecessary switching overhead
    threads = 8

    data_selection = input("Would you like to download just the layers (default), or the .obj file, or all the segment files? (layers/obj/all): ")
    
    csv_file_path = "./segments_to_download_s3.csv"
    specified_segments = read_csv_to_array(csv_file_path)
    
    if specified_segments == []:
        segments_to_download = input("\nEnter segment id's to download in a comma separated format\nEx: 20231030220150,20231031231220 or all for all segments\nfrom this scroll. You can also specify them\nin the neighboring segments_to_download_s3.csv file (all/id's): ")
    else: 
        segments_to_download = "csv_passed_in_segment_ids"

    if segments_to_download.strip().lower() == "all":
        if data_selection.strip().lower() == "all":
            subprocess.run(["rclone", "copy", f":http:{base_url}", f"{target_dir}",
                            "--http-url", f"https://dl.ash2txt.org/", "--progress",
                            f"--multi-thread-streams={threads}", f"--transfers={threads}"], check=True)
        elif data_selection.strip().lower() == "obj":
            subprocess.run(["rclone", "copy", f":http:{base_url}", f"{target_dir}",
                            "--http-url", f"https://dl.ash2txt.org/", "--progress",
                            f"--multi-thread-streams={threads}", f"--transfers={threads}", 
                             "--include","**/*.obj","--exclude", "**/*_points.obj"], check=True)
        else:
            subprocess.run(["rclone", "copy", f":http:{base_url}", f"{target_dir}",
                            "--http-url", f"https://dl.ash2txt.org/", "--progress",
                            f"--multi-thread-streams={threads}", f"--transfers={threads}", 
                            "--include", "**/layers/**"], check=True)
    else:
        if segments_to_download != "csv_passed_in_segment_ids":
            specified_segments = comma_separated_string_to_array(segments_to_download)


        file_list = generate_layers_file_list(specified_segments, base_url, data_selection.strip().lower())
        download_from_file_list(base_url, target_dir, file_list, threads)


if __name__ == "__main__":
    main()
