import subprocess


def strip_quotes(value):
    return value.replace("'", "").replace('"', "")


def main():
    base_url = "/fragments/Frag4/PHercParis1Fr39.volpkg/working/54keV_exposed_surface"
    target_dir = "./"

    # Number of threads to use for downloading, 
    # ideally enough to saturate the network but not more
    # to prevent unnecessary switching overhead
    threads = 8

    data_selection = input("would you like to download the final outputs, or all the fragment surface files? default to final outputs (all/final): ")

    if data_selection == "all":
        subprocess.run(["rclone", "copy", f":http:{base_url}", f"{target_dir}",
                        "--http-url", f"https://dl.ash2txt.org/", "--progress",
                        f"--multi-thread-streams={threads}", f"--transfers={threads}"], check=True)
    else:
        subprocess.run(["rclone", "copy", f":http:{base_url}/PHercParis1Fr39_54keV_surface_volume", f"{target_dir}surface_volume",
                        "--http-url", f"https://dl.ash2txt.org/", "--progress",
                        f"--multi-thread-streams={threads}", f"--transfers={threads}"], check=True)
        
        additional_files = ["extras/PHercParis1Fr39_54keV_ir.png","PHercParis1Fr39_54keV_inklabels.png","extras/PHercParis1Fr39_54keV.tif","PHercParis1Fr39_54keV_mask.png"]
        for file in additional_files:
            subprocess.run(["rclone", "copy", f":http:{base_url}/{file}", f"{target_dir}",
                        "--http-url", f"https://dl.ash2txt.org/", "--progress",
                        f"--multi-thread-streams={threads}", f"--transfers={threads}"], check=True)


if __name__ == "__main__":
    main()
