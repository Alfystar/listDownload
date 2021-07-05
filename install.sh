#!/usr/bin/bash
# Install script for List Download



# Verify that the PWD is the listDownload root directory.
CURR_DIR=${PWD##*/}
REQ_CURR_DIR="listDownload"

if [[ $CURR_DIR != $REQ_CURR_DIR ]]; then
	echo "ERROR: Wrong path, this script must be executed inside listDownload repository" 1>&2
	exit
fi

REPO_DIR=$(pwd)

sudo apt update -y
sudo apt install git xterm python3 -y
sudo apt autoremove -y

sudo chmod +x listDownload.py

# Export the current path on Mark this setup task as done.
printf '\n# List download Path add\nPATH="$PATH:'$REPO_DIR'"\n' >> ~/.profile
