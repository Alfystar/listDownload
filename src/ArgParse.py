class Parser:
    """
    The Parser class contain data and function to read the parameter and create the url
    The 2 son class are used for the specific purpose
    """
    # Prameter Mandatory
    baseUrl = None
    endUrl = None
    startNum = None
    endNum = None

    # Parametri Facoltativi
    pDW = 5
    digit = 2
    outDir = "./listDowndload/"
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

    def __init__(self, argv):
        super().__init__()
        self.__init__(argv, self.outDir)

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
