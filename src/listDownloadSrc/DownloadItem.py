import platform
import time
from enum import Enum, auto

import requests

from src.listDownloadSrc.utilityFunction import *  # local main include

# try:
#     from .utilityFunction import *  # module include
# except:
#     from src.listDownloadSrc.utilityFunction import *  # local main include

debug: bool = False
defaultDir: str = "./listDownload/"


def changeDefaultDir(newDir) -> None:
    global defaultDir
    newDir = removeProblematicCharacter(newDir)
    if not is_path_creatable(newDir):
        raise Exception("newDir: \"" + newDir + "\" isn't a Creatable directory, check your privilege")

    defaultDir = newDir


def getDefaultDir() -> str:
    return defaultDir


class DownloadPolicy(Enum):
    Ov = auto()  # Override         := Override the File if already exist
    DN = auto()  # DownloadIfNew    := If the webFile is newly download
    Ig = auto()  # Jump             := Jump over this File if already exist


class DownloadItem:
    """
    This Class object represent one complete ITEM to download, and add any method and attribute to better
    describe the object.
    """
    # Download Parameter
    url: str = ""  # Download Url
    name: str = ""  # File name
    outDir: str = ""  # Output Directory of the Download, not end with '/' possibly,
    outDirDefault: bool = True  # Start True, can be only change to False, if True on download moment outDir
    # will read again from global defaultDir
    savePath: str = ""  # outDir + savePath during download make the "savePath"

    verbose: bool = False  # Verbose output (generate xterm shell)

    # Class state Parameter
    fileExist: bool = False
    filePolicy: DownloadPolicy = DownloadPolicy.DN  # If file exist, policy can change

    # Download Current State
    totalSize: int = 0
    downloadedSize: int = 0
    currentSpeed: int = 0

    # Connection Obj
    response: requests = None

    # Callback pointer
    startDownloadNotiy: list = []
    downloadUpdateNotify: list = []
    completeUpdateNotify: list = []

    def __init__(self, url: str, outDir: str = None, verbose: bool = False,
                 startDownloadNotiy=None, chunkUpdateNotify=None, completeNotify=None):
        # Url extract Data
        if is_string_an_url(url):
            self.url = url
        else:
            raise Exception("Url isn't a downloadable file")
        tmpName = extractName2Url(self.url)

        # OutDir extract Data
        if outDir is None:
            outDir = getDefaultDir()
        self.changeSaving(outDir, tmpName)

        # Verbose extract Data
        self.verbose = verbose

        # Calls-back registering
        self.registerStartDownloadNotify(startDownloadNotiy)
        self.registerDownloadUpdateNotify(chunkUpdateNotify)
        self.registerCompleteUpdateNotify(completeNotify)

    def changeSaving(self, path: str = None, new_name: str = None):
        """
        @path := The directory path where the file will save
        @new_name := The name of the file
        """
        global defaultDir

        if new_name is None:
            new_name = self.name
        new_name = removeProblematicCharacter(new_name)

        if path is None:
            if self.outDirDefault:
                path = defaultDir
            else:
                path = self.outDir
        else:
            self.outDirDefault = False

        if path == "":
            path = self.outDir
        if path[-1] == "/":
            path = path[:-1]
        path = removeProblematicCharacter(path)

        if not is_path_creatable(path):
            raise Exception("path: \"" + path + "\" isn't a Creatable directory, check your privilege")

        savePath = path + "/" + new_name

        self.outDir = path
        self.name = new_name
        self.savePath = savePath
        self.fileExist = os.path.isfile(self.savePath)

    def myDownload(self) -> bool:
        """
        This Function return true if file are effectively downloaded
        """

        self.sendStartDownloadNotify()

        if self.outDirDefault:  # Reload last global name
            self.changeSaving()

        # Create the Download Directory
        try:
            os.makedirs(self.outDir)
        except FileExistsError:
            # Nop all Ok
            pass
        except Exception as e:
            print("os.makedirs get Error:", e)

        # Download Policy based on the policy
        if self.fileExist:
            # If exist, the result depend form the policy chosen
            if self.filePolicy == DownloadPolicy.Ig:
                return False
            if self.filePolicy == DownloadPolicy.DN:
                # wgetOption += "-nc "  # --no-clobber if file is present, check the time-stamp
                pass
            if self.filePolicy == DownloadPolicy.Ov:
                # wgetOption += " "
                pass

        if debug:
            print("\nDownload: " + self.url + "\n\t Start " + self.savePath)

        # Information Download
        start = time.perf_counter()
        with open(self.savePath, "wb") as f:
            self.response = requests.get(self.url, stream=True)
            self.totalSize = int(self.response.headers.get('content-length'))

            if self.totalSize is None:  # no content length header
                f.write(self.response.content)
                return False
            else:
                self.downloadedSize = 0
                # Connection never close, but "interrupt" is send every chunk, efficient and able to get statistics
                for data in self.response.iter_content(chunk_size=4096):
                    self.downloadedSize += len(data)
                    self.currentSpeed = self.downloadedSize // (time.perf_counter() - start)
                    f.write(data)
                    self.sendChunkUpdateNotify()
        self.currentSpeed = 0
        self.sendCompleteUpdateNotify()
        return True

    def download(self) -> bool:
        """
        This Function return true if file are effectively downloaded
        """

        self.sendStartDownloadNotify()

        if self.outDirDefault:  # Reload last global name
            self.changeSaving()

        # Create the Download Directory
        try:
            os.makedirs(self.outDir)
        except FileExistsError:
            # Nop all Ok
            pass
        except Exception as e:
            print("os.makedirs get Error:", e)

        wgetOption: str = ""
        # Download Policy based on the policy
        if self.fileExist:
            # If exist, the result depend form the policy chosen
            if self.filePolicy == DownloadPolicy.Ig:
                return False
            if self.filePolicy == DownloadPolicy.DN:
                wgetOption += "-nc "  # --no-clobber if file is present, check the time-stamp
            if self.filePolicy == DownloadPolicy.Ov:
                wgetOption += " "

        if debug:
            print("\nDownload: " + self.url + "\n\t Start " + self.savePath)
        download_cmd: str = ""
        if platform.system() == "Linux":
            download_cmd = "wget " + wgetOption + "--output-document \"" + self.savePath + "\" " + self.url
        elif platform.system() == "Windows":
            download_cmd = "Invoke-WebRequest -Uri " + self.url + " -OutFile \"" + self.savePath + "\""
        else:
            print("OS not Supported")
            return False

        retCode = 0  # 0:= Download success, otherwise no download started
        if platform.system() == "Linux":
            if self.verbose:
                cmd = "xterm -e bash -c '" + download_cmd + "'"
            else:
                cmd = download_cmd + " --quiet"

            if debug:
                print(cmd)
            else:
                retCode = os.system(cmd)

        elif platform.system() == "Windows":
            cmd = download_cmd
            if debug:
                print("powershell.exe " + cmd)
            else:
                retCode = os.system("powershell.exe " + cmd)

        else:
            print("OS not Supported")
        # todo: ottenere il return code dei terminali in base al successo o meno del download
        if debug:
            print("\n\t END " + self.savePath)
        if retCode == 0 or retCode > 255:
            self.totalSize = 1;
            self.downloadedSize = 1;
            self.sendCompleteUpdateNotify()
            return True
        else:
            return False

    def downloadStatus(self) -> float:
        if self.totalSize != 0:
            return (self.downloadedSize * 100) / self.totalSize
        else:
            return 0

    def memStatus(self) -> str:
        return bytesConvert(self.downloadedSize, "k") + "/" + bytesConvert(self.totalSize, "k")

    def speedStatus(self) -> str:
        return bytesConvert(self.currentSpeed) + "/s"

    # Register CallBack function Zone

    def registerCallBack(self, callList, functPointer):
        if functPointer is not None:
            callList.append(functPointer)

    def registerStartDownloadNotify(self, startNotify):
        self.registerCallBack(self.startDownloadNotiy, startNotify)

    def registerDownloadUpdateNotify(self, chunkUpdateNotify):
        self.registerCallBack(self.downloadUpdateNotify, chunkUpdateNotify)

    def registerCompleteUpdateNotify(self, completeUpdateNotify):
        self.registerCallBack(self.completeUpdateNotify, completeUpdateNotify)

    # Send CallBack function Zone
    def sendNotify(self, list):
        for call in list:
            call(self)

    def sendStartDownloadNotify(self):
        self.sendNotify(self.startDownloadNotiy)

    def sendChunkUpdateNotify(self):
        self.sendNotify(self.downloadUpdateNotify)

    def sendCompleteUpdateNotify(self):
        self.sendNotify(self.completeUpdateNotify)


ExampleItem = DownloadItem("https://static.djangoproject.com/img/fundraising-heart.cd6bb84ffd33.svg", "./example/",
                           True)

if __name__ == '__main__':
    item1 = DownloadItem("https://static.djangoproject.com/img/fundraising-heart.cd6bb84ffd33.svg")
    print("################## first download ##################")
    item1.download()

    item2 = DownloadItem("https://static.djangoproject.com/img/fundraising-heart.cd6bb84ffd33.svg", "./example")
    print("################## second download with output dir ##################")
    item2.download()

    changeDefaultDir("./testDir")
    print("################## changed download directory: " + defaultDir + "##################")
    item3 = DownloadItem("https://static.djangoproject.com/img/fundraising-heart.cd6bb84ffd33.svg")

    print("################## third download ##################")
    item1.download()
    item2.download()
    item3.download()
