class Parser:
    """
        Classe con la responsabilità di leggere una linea ed estrarne i parametri
        E se sono compatibili, creare la lista degli Url
        """
    # Parametri Obbligatori
    baseUrl = None
    endUrl = None
    startNum = None
    endNum = None

    # Parametri Facoltativi
    pDW = None
    digit = None
    outDir = "./parallelDowndload/"
    quite = None

    # Url List
    urlParam = []  # [url, name, savePath]

    def __init__(self):
        print("Costruttore di default")
        return self

    def generateList(self):
        if self.baseUrl is None or self.endUrl is None or self.startNum is None or self.endNum is None:
            raise Exception("Parametri non riconosciti")

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

        if op == "-p" or op == "--parallelDownload":
            val = argList[1]
            if (val.isnumeric()):
                self.pDW = int(val)
                return argList[2:]
            else:
                raise Exception("parallelDownload Incorrect")

        elif op == "-o" or op == "--outSave":
            self.outDir = argList[1]
            return argList[2:]

        elif op == "-d" or op == "--digit ":
            val = argList[1]
            if (val.isnumeric()):
                self.digit = int(val)
                return argList[2:]
            else:
                raise Exception("digit Incorrect")

        elif op == "--quiet":
            self.quite = True
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
            if (self.endNum < self.startNum):
                raise Exception("Extreme number wrong")
        else:
            raise Exception("Extreme number wrong")

        argList = argv[4:]
        self.listArgvParse(argList)

    def listArgvParse(self, argList):
        # Quando ci saranno attivo le opzioni
        while (len(argList) > 0):
            argList = self.optionSet(argList)


class ArgParse(Parser):


    def __init__(self, argv):
        """
        Prende una lista di Argv (dal terminale o dal file) e ne estrae i valori
        Se si vuole avere la lista chiamare generateList
        :param argv:
        :return: Null, set the class attribute
        """
        #super().__init__(self)
        self.systemConfig(argv)
        self.generateList()




class ArgListParse(Parser):
    def __init__(self, listArgv):
        #super().__init__(self)
        super().listArgvParse(listArgv)
