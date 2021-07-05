# List Download
This is a Python script to download multiple different file with same PREFIX and SUFFIX, but different number inside the file (very common in serial files)

For example:

```
https://www.eyesonanime.org/DDL/ANIME/BlackClover/BlackClover_Ep_01_SUB_ITA.mp4
https://www.eyesonanime.org/DDL/ANIME/BlackClover/BlackClover_Ep_02_SUB_ITA.mp4
...
https://www.eyesonanime.org/DDL/ANIME/BlackClover/BlackClover_Ep_10_SUB_ITA.mp4
... and so on
```

### Script Install:

To install this script and use from terminal every where you are following this guide:

```bash
cd ~/Documents/ # or any where you want download
git clone https://github.com/Alfystar/listDownload.git
cd listDownload
source install.sh
source ~/.profile # to add path on current terminal
```

After reboot, the path will be add on all path in all environment, until the rebooting you have to execute in any new terminal `source ~/.profile`.

### Script usage:

Possible example to use the command do download list of anime are:

```bash
listDownload.py https://www.eyesonanime.org/DDL/ANIME/BlackClover/BlackClover_Ep_ _SUB_ITA.mp4 1 20 -p 100 -d 1 -q
```

For case with big number of tiny file where the digit aren't always 2:

```bash
listDownload.py https://www.egr.msu.edu/~khalil/NonlinearSystems/Sample/Lect_ .pdf 1 41 -p 100 -d 1 -q
```

More over, if you have to download form different site and with different macro url, it's possible create list in a file, and next use the software to parallelize the download in efficient manner:

Create file named, for example, `test.txt`:

```
https://www.egr.msu.edu/~khalil/NonlinearSystems/Sample/Lect_ .pdf 1 5 -p 100 -d 1 -o test1
https://www.egr.msu.edu/~khalil/NonlinearSystems/Sample/Lect_ .pdf 10 15 -p 100 -d 1 -o "test 2"
https://www.egr.msu.edu/~khalil/NonlinearSystems/Sample/Lect_ .pdf 20 25 -p 100 -d 1
```

and next call the software (remember, `test.txt` is the path where the file is saved):

```bash
listDownload.py -i test.txt -o testDir
```

with this output

```
.
├── testDir
│   ├── Lect_20.pdf
│   ├── Lect_21.pdf
│   ├── Lect_22.pdf
│   ├── Lect_23.pdf
│   ├── Lect_24.pdf
│   └── Lect_25.pdf
├── test1
│   ├── Lect_1.pdf
│   ├── Lect_2.pdf
│   ├── Lect_3.pdf
│   ├── Lect_4.pdf
│   └── Lect_5.pdf
├── test_2
│   ├── Lect_10.pdf
│   ├── Lect_11.pdf
│   ├── Lect_12.pdf
│   ├── Lect_13.pdf
│   ├── Lect_14.pdf
│   └── Lect_15.pdf
└── test.txt

```





### Script man

```
listDownload.py <baseUrl> <endUrl> <startNum> <endNum> [Options]
        baseUrl:= First part of the url (until XX number)
        endUrl:= Second part of the url (after XX number)
        startNum:= First index included
        endNum:= Last index (included)
[Options]:
                 -p --parallelDownload <int> Number of concurrency downdload (default = 5)
                 -o --outSave <path> Saving directory Path (default = ./listDowndload)
                 -d --digit <digit> Number of digit (default = 2)
                 --quiet no show all data

 Is also possible setup multiple download in a File:
./parallelDownload.py -i <File List> [Options All]
[Options All]:
                 -p --parallelDownload <int> Number of concurrency downdload (default = 5)
                 --quiet no show all data

[File List syntax]:
For EVERY LINE the syntax MUST be is:
<baseUrl> <endUrl> <startNum> <endNum> [Options file]
[Options file] (in case of missing, the global option will be used:
                 -o --outSave <path> Saving directory Path (default = see global)
                 -d --digit <digit> Number of digit (default = see global)
```

### Capability
- Cross Platform, boot Linux and Windows
- Real parallel download customizable
- Parametric Digit of the number
- Output direcory choosable and recursivly create
- File Setup for multiple download in multiple sub directory
- Debug info

#### Linux dependace
- wget (default)
- xterm (default)

#### Linux dependace
- Invoke-WebRequest(default)


### Future Work
- Multiple terminal for Windows
-Gui