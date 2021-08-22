#!/usr/bin/bash
# Install script for List Download in the system for all user

# Verify that the PWD is the listDownload root directory.
CURR_DIR=${PWD##*/}
REQ_CURR_DIR="listDownload"

if [[ $CURR_DIR != $REQ_CURR_DIR ]]; then
	echo "ERROR: Wrong path, this script must be executed inside listDownload repository" 1>&2
	exit
fi

APT_PATH=$(which apt)
PACMAN_PATH=$(which pacman)

if [[ $APT_PATH != "" ]]; then         # verify the presence of the apt manager
    sudo apt update -y
    sudo apt install python3 python3-pip -y
    sudo apt autoremove -y
elif [[ $PACMAN_PATH != "" ]]; then    # verify the presence of the pacman manager
    sudo pacman -Syy
    sudo pacman -S python3 python3-pip -y
else
    echo "This Install script wasn't think for your Pack Manager (Apt or Pacman), please install by yourself the following dependances:"
    echo "install: git xterm python3"
    echo "Thanks for the cooperation =}"
fi

# Python3 dependances
# Django is network testing library
# urwid is TUI library
#   @urwidtrees is library based on urwid

sudo pip3 install Django urwid urwidtrees
sudo chmod +x listdownload.py

REPO_DIR=$(pwd)
cd /usr/local/bin/
sudo ln -s $REPO_DIR/listDownload.py

# Export the current path on Mark this setup task as done.
# printf '\n# List download Path add\nPATH="$PATH:'$REPO_DIR'"\n' >> ~/.profile
