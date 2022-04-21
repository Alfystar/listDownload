from src.listDownloadSrc.requestTypes.RequestContainer import RequestContainer


class YoutubeRequest(RequestContainer):
    url: str = ""

    def __init__(self, url: str):
        super().__init__()
        self.RequestType = "Youtube"
        self.url = url
