"""
This class is the DAD for specific group of downloading file, it contains the sub level download items
"""
import urwid

from src.listDownloadSrc.requestTypes.RequestContainer import RequestContainer
from src.listDownloadSrc.utilityFunction import bytesConvert
from src.tuiSrc.treeView.DownloadDisplay import DownloadDisplay


class RequestContainerDisplay(urwid.WidgetWrap):
    signals = ['click']
    rc: RequestContainer = None
    dad = None  # type 'DownloadTree' normally
    subBranch = []

    # Download Display Objects, instantiate in init funct to be different for all instance
    info: urwid.Text = None
    bar: urwid.ProgressBar = None
    speed: urwid.Text = None

    # PopUp widget
    popUpWidgetRef = None

    def __init__(self, rc: RequestContainer, dad):
        self.dad = dad
        self.info = urwid.Text("")
        self.bar = urwid.ProgressBar('normalTot', 'completeTot', 0, satt='c')
        self.speed = urwid.Text("0B", align='center')

        top = urwid.Columns([('weight', 4, self.info),
                             ('weight', 4, self.bar),
                             ('weight', 2, self.speed)]
                            , dividechars=0)
        top = urwid.AttrMap(top, 'DownloadItem', 'DownloadItemFocus')

        super().__init__(top)
        self.infoReset(rc)


    def keypress(self, size, key):
        if key == 'enter':
            self._emit('click')
            return None
        return key

    def generateSubBranch(self):  # Generate subBranch for the tree
        self.subBranch = []
        for it in self.rc.generateItem():
            self.subBranch.append((DownloadDisplay(it, self.dataReload), None))
        if len(self.subBranch) == 0:
            self.subBranch = None

    def infoReset(self, newRc):
        self.rc = newRc
        self.info.set_text(
            self.rc.RequestType + "  " + self.rc.RequestName + "  " + self.rc.RequestInfo + "\nin: " + self.rc.RequestSavePath)
        self.dataReload()
        self.generateSubBranch()



    def dataReload(self):
        memTot = 0
        memCur = 0
        curSpeed = 0
        for el in self.subBranch:
            memTot += el[0].item.totalSize
            memCur += el[0].item.downloadedSize
            curSpeed += el[0].item.currentSpeed
        if (memTot != 0):
            self.bar.set_completion(memCur / memTot)
        else:
            self.bar.set_completion(0)
        self.speed.set_text(bytesConvert(curSpeed) + "/s")

    def selectable(self):
        return True