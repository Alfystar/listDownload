from src.listDownloadSrc.DownloadItem import DownloadItem
from src.listDownloadSrc.requestTypes.RequestContainer import RequestContainer
from src.listDownloadSrc.utilityFunction import *


class ListRequest(RequestContainer):
    parametricUrl: str = None
    startNum: int = None
    endNum: int = None
    digit: int = 2

    outDirPath: str = None

    def __init__(self, parametricUrl: str, startNum: int, endNum: int, outDirPath: str = None):
        super().__init__()
        self.RequestType = "List"
        self.parametricUrl = parametricUrl
        if startNum > endNum:
            self.startNum = endNum
            self.endNum = startNum
        else:
            self.startNum = startNum
            self.endNum = endNum
        self.digit = self.parametricUrl.count('#')
        self.outDirPath = outDirPath

        self.RequestName = extractName2Url(self.parametricUrl)
        self.RequestInfo = "From " + str(self.startNum) + "->" + str(self.endNum)
        self.outDirPath = outDirPath

    def generateItem(self) -> list:
        if self.parametricUrl is None or self.startNum is None or self.endNum is None:
            raise Exception("Parameter not valid")

        itemList: list = []
        # Genero la lista degli url e le opzioni associate
        for i in range(self.startNum, self.endNum + 1):
            num = "{num:0{dig}d}".format(dig=self.digit, num=i)
            url = self.parametricUrl.replace("#" * self.digit, num)
            item = DownloadItem(url, self.outDirPath)

            # Aggiungo gli item alla lista
            itemList.append(item)

        return itemList
