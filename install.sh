#!/usr/bin/bash
# Install script for List Download

# Verify that the PWD is the listDownload root directory.
CURR_DIR=${PWD##*/}
REQ_CURR_DIR="listDownload"

if [[ $CURR_DIR != $REQ_CURR_DIR ]]; then
	echo "ERROR: Wrong path, this script must be executed inside listDownload repository" 1>&2
	exit
fi

if [[ ${which apt} != "" ]]; then         # verify the presence of the apt manager
	sudo apt update -y
  sudo apt install git xterm python3 -y
  sudo apt autoremove -y
elif [[ ${which pacman} != "" ]]; then    # verify the presence of the pacman manager
  sudo pacman -Syy
  sudo pacman -S git xterm python3 -y
else
  echo "This Install script wasn't think for your Pack Manager (Apt or Pacman), please install by yourself the following dependances:"
  echo "install: git xterm python3"
  echo "Thanks for the cooperation =}"
fi

sudo chmod +x listDownload.py

REPO_DIR=$(pwd)
# Export the current path on Mark this setup task as done.
printf '\n# List download Path add\nPATH="$PATH:'$REPO_DIR'"\n' >> ~/.profile
