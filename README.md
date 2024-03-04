
# Welcome to the Vesuvius Data Download Repo
The purpose of this repo is to remove as much of the fricton and increase the clarity of, what the Vesuvius Data is, what data you want for your use case, and how to download it, as possible. 

It has three major parts.
  - This README file, which explains how to setup and run the python code to download the Vesuvius data.
  - The python files that make many common download use cases much more convinient than writing your own scripts
  - The [wiki pages](https://github.com/JamesDarby345/VesuviusDataDownload/wiki) which explains & contains the following:
     - what the data is
     - the use case for each part of the data
     - (some of) the community developed tools & the data they work best with
     - a quick [data reference handbook](https://github.com/JamesDarby345/VesuviusDataDownload/wiki/Vesuvius-Data-Handbook) for scroll and fragment data sizes, scan id's, scan resolution and keV and dl.ash2txt.org links

## README Table of Contents
- Prerequisites
- [Installation Instructions](#installation-instructions)
- [How to use](#how-to-use)
- Motivation
- Technical Development Decisions
  - semi organized notes on rclone commands
- Refrences/Data Contributions

## Prerequisites
1. I assume some fundamental knowledge of how to navigate into directories with a terminal & how to run python files. 
There are many great tutorial on this, and if you ever get stuck on this, or anything else in this repo, or challenge, we live in a post [chatGPT](https://chat.openai.com/) world, and these two things are well within its capabilities to explain, so ask it to help! Asking clear questions with as much context as is reasonable helps to get better responses back.

2. Before proceeding, you must agree to the [data license](https://docs.google.com/forms/d/e/1FAIpQLSf2lCOCwnO1xo0bc1QdlL0a034Uoe7zyjYBY2k33ZHslHE38Q/viewform) to be provided the username and password for the data server. This login is required to use the download scripts in this repo.

## Installation Instructions
1. Navigate into the directory you would like to have this repo, and thus your data, in. Then run the following command to clone the repo to your local computer
```
git clone https://github.com/JamesDarby345/VesuviusDataDownload.git
```
2. The only dependency the repo uses that isnt already included with python is rclone. How to install it so it is accesible from the command line is OS dependant.
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
   
6. Add the path to the folder where you extracted rclone (e.g., C:\rclone) and Click "OK" to close all dialogs. You can copy paste is from the top bar of file explorer if you are in the directory with the rclone.exe file if you didnt save it from before.
   
   <img width=400 alt="Paste path to rclone" src=https://github.com/JamesDarby345/VesuviusDataDownload/assets/49734270/d8f93ae3-5fb3-4d0e-8909-79cffa53b25d><br>


**Verify Installation:**
Open a new Command Prompt and type the below command to verify the installation.<br>
```
rclone --version
```

## MacOS
**Homebrew**
If you dont already have homebrew, install it by running the following command in a terminal
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


## Linux
**Download and Install Rclone:**
Open Terminal.
You can download and install rclone using the script provided by the rclone team. This method automatically downloads the correct version and adds it to your PATH:
```
curl https://rclone.org/install.sh | sudo bash
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

## How to use
   
## Motivation
The download.sh file in Youssef's GP Ink Detection model works great for its use case, downloading all the segments used to train the ink detection model. But .sh doesnt work natively on windows, also the 100+ lines of mostly similar rclone commands with only a few parameters changing slightly triggered my software engineering senses that there must be a better way than this. After deiciding, maybe I want to look at all the unified segment .tifs as well, and having to write a script to edit the download.sh script to add them all in, I thought writing a script to edit a script is surly a sign of something not quite right, and this is getting annoying, even for me, a fairly technically adept user. These thoughts bounced around in my head until I made some time to create a better version. This is the result of that effort. This is not the final say on the matter, but it is a solid incremental improvement. 

## Technical Development Decisions
I have choosen to use python, as unlike .sh, bash or powershell scripts, python is portable across all OS's, and is as easy to understand, use and modify as reasonably possible.

I have choosen to use rclone as the underlying download command as it can sync files, instead of just downloading them like wget. 
This means if a download is interrupted, the exact same rclone command can be run again to download the rest of the files (including finishing partially downloaded files),
without re-downloading the files that are already downloaded! A very handy feature when downloading TB's of data that may get interrupted. 

I could of made the files into generalized download files, or even just one python file, instead of creating a version for data type for each scroll and fragment. But I wanted this repo to be as easy to use and free of oh uh, did I mess up moments as possible. I deicided enforcing/suggesting a reasonable data file structure by providing it as the default in the repo and then putting download files that do what they are named in each folder that then download the data into a folder next to them had some advantages over a more flexible script. This way the user doesnt need to worry about creating a directory structure themselves, reducing friction, and with rclone being able to sync files instead of redownloading themm, making the default behaviour downloading to the same place, unless the files are moved, makes that a ubiquiotus process the user doesnt even need to think about. Compared to making sure they specify the same download location as last time, this seemed like a better solution. The code also creates folders that seperate and put layers between the non-unique .tif names, making accidentally overwriting previous data imossible without modifying the code, something that made me very sad in the past when I may or may not of done that.
Is this repo perfect? of course not, one sore spot is what if the data is stored over multiple disks? But I think this is a solid incremental improvement over the figure it out yourself system for most users.

### Semi-organized notes on rclone commands:

If your download stops half way, you can simply re-run it as rclone will not redownload any files that match and are the same size, this means even if one file is only half downloaded, simply re-running the command will fix it as well as not re download everything you already have in the target directory!

The typical rclone command pattern is:

rclone copy "url in the server, Note 1" "local directory path to download to, Note 2" --http-url "http://${USERNAME}:${PASSWORD}@dl.ash2txt.org/" --progress --multi-thread-streams=8 --transfers=8

The design is to whenever reasonable take all the files the user wants, and combine them into one rclone command. This is so rclone can handle the parallelism, as well as provide total size, download rate and eta information which is useful for the user, so they know about how it will take, and if they need to scale back their download due to space constraints etc. This does cause an around ~1 min delay as rclone 'starts up' so for smaller downloads I just use multiple sequential rclone commands. rclone appears to download small amounts of data faster this way without the --file-from flag startup cost, though this is untested. The feedback is faster anyway so it is a better user experience.

Note 1: an example is ":http:/full-scrolls/Scroll1.volpkg/volumes/20230205180739" 
in dl.ash2txt.org you can simply copy the url in the browser.
![url from browser](<Example_dlash2text_url.png>)

Note 2: this can either be an absolute path, typically copied from a file explorer, or from the 
command line, but it can also be a relative path from where the rclone is being run.
An example is putting "./scroll1" and rclone will make that directory in its location and copy the files there

The user name and password are the ones provided to you after  agreeing to the data lisence
the last couple --flags are progress, so you can see how the download is progressing in the terminal,
and --multi-thread-streams=8 --transfers=8 which allow rclone to download multiple files at once if it can.

This repo is using python subprocesses to run the rclone commands to add some additonal logic to make downloads easier and more customizable, while maintaining native portability across operating systems which would be lost is .sh, bash or .bat etc scripts were used.

## Refrences/Data Contributions
EduceLabs scanned and provided the foundational data we are working with, the Volumes & Fragments

@Spelufo on discord generously open sourced the pherc_0332_53.csv and scroll_1_54_mask.csv volume grid masks, as well as developing the code to create the volume grids.

@james darby on discord developed the code and masked the .tifs for scroll 1 & 2
