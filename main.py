#!/usr/bin/python3.8

import sys
import os
import time
from datetime import datetime 
import platform

# Parametri Obbligatori
baseUrl = ""
endUrl = ""
startNum = 0
endNum = 0

# Parametri Facoltativi
pWget = 5
digit = 2


def help():
    print("correct syntax is:")
    print("main.py <baseUrl> <endUrl> <startNum> <endNum> [Options]")
    print("\tbaseUrl:= Prima parte dell'url fissa fino ai numeri XX")
    print("\tendUrl:= Seconda parte dell'url fissa dopo i numeri XX")
    print("\tstartNum:= Primo episodio da scaricare")
    print("\tendNum:= Ultimo episodio da scaricare (Compreso)")
    print("[Options]:")
    print("\t\t -p --parallelWget <Number> Quante istanze di wget in parallelo, 5 default")
    print("\t\t -o --outSave <path> Path su cui salvare, di default la corrente")
    print("\t\t -d --digit <numDigit> Numero di caratteri obbligatori, default 2")

    print("You type the command:")
    print(sys.argv[1:])  # Press Ctrl+8 to toggle the breakpoint.
    exit(-1)


def optionSet(argList):
    # Ritorna la subList
    op = argList[0]
    
    if op == "-p" or op == "--parallelWget":
        val = argList[1]
        if (val.isnumeric()):
            global pWget
            pWget = int(val)
            print("pWget assegnata pari a: "+ str(pWget))
            return argList[2:]
        else:
            help()

    elif op == "-o" or op == "--outSave":
        val = argList[1]

        if not os.path.exists(val):
            os.makedirs(val)
            os.chdir(val)
        else:
            os.chdir(val)
        return argList[2:]
    
    elif op == "-d" or op == "--digit ":
        val = argList[1]
        if (val.isnumeric()):
            global digit
            digit = int (val)
            print("digit assegnata pari a: "+ str(digit))
            return argList[2:]
        else:
            help()

    else:
        help()

def systemConfig(argv):
    global startNum, endNum
    if (len(argv) < 5):
        help()

    global baseUrl, endUrl, startNum, endNum

    baseUrl = str(argv[1])
    endUrl = str(argv[2])
    if argv[3].isnumeric() and argv[4].isnumeric():
        startNum = int(argv[3])
        endNum = int(argv[4])
        if (endNum < startNum):
            help()
    else:
        help()

    # Quando ci saranno attivo le opzioni
    if len(argv) > 5:
        argList = argv[5:]
        while (len(argList) > 0):
            argList = optionSet(argList)


def son(url, i):
    print("\nDownload: " + url + "\n\t Start " + str(i))
    if (platform.system()=="Linux"):
        os.system("xterm -e bash -c '"+"wget " + url+"'")
    elif (platform.system()=="Windows"):
        os.system("Invoke-WebRequest -Uri "+ url)
    else:
        print("OS not Supported")
    print("\n\t END " + str(i))

    #os.system("exit")
    exit(0)


def main():
    systemConfig(sys.argv)

    # Inizio la procedura
    start_time = datetime.now() 

    tokenActive = 0
    nDownload = 0;
    for i in range(startNum, endNum+1):
        tokenActive += 1
        pid = os.fork()
        if pid == 0:    #child process
            num = "{num:0{dig}d}".format(dig=digit,num=i)
            son(baseUrl + num + endUrl , i)
        else: # We are in the parent process.
            nDownload += 1
            if(tokenActive<pWget):
                continue
            else:
                os.wait()
                tokenActive -= 1
    
    while(tokenActive!=0):
        os.wait()
        tokenActive -= 1
        
    time_elapsed = datetime.now() - start_time 
    print("## Downloads end ##")
    print('Total Time (hh:mm:ss.ms) {}'.format(time_elapsed))
    print('Mean Time (hh:mm:ss.ms) {}'.format(time_elapsed/(nDownload)))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
