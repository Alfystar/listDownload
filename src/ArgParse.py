import sys
from .DownloadItem import *

class ParserClass:
    # Parameter Mandatory
    baseUrl: str = None
    endUrl: str = None
    startNum: int = None
    endNum: int = None

    # Faculty Parameter
    pDW: int = None
    digit: int = 2
    outDir: str = defaultDir
    verbose: bool = False

    def __init__(self):
        self.argvParser()
        return


    def argvParser(self):
        if "-i" in sys.argv:
            # File Parser
            # listDownload.py -i <File List>                                          # Multiple-block download
            fileList = sys.argv[sys.argv.index("-i") + 1]

        else:
            # Single download
            # listDownload.py <baseUrl> <endUrl> <startNum> <endNum> [Global-Options] # One Download block
            if len(sys.argv) < 5:
                raise Exception("Not enough parameter for ##One Download block## modality")

            argvParseTerminal = 0
            try:
                terminalArgv = sys.argv[1:]
                argvParseTerminal = ArgParse(terminalArgv, defaultDownloadPath)
            except Exception as e:
                print("Oops!", str(e), "occurred.")
                helpMan()

            # Estraggo i parametri funzionali
            urlListParam += argvParseTerminal.urlParam

            if argvParseTerminal.pDW is not None:
                pDW = argvParseTerminal.pDW
            if argvParseTerminal.quite is not None:
                quite = argvParseTerminal.quite


def urlListInit():
    """
    Make the urlList in base of the command line params
    :return:
    """
    global urlListParam, pDW, quite, fileList

    if "-i" in sys.argv:
        index = sys.argv.index("-i")
        fileList = sys.argv[index + 1]
        subList = sys.argv[1:index] + sys.argv[index + 2:]
        argvListParse = 0
        try:
            argvListParse = ArgListParse(subList)
        except Exception as e:
            print("Oops!", str(e), "occurred.")
            helpMan()

        # Estraggo i parametri funzionali
        if argvListParse.pDW is not None:
            pDW = argvListParse.pDW
        if argvListParse.quite is not None:
            quite = argvListParse.quite

        # Using readlines()
        file1 = open(fileList, 'r')
        Lines = file1.readlines()
        file1.close()

        list_of_lists = []
        for line in Lines:
            list_of_lists.append(shlex.split(line))

        argvParseFile = 0
        for line in list_of_lists:
            try:
                argvParseFile = ArgParse(line, argvListParse.outDir)
            except Exception as e:
                print("Oops!", str(e), "occurred.")
                print(line)
                helpMan()

        # Estraggo i parametri funzionali
        urlListParam += argvParseFile.urlParam

    else:  # Comando Singolo
        if len(sys.argv) < 5:
            helpMan()

        argvParseTerminal = 0
        try:
            terminalArgv = sys.argv[1:]
            argvParseTerminal = ArgParse(terminalArgv, defaultDownloadPath)
        except Exception as e:
            print("Oops!", str(e), "occurred.")
            helpMan()

        # Estraggo i parametri funzionali
        urlListParam += argvParseTerminal.urlParam

        if argvParseTerminal.pDW is not None:
            pDW = argvParseTerminal.pDW
        if argvParseTerminal.quite is not None:
            quite = argvParseTerminal.quite

class Parser:
    """
    The Parser class contain data and function to read the parameter and create the url
    The 2 son class are used for the specific purpose
    """
    # Parameter Mandatory
    baseUrl = None
    endUrl = None
    startNum = None
    endNum = None

    # Faculty Parameter
    pDW = 5
    digit = 2
    outDir = "./listDownload/"
    quite = None

    # Url List
    urlParam = []  # [url, name, savePath]

    def __init__(self):
        return

    def generateList(self):
        if self.baseUrl is None or self.endUrl is None or self.startNum is None or self.endNum is None:
            raise Exception("Parameter not valid")

        # Genero la lista degli url e le opzioni associate
        for i in range(self.startNum, self.endNum + 1):
            num = "{num:0{dig}d}".format(dig=self.digit, num=i)
            url = self.baseUrl + num + self.endUrl
            name = self.baseUrl[self.baseUrl.rfind("/") + 1:] + num + self.endUrl

            # Aggiungo gli item alla lista
            self.urlParam.append([url, name, self.outDir])

    def optionSet(self, argList):
        """
        Ricevo argList e ritorno una sotto lista, impostando i miei parametri interni
        :param argList: @Lista di parametri
        :return: @SubList senza i parametri usati
        """
        op = argList[0]

        if op == "#" or op == "//":     # comment detect and avoiding
            return []   # Empty list

        if op == "-p" or op == "--parallelDownload":
            val = argList[1]
            if val.isnumeric():
                self.pDW = int(val)
                return argList[2:]
            else:
                raise Exception("parallelDownload parameter are Incorrect")

        elif op == "-o" or op == "--outSave":
            self.outDir = argList[1]
            return argList[2:]

        elif op == "-d" or op == "--digit ":
            val = argList[1]
            if val.isnumeric():
                self.digit = int(val)
                return argList[2:]
            else:
                raise Exception("digit parameter are Incorrect")

        elif op == "-q" or op == "--quiet":
            self.quite = True
            return argList[1:]
        elif op == "-v" or op == "--verbose":
            self.quite = False
            return argList[1:]

        else:
            raise Exception("Params not reconize")

    def systemConfig(self, argv):
        """
        Presia una lista di argv (sia da file o dal terminale, aggiunge gli url alla lista
        :param argv: @list [<baseUrl>, <endUrl>, <startNum>, <endNum>, [Options] ...]
        :return:
        """

        self.baseUrl = str(argv[0])
        self.endUrl = str(argv[1])

        if argv[2].isnumeric() and argv[3].isnumeric():
            self.startNum = int(argv[2])
            self.endNum = int(argv[3])
            if self.endNum < self.startNum:
                raise Exception("The Order of the Number are wrong, please change the order")
        else:
            raise Exception("The Number of the index aren't number!! please use the correct sintax")

        argList = argv[4:]      # get the variable side of the string
        self.listArgvParse(argList)

    def listArgvParse(self, argList):
        # Quando ci saranno attivo le opzioni
        while len(argList) > 0:
            argList = self.optionSet(argList)


class ArgParse(Parser):
    """
    The argParse is used to parse boot Mandatory and optional line of the command
    """

    def __init__(self, argv, defaultOutDir):
        super().__init__()
        self.outDir = defaultOutDir
        self.systemConfig(argv)
        self.generateList()


class ArgListParse(Parser):
    """
    The ArgListParse is used to parse only che optional argument
    """

    def __init__(self, listArgv):
        super().__init__()
        super().listArgvParse(listArgv)
