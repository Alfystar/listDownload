from src.listDownloadSrc.requestTypes.RequestContainer import RequestContainer


class SingleRequest(RequestContainer):
    url: str = ""

    def __init__(self, url: str):
        super().__init__()
        self.RequestType = "Single"
        self.url = url
