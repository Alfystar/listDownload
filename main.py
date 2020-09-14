#!/usr/bin/python3.8

import sys
import os
import time
from datetime import datetime 


# Parametri Obbligatori
baseUrl = ""
endUrl = ""
startNum = 0
endNum = 0

# Parametri Facoltativi
pWget = 5


def help():
    print("correct syntax is:")
    print("main.py <baseUrl> <endUrl> <startNum> <endNum> [Options]")
    print("\tbaseUrl:= Prima parte dell'url fissa fino ai numeri XX")
    print("\tendUrl:= Seconda parte dell'url fissa dopo i numeri XX")
    print("\tstartNum:= Primo episodio da scaricare")
    print("\tendNum:= Ultimo episodio da scaricare (Compreso)")
    print("[Options]:")
    print("\t\t -p --parallelWget <Number> Quante istanze di wget in parallelo, 5 default")
    print("\t\t -d --dirSave <path> Path su cui salvare, di default la corrente")

    print("Your command")
    print(sys.argv[1:])  # Press Ctrl+8 to toggle the breakpoint.
    exit(-1)


def optionSet(op, val):
    if op == "-p" or op == "--parallelWget":
        if (val.isnumeric()):
            global pWget
            pWget = int(val)
            print("pWget assegnata pari a: "+ str(pWget))
        else:
            help()

    elif op == "-d" or op == "--dirSave":
        if not os.path.exists(val):
            os.makedirs(val)
            os.chdir(val)
        else:
            os.chdir(val)

    else:
        help()


def son(url, i):
    print("\nDownload: " + url + "\n\t Start " + str(i))
    os.system("xterm -e bash -c '"+"wget " + url+"'")
    #os.system("wget --quiet " + url)
    #print("wget -no-verbose " + url)
    print("\nDownload: " + url + "\n\t END " + str(i))
    #time.sleep(1)

    os.system("exit")

    exit(0)


def main():
    global startNum, endNum
    if (len(sys.argv) < 5):
        help()

    global baseUrl
    global endUrl
    global startNum
    global endNum

    baseUrl = str(sys.argv[1])
    endUrl = str(sys.argv[2])
    if sys.argv[3].isnumeric() and sys.argv[4].isnumeric():
        startNum = int(sys.argv[3])
        endNum = int(sys.argv[4])
        if (endNum < startNum):
            help()

    else:
        help()

    # Quando ci saranno attivo le opzioni
    if len(sys.argv) > 5:
        print("dentro")
        for i in range(0, len(sys.argv[5:]), 2):  # Salto di 2 perchè ci sono le opzioni
            print(sys.argv[5 + i:5 + i + 2])
            optionSet(sys.argv[5 + i], sys.argv[5 + i + 1])

    start_time = datetime.now() 

    tokenActive = 0
    print("pWget letta pari a: " + str(pWget))
    for i in range(startNum, endNum+1):
        tokenActive += 1
        pid = os.fork()
        if pid == 0:    #child process

            son(baseUrl + str(f"{i:02d}") + endUrl, i)
        else: # We are in the parent process.
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




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
