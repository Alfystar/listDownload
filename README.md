# Parallel File Manager
This is a Python script to download differen file with same PREFIX and SUFFIX, but different number inside the file (very common in serial files)

### Script usage:

```
./parallelDownload.py <baseUrl> <endUrl> <startNum> <endNum> [Options]
        baseUrl:= First parto of the url (until XX number)
        endUrl:= Second parto of the url (after XX number)
        startNum:= First index included
        endNum:= Last index (included)

 Is also possible setup multiple download in a File:
./parallelDownload.py -i <File List> [option]
[Options]:
                 -p --parallelDownload <int> Number of concurrency downdload (default = 5)
                 -o --outSave <path> Saving directory Path (default = ./parallelDowndload)
                 -d --digit <digit> Number of digit (default = 2)
                 --quiet no show all data

[File List syntax]:
For EVERY LINE the syntax MUST be is:
<baseUrl> <endUrl> <startNum> <endNum> [Options file]
[Options file] (in case of missing, the default option will be used:
                 -o --outSave <path> Saving directory Path (default = ./parallelDowndload)
                 -d --digit <digit> Number of digit (default = 2)

```

### Capability
- Real parallel download customizable
- Parametric Digit of the number
- Output direcory choosable and recursivly create
- File Setup for multiple download in multiple sub directory
- Debug info

#### Linux dependace
- wget (default)
- xterm (default)

### Future Work
Enable file list to program multiple download