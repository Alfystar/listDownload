class RequestContainer:
    changeNotifyCallback: list = []

    # Info attribute
    RequestType: str = ""
    RequestName: str = ""
    RequestInfo: str = ""
    RequestSavePath: str = ""

    def __init__(self):
        pass

    # Generate a list of DownloadItem Object
    def generateItem(self) -> list:  # All son have to override this method
        raise NotImplementedError("ERROR: 'generateItem()' method needs to be defined by sub-class")

    def registerChangeNotify(self, callbackRegister):
        self.changeNotifyCallback.append(callbackRegister)

    def sendChangeNotify(self):
        for call in self.changeNotifyCallback:
            call(self)
