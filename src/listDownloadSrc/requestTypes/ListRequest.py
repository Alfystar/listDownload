from src.listDownloadSrc.DownloadItem import DownloadItem
from src.listDownloadSrc.requestTypes.RequestContainer import RequestContainer
from src.listDownloadSrc.utilityFunction import *


class ListRequest(RequestContainer):
    baseUrl: str = None
    endUrl: str = None
    startNum: int = None
    endNum: int = None
    digit: int = 2

    outDirPath: str = None

    def __init__(self, baseUrl: str, endUrl: str, startNum: int, endNum: int, digit: int = 2, outDirPath: str = None):
        super().__init__()
        self.RequestType = "List"
        self.baseUrl = baseUrl
        self.endUrl = endUrl
        if (startNum > endNum):
            self.startNum = endNum
            self.endNum = startNum
        else:
            self.startNum = startNum
            self.endNum = endNum
        self.digit = digit
        self.outDirPath = outDirPath

        self.RequestName = extractName2Url(self.baseUrl + self.digit * "#" + self.endUrl)
        self.RequestInfo = "From " + str(self.startNum) + "->" + str(self.endNum)
        self.outDirPath = outDirPath

    def generateItem(self) -> list:
        if self.baseUrl is None or self.endUrl is None or self.startNum is None or self.endNum is None:
            raise Exception("Parameter not valid")

        itemList: list = []
        # Genero la lista degli url e le opzioni associate
        for i in range(self.startNum, self.endNum + 1):
            num = "{num:0{dig}d}".format(dig=self.digit, num=i)
            url = self.baseUrl + num + self.endUrl
            item = DownloadItem(url, self.outDirPath)

            # Aggiungo gli item alla lista
            itemList.append(item)

        return itemList
