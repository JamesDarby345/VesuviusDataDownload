# Welcome to the Vesuvius Data Download Repo
<p align="center">
<img width=300 alt="Vesuvius data download repo icon" src=https://github.com/JamesDarby345/VesuviusDataDownload/assets/49734270/dfa44677-f063-436d-88b4-e92bb8891848>
</p> 

## Due to path changes on the download server, the repo may not work as intended at the moment

The purpose of this repo is to remove as much of the friction and increase the clarity of, what the Vesuvius Data is, what data you want for your use case, and how to download it, as possible.

It has three major parts.
  - This README file, which explains how to set up and run the python code to download the Vesuvius data.
  - The python files that make many common download use cases much more convenient than writing your own scripts
  - The [wiki pages](https://github.com/JamesDarby345/VesuviusDataDownload/wiki) which explains & contains the following:
     - what the data is
     - the use case for each part of the data
     - (some of) the community developed tools & the data they work best with
     - a quick [data reference handbook](https://github.com/JamesDarby345/VesuviusDataDownload/wiki/Vesuvius-Data-Handbook) for scroll and fragment data sizes, scan id's, scan resolution and keV and dl.ash2txt.org links

## README Table of Contents
- [Prerequisites](#prerequisites)
- [Installation Instructions](#installation-instructions)
- [How to use](#how-to-use)
- [Motivation](#motivation)
- [Technical Development Decisions](#technical-development-decisions)
  - [Semi organized notes on rclone commands](#semi-organized-notes-on-rclone-commands)
- [References/Data Contributions](#referencesdata-contributions)

Do you think anything is missing? Anything unclear? Let me know with a github issue, or a message on discord. Im @james darby on the Vesuvius Server.

## Prerequisites
1. I assume some fundamental knowledge of how to navigate into directories with a terminal, have git and python installed (to clone the repo and run the files) & how to run python files from the command line (cd to the directory, and type python file_name.py). 
There are many great tutorial on this, [All OS Python install](https://kinsta.com/knowledgebase/install-python/), [All OS Git install](https://github.com/git-guides/install-git), [Command line basics](https://tutorials.codebar.io/command-line/introduction/tutorial.html) (you only need to know how to use cd for this repo),  and if you ever get stuck on this, or anything else in this repo, or challenge, we live in a post [chatGPT](https://chat.openai.com/) world, and these three things are well within its capabilities to explain, so ask it to help! Asking clear questions with as much context as is reasonable helps to get better responses back.

2. Before proceeding, you must agree to the [data license](https://docs.google.com/forms/d/e/1FAIpQLSf2lCOCwnO1xo0bc1QdlL0a034Uoe7zyjYBY2k33ZHslHE38Q/viewform) to be provided the username and password for the data server. This login is required to use the download scripts in this repo.

## Installation Instructions
1. Navigate into the directory you would like to have this repo, and thus your data, in. Then run the following command to clone the repo to your local computer
```
git clone https://github.com/JamesDarby345/VesuviusDataDownload.git
```
2. The only dependency the repo uses that isn't already included with python is rclone. How to install it so it is accessible from the command line is OS dependent.
   - [Windows](#windows)
   - [MacOS](#macos)
   - [Linux](#linux)
## Windows
**Download Rclone:**
Visit the [Rclone downloads page](https://rclone.org/downloads/).
Download the zip file for Windows (e.g., rclone-current-windows-amd64.zip for 64-bit systems).

**Extract the ZIP File:**
Right-click the downloaded .zip file and select "Extract All...".
Choose a destination folder where you want to store rclone (e.g., C:\rclone).
Save this destination path as we will use it in the next step.

**Add Rclone to the PATH:**

1. Search for "Edit the system environment variables" in the Start menu and open it.

   <img width=600 alt="windows search bar ex" src=https://github.com/JamesDarby345/VesuviusDataDownload/assets/49734270/16973bce-1d04-49d8-b99d-2bbfbb1531f5>

2. Click the "Environment Variables..." button.

   <img width=400 alt="Environment Variables button" src=https://github.com/JamesDarby345/VesuviusDataDownload/assets/49734270/4f11c8f0-c8eb-4d64-acbf-e4f1ed0f1aa5>

3. Under "System variables", scroll down and select the "Path" variable, then click "Edit...".

   <img width=400 alt="edit path" src=https://github.com/JamesDarby345/VesuviusDataDownload/assets/49734270/f2b9c086-46a0-44b8-a95f-cd56d5b047b9>

4. Click "New" to add a new environment variable
   
   <img width=400 alt="Add new env var" src=https://github.com/JamesDarby345/VesuviusDataDownload/assets/49734270/17fc7782-8709-4e8a-8445-fec759008c43>
   
6. Add the path to the folder where you extracted rclone (e.g., C:\rclone) and Click "OK" to close all dialogs. You can copy paste it from the top bar of file explorer if you are in the directory with the rclone.exe file if you didn't save it from before.
   
   <img width=400 alt="Paste path to rclone" src=https://github.com/JamesDarby345/VesuviusDataDownload/assets/49734270/d8f93ae3-5fb3-4d0e-8909-79cffa53b25d><br>


**Verify Installation:**
Open a new Command Prompt and type the below command to verify the installation.<br>
```
rclone --version
```

[Back to top](#welcome-to-the-vesuvius-data-download-repo)
## MacOS
**Homebrew**
If you don't already have homebrew, install it by running the following command in a terminal
```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
**Brew rclone installation**
Run the following command to install rclone
```
brew install rclone
```

**Verify Installation:**
Once the command completes, open a new terminal and verify the installation by typing:
```rclone --version```

[Back to top](#welcome-to-the-vesuvius-data-download-repo)
## Linux
**Download and Install Rclone:**
Open Terminal.
You can download and install rclone using the script provided by the rclone team. This method automatically downloads the correct version and adds it to your PATH:
```
curl https://rclone.org/install.sh | sudo bash
```
if you don't have curl installed use the following command to install it
```
sudo apt update && sudo apt install curl
```
**Verify Installation:**
Once the script completes, open a new terminal and verify the installation by typing:
```rclone --version```
<br><br><br>
**Once finished,** with rclone installed, the python files should be ready to run! They are designed to run from the command line by navigating to the directory they are in and running them with the below command pattern. 
```
python name_of_file.py
```
Actual examples will follow in the How to use section.

[Back to top](#welcome-to-the-vesuvius-data-download-repo)
## How to use
Basic usage should (hopefully) be fairly simple, run the file you want with python from the command line and input the information it asks for. To know which file you want, and the rest of the details, keep reading.

Use the [data reference wiki](https://github.com/JamesDarby345/VesuviusDataDownload/wiki) (especially [this page](https://github.com/JamesDarby345/VesuviusDataDownload/wiki/Vesuvius-Data-Reference)) to select which kind of data you would like to download. Then navigate to the appropriate folder. 
- The Fragments folder contains Fragment folders 1-6 and their associated fragment surface download file. (download_fragment_surface_fx.py)
- Each Scroll folder contains the download scripts for that Scroll
  - The scroll's Volumes (download_volumes_sx.py)
  - The Masked Volumes for Scroll 1 & 2 (download_masked_volumes_sx.py)
  - The scroll's Volume Grids (download_volume_grids_sx.py)
  - The Segments segmented from that scroll (download_segments_sx.py)

Each file type works a little bit differently, but simply navigating into the folder and running the file with python file_name.py will cause the script to prompt you for the minimal information it needs and will then begin to download. Just doing this should be enough to get you started.

You will notice that each file will prompt you for a username and password, this is to login to the dl.ash2txt.org server, and are the same ones you receive after accepting the data agreement. If like me you quickly get annoyed by putting in the username and password, you can edit (or create if its not there) the ```config.env``` file which is in the top level of the repo, and put the username and password in there and the scripts will use that instead of prompting you. Be careful to not accidentally release the username and password to those who have not agreed to the data license, especially if you contribute to this repo. 

You may also notice that the scripts will load without showing progress for ~1-2 minutes for larger download requests. This is expected as rclone is 'warming up' to download a large number of files efficiently, synchronizing with what you may already have, and will be able to provide download rate, the total download size and approximate ETA reporting once done. Below is what to expect the output to look like when starting the command, and after a few minutes for the larger downloads. 

Output on startup<br>
<img width=600 alt="rclone starting" src=https://github.com/JamesDarby345/VesuviusDataDownload/assets/49734270/1e6fc52b-5867-49b3-8e53-843a017c78fc><br><br>
Output after startup complete<br>
<img width=600 alt="rclone running" src=https://github.com/JamesDarby345/VesuviusDataDownload/assets/49734270/8ede1eb8-dfda-476d-9d78-cb18597368cc>

All that's left to do is wait for a few seconds to a few days, depending on how much data you requested, and how fast your internet is. But over a few days many unexpected things could happen such as power outages, people complaining the internet is slow, or the dog eating the router. But do not worry, as long as your computer didn't blow up and the downloaded files are still intact, you didn't lose any progress. 

In fact the download can be stopped at any time with ```Ctrl+C``` in the terminal window or closing the terminal itself. When you want to continue the download, just re-run the file again. rclone will realize you already have some of the files and move on to the next one without downloading (if it is the same size as the one it's trying to download). This means it will even re-download partially downloaded files. Additionally the scripts make nice folder structures for each data type, so accidentally overwriting data by running these (unchanged) scripts will not happen.

If you want more details on what exactly an option does or how one of the download scripts work, a wiki page for that is in the works and will be linked here soon. 

Hope your download goes well and that you help us read the scrolls! And if you have read this far and think this repo will be helpful, I wouldn't mind a star on it :)

[Back to top](#welcome-to-the-vesuvius-data-download-repo)
## Motivation
The download.sh file in Youssef's GP Ink Detection model works great for its use case, downloading all the segments used to train the ink detection model. But .sh doesnt work natively on windows, also the 100+ lines of mostly similar rclone commands with only a few parameters changing slightly triggered my software engineering senses that there must be a better way than this. After deciding, maybe I want to look at all the unified segment .tifs as well, and having to write a script to edit the download.sh script to add them all in, I thought writing a script to edit a script is surly a sign of something not quite right, and this is getting annoying, even for me, a fairly technically adept user. These thoughts bounced around in my head until I made some time to create a better version. This is the result of that effort. This is not the final say on the matter, but it is a solid incremental improvement. 

[Back to top](#welcome-to-the-vesuvius-data-download-repo)
## Technical Development Decisions
I have chosen to use python, as unlike .sh, bash or powershell scripts, python is portable across all OS's, and is as easy to understand, use and modify as reasonably possible.

I have chosen to use rclone as the underlying download command as it can sync files, instead of just downloading them like wget. 
This means if a download is interrupted, the exact same rclone command can be run again to download the rest of the files (including finishing partially downloaded files),
without re-downloading the files that are already downloaded! A very handy feature when downloading TB's of data that may get interrupted. 

I could have made the files into generalized download files, or even just one python file, instead of creating a version for data type for each scroll and fragment. But I wanted this repo to be as easy to use and free of oh uh, did I mess up moments as possible. I decided enforcing/suggesting a reasonable data file structure by providing it as the default in the repo and then putting download files that do what they are named in each folder that then download the data into a folder next to them had some advantages over a more flexible script. This way the user does not need to worry about creating a directory structure themselves, reducing friction, and with rclone being able to sync files instead of redownloading decided, making the default behavior downloading to the same place, unless the files are moved, makes that a ubiquitous process the user doesn't even need to think about. Compared to making sure they specify the same download location as last time, this seemed like a better solution. The code also creates folders that separate and put layers between the non-unique .tif names, making accidentally overwriting previous data impossible without modifying the code, something that made me very sad in the past when I may or may not have done that.
Is this repo perfect? Of course not, one sore spot is what if the data is stored over multiple disks? But I think this is a solid incremental improvement over the figure it out yourself system for most users.

[Back to top](#welcome-to-the-vesuvius-data-download-repo)
  ### Semi-organized notes on rclone commands

If your download stops halfway, you can simply re-run it as rclone will not redownload any files that match and are the same size, this means even if one file is only half downloaded, simply re-running the command will fix it as well as not re download everything you already have in the target directory!

The typical rclone command pattern is:

rclone copy "url in the server, _Note 1_" "local directory path to download to, _Note 2_" --http-url "https://dl.ash2txt.org/" --progress --multi-thread-streams=8 --transfers=8

The design is to whenever reasonable take all the files the user wants, and combine them into one rclone command. This is so rclone can handle the parallelism, as well as provide total size, download rate and eta information which is useful for the user, so they know about how it will take, and if they need to scale back their download due to space constraints etc. This does cause an around ~1 min delay as rclone 'starts up' so for smaller downloads I just use multiple sequential rclone commands. rclone appears to download small amounts of data faster this way without the --file-from flag startup cost, though this is untested. The feedback is faster anyway so it is a better user experience.

_Note 1_: an example is ":http:/full-scrolls/Scroll1.volpkg/volumes/20230205180739" 
in dl.ash2txt.org you can simply copy the url in the browser.
![url from browser](<Example_dlash2text_url.png>)

_Note 2_: this can either be an absolute path, typically copied from a file explorer, or from the 
command line, but it can also be a relative path from where the rclone is being run.
An example is putting "./scroll1" and rclone will make that directory in its location and copy the files there

The user name and password are the ones provided to you after  agreeing to the data license
the last couple --flags are progress, so you can see how the download is progressing in the terminal,
and --multi-thread-streams=8 --transfers=8 which allow rclone to download multiple files at once if it can.

This repo is using python subprocesses to run the rclone commands to add some additional logic to make downloads easier and more customizable, while maintaining native portability across operating systems which would be lost if .sh, bash or .bat etc scripts were used.

[Back to top](#welcome-to-the-vesuvius-data-download-repo)
## References/Data Contributions
EduceLabs scanned and provided the foundational data we are working with, the Volumes & Fragments

@Spelufo on discord generously open sourced the pherc_0332_53.csv and scroll_1_54_mask.csv volume grid masks, as well as developing the code to create the volume grids.

@james darby on discord developed the code and masked the .tifs for scroll 1 & 2

[Back to top](#welcome-to-the-vesuvius-data-download-repo)
