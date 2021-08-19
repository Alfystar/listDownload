from enum import Enum, auto
import platform
from .validateFunction import *

debug: bool = True
defaultDir: str = "./listDownload/"


def changeDefaultDir(newDir) -> None:
    global defaultDir
    newDir = removeProblematicCharacter(newDir)
    if not is_path_creatable(newDir):
        raise Exception("newDir: \"" + newDir + "\" isn't a Creatable directory, check your privilege")

    defaultDir = newDir


def removeProblematicCharacter(path: str) -> str:
    path = path.replace(" ", "_")
    path = path.replace(":", "_")
    return path


class DownloadPolicy(Enum):
    Override = auto()  # Override the File if already exist
    DownloadIfNew = auto()  # Override if the webFile is more newly
    Ignore = auto()  # Jump this File if already exist


class DownloadInfo:
    currentItem = None  # type DownloadItem, but isn't possible force because the first depend from the second

    def __init__(self):
        pass


class DownloadItem:
    """
    This Class object represent one complete ITEM to download, and add any method and attribute to better
    describe the object.
    """
    # Download Parameter
    url: str = ""  # Download Url
    name: str = ""  # File name
    outDir: str = ""  # Output Directory of the Download, not end with '/' possibly
    savePath: str = ""  # outDir + savePath during download make the "savePath"

    verbose: bool = False  # Verbose output (generate xterm shell)

    # Class state Parameter
    fileExist: bool = False
    filePolicy: DownloadPolicy = DownloadPolicy.DownloadIfNew  # If file exist, policy can change

    # Download Current State
    totalSize: int = 0
    downloadSize: int = 0
    currentSpeed: int = 0

    # Callback pointer
    dataUpdateNotify_callback = None  # self.dataUpdateNotify_callback(self)   Notify another Chunk-Reading

    def __init__(self, url: str, outDir: str = defaultDir, verbose: bool = False, readNotify=None):
        # Url extract Data
        if is_string_an_url(url):
            self.url = url
        else:
            raise Exception("Url isn't a downloadable file")
        name = self.url[self.url.rfind("/") + 1:]  # Name is last part of the url

        # OutDir extract Data
        self.changeSaving(outDir, name)

        # Verbose extract Data
        self.verbose = verbose

        # Calls-back
        self.dataUpdateNotify_callback = readNotify

    def changeSaving(self, path: str = "", new_name: str = ""):
        if new_name == "":
            new_name = self.name
        if path == "":
            path = self.outDir
        new_name = removeProblematicCharacter(new_name)

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

    def download(self, di: DownloadInfo = None) -> bool:
        """
        This Function return true if file are effectively downloaded
        """
        if di is not None:
            di.currentItem = self

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
            if self.filePolicy == DownloadPolicy.Ignore:
                return False
            if self.filePolicy == DownloadPolicy.DownloadIfNew:
                wgetOption += "-nc "  # --no-clobber if file is present, check the time-stamp
            if self.filePolicy == DownloadPolicy.Override:
                wgetOption += " "

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
        print("\n\t END " + self.savePath)
        if (retCode == 0):
            return True
        else:
            return False


if __name__ == '__main__':
    item = DownloadItem("https://static.djangoproject.com/img/fundraising-heart.cd6bb84ffd33.svg", "../example/", True)
    item.changeSaving(new_name="test")
    item.download()

    item = DownloadItem("https://static.djangoproject.com/img/fundraising-heart.cd6bb84ffd33.svg", verbose=True)
    item.changeSaving(new_name="test")
    item.download()
