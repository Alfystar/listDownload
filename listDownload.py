#!/usr/bin/python3
# Test normal
# https://www.egr.msu.edu/~khalil/NonlinearSystems/Sample/Lect_ .pdf 1 41 -p 100 -d 1 --quiet
# Test file:
# -i test.txt -o testDir

import os
import shlex
import sys
from datetime import datetime

# Personal Lib
from src.ArgParse import *
from src.runDownload import *

def helpMan():
    print("a)\tlistDownload.py <baseUrl> <endUrl> <startNum> <endNum> [Global-Options] # One Download block")
    print("\t Or:")
    print("b)\tlistDownload.py <File List>                                             # Multiple-block download")

    print("\n<Mandatory Parameters>")
    print("\tbaseUrl:= First part of the url (until XX number)")
    print("\tendUrl:= Second part of the url (after XX number)")
    print("\tstartNum:= First index included")
    print("\tendNum:= Last index (included)")
    print("[Global-Options]:")
    print("\t\t -p --listDownload <int> Number of concurrency download (default = 5)")
    print("\t\t -o --outSave <path> Saving directory Path (default = ./listDownload)")
    print("\t\t -d --digit <digit> Number of digit (default = 2)")
    print("\t\t -q --quiet no show all data")
    print("\t\t -v --verbose show all data by Xterm support Terminal")

    print("\n[File Sintax]:")
    print("The file permits to the user to define a more complex list of download, with very simple syntax:")
    print("[1°Line]\t[Global-Options]")
    print("[i°Line]\t <Mandatory Parameters> [Local-Options]")

    print("[Local-Options] (in case of missing, the global option will be used:")
    print("\t\t -o --outSave <path> Saving directory Path (default = see global)")
    print("\t\t -d --digit <digit> Number of digit (default = see global)")

    print("\n[Comment Sintax]:")
    print("Is possible add comment at the end of the line using '#' or '//',")
    print("all the text present after this character will be ignore ")

    print("\n[1° line] Description:")
    print("The First line with the [Global-Options] sintax select the default behaviour for all line")
    print("this line can be OMITTED, in this case system-default param are used instead")
    print("When OMITTED the first line could be write as general [i° line]")

    print("\n[i° line] Description:")
    print("Any i-line is another download list, with him is possible set the ")
    print("this line can be OMITTED, and system-default param are used instead")

    print("You type the command:")
    print(sys.argv[1:])
    exit(-1)


def main():
    helpMan()
    urlListInit()

    print("The download start with " + str(pDW) + " parallel Connection")
    print("Output quiet = " + str(quite) + " My Current Work Directory is: " + os.getcwd())

    # Start parallel procedure
    start_time = datetime.now()

    nDownload = downloadList()

    time_elapsed = datetime.now() - start_time
    print("## Downloads end ##")
    print('Total Time (hh:mm:ss.ms) {}'.format(time_elapsed))
    print('Mean Time General(hh:mm:ss.ms) {}'.format(time_elapsed / nDownload))
    print('Mean Time x File (hh:mm:ss.ms) {}'.format(time_elapsed * min(pDW, nDownload) / nDownload))
    print('Concurrency Download :' + str(min(pDW, nDownload)))


if __name__ == '__main__':
    main()
