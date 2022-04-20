from urwidtrees.widgets import TreeBox
from urwidtrees.tree import SimpleTree
from urwidtrees.nested import NestedTree
from urwidtrees.decoration import ArrowTree, CollapsibleArrowTree  # decoration

import urwid
from urwid import ACTIVATE
from urwid.util import is_mouse_press

# todo: remove ExampleItem & ListRequest, is only for debug
from .RequestForm import RequestForm
from ..listDownloadSrc.userRequestSubSystem import RequestContainer, ListRequest
from ..listDownloadSrc.downloadSubSystem import DownloadItem, ExampleItem
from ..listDownloadSrc.utilityFunction import bytesConvert


# We use selectable Text widgets for our example..
# Selezionabili ma non modificabili, se non fossero selezionabili, il cursore li salterebbe!

class FocusableText(urwid.WidgetWrap):
    """Selectable Text used for nodes in our example"""

    def __init__(self, txt):
        t = urwid.Text(txt)
        w = urwid.AttrMap(t, 'DownloadItem', 'DownloadItemFocus')
        urwid.WidgetWrap.__init__(self, w)

    def selectable(self):
        return True

    def keypress(self, size, key):
        return key


"""
This class display the status of a specific download
"""


class DownloadDisplay(urwid.WidgetWrap):
    item: DownloadItem = None
    _selectable: bool = False

    # Download Display Objects
    name: urwid.Text = None
    bar: urwid.ProgressBar = None
    policy: urwid.Text = None
    size: urwid.Text = None
    speed: urwid.Text = None

    signals = ["click"]

    # Callback
    dataChangeNotify = None  # Call when the item change something, to notify some-other, self.dataChangeNotify(self)

    def __init__(self, item: DownloadItem, dataChangeNotify=None, selectable: bool = True):
        self.item = item
        self.dataChangeNotify = dataChangeNotify
        self.item.registerDownloadUpdateNotify(self.downloadNotify)
        self.item.registerCompleteUpdateNotify(self.completeNotify)

        self._selectable = selectable

        self.itemUpdateData()

        top = urwid.Columns([('weight', 8, self.name),
                             ('weight', 4, self.bar),
                             ('weight', 1, self.policy),
                             ('weight', 4, self.size),
                             ('weight', 2, self.speed)]
                            , dividechars=0)
        top = urwid.AttrMap(top, 'DownloadItem', 'DownloadItemFocus')
        urwid.WidgetWrap.__init__(self, top)

        urwid.connect_signal(self, 'click', self.clickEvent)

    def itemUpdateData(self):
        self.name = urwid.Text(self.item.name, align='left')
        self.bar = urwid.ProgressBar('normal', 'complete', self.item.downloadStatus(), satt='c')
        self.policy = urwid.Text(self.item.filePolicy.name, align='center')
        self.size = urwid.Text(self.item.memStatus(), align='center')
        self.speed = urwid.Text(self.item.speedStatus(), align='center')

    def selectable(self):
        return self._selectable

    def keypress(self, size, key):
        """
        Send 'click' signal on 'enter' command.
        """
        if self._command_map[key] == ACTIVATE:
            self._emit('click')
            return None
        return super().keypress(size, key)

    def mouse_event(self, size, event, button, x, y, focus):
        """
        Send 'click' signal on button 1 press.
        """
        if button != 1 or not is_mouse_press(event):
            return False

        self._emit('click')
        return True

    i = 0

    # Click
    def clickEvent(self, objectEvent):
        self.i = self.i + 1
        self.name.set_text(["Cliccato ", str(self.i), " Volte"])

    # Notify Callback
    def downloadNotify(self, objectNotify: DownloadItem):
        self.itemUpdateData()
        self.dataChangeNotify(self)
        super().refresh()

    def completeNotify(self, objectNotify: DownloadItem):
        self.itemUpdateData()
        newTop = urwid.Columns([urwid.AttrMap(self.name, 'banner'), self.bar, self.size], dividechars=1)
        urwid.WidgetWrap.__init__(self, newTop)
        self.dataChangeNotify(self)
        super().refresh()


"""
This class is the DAD for specific group of downloading file, it contains the sub level download items
"""


class RequestContainerDisplay(urwid.PopUpLauncher):
    rc: RequestContainer = None
    dad = None  # type 'DownloadTree' normally
    subBranch = []

    # Download Display Objects
    info: urwid.Text = None
    bar: urwid.ProgressBar = None
    speed: urwid.Text = None

    # PopUp widget
    popUpWidgetRef = None

    def __init__(self, rc: RequestContainer, dad):
        self.rc = rc
        self.dad = dad
        self.info = urwid.Text(
            self.rc.RequestType + "  " + self.rc.RequestName + "  " + self.rc.RequestInfo + "\nin: " + self.rc.RequestSavePath)
        self.bar = urwid.ProgressBar('normalTot', 'completeTot', 0, satt='c')
        self.speed = urwid.Text("0B", align='center')

        self.generateSubBranch()
        self.dataReload()

        top = urwid.Columns([('weight', 4, self.info),
                             ('weight', 4, self.bar),
                             ('weight', 2, self.speed)]
                            , dividechars=0)
        top = urwid.AttrMap(top, 'DownloadItem', 'DownloadItemFocus')

        #  Genero il bottone, ma il nome lo scrivo attraverso l'icona selezionabile
        #         super(popUpButtonActivator, self).__init__(urwid.Button(caption))
        #         self.original_widget._w = urwid.AttrMap(urwid.SelectableIcon([u'  \N{BULLET} ', caption], 2), None, 'selected')
        #
        #         # Riassegno le variabili passate
        #         if popUpWidget is not None:
        #             self.popUpWidgetRef = popUpWidget
        #         if widgedSize is not None:
        #             self.widgetSizeRef = widgedSize
        #
        #         # Connetto il segnale per mostrare il popup
        #         urwid.connect_signal(self.original_widget, 'click', lambda button: (self.open_pop_up(), self.popUpWidgetRef.resetParam()))
        #
        #     def create_pop_up(self):  # Genera in loco un widget, e in questo caso assegna al pulsante la chiusura
        #         urwid.connect_signal(self.popUpWidgetRef, 'close', lambda button: self.close_pop_up())
        super(RequestContainerDisplay, self).__init__(top)
        # todo: quando ci saranno più tipi di download, specializzare i form
        self.popUpWidgetRef = RequestForm(formCompleteNotify=self.updateRequestListDownload_callback)

    def create_pop_up(self):  # Genera in loco un widget, e in questo caso assegna al pulsante la chiusura
        urwid.connect_signal(self.popUpWidgetRef, 'close', lambda button: self.close_pop_up())
        return self.popUpWidgetRef

    def get_pop_up_parameters(self):  # assegna posizione relativa rispetto pulsante
        return {'left': -2, 'top': 0, 'overlay_width': 120, 'overlay_height': 15}

    def keypress(self, size, key):
        if key == 'enter':
            # todo: quando ci saranno più tipi specializzerò il reset
            if type(self.rc) == ListRequest:
                self.popUpWidgetRef.resetParam(self.rc.baseUrl, self.rc.endUrl, self.rc.startNum, self.rc.endNum,
                                               self.rc.digit)
            self.open_pop_up()
        return key

    def updateRequestListDownload_callback(self, basePath, endPath, startIndex, endIndex, digit=2):
        rc = ListRequest(basePath, endPath, startIndex, endIndex, digit)
        self.dad.changeRequest(self.rc, rc)

    def generateSubBranch(self):  # Generate subBranch for the tree
        self.subBranch = []
        for it in self.rc.generateItem():
            self.subBranch.append((DownloadDisplay(it, self.dataReload), None))
        if len(self.subBranch) == 0:
            self.subBranch = None

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


"""
This class is the top level of the download tree
Is the conteiner for the leaf item (the active download)
"""


class DownloadTree(TreeBox):
    # Data List
    rcList: list = []  # List of the different RequestContainer, used to generate theirs item list

    tree = None  # Global Object for the tree
    requestTreeList = []  # List of the Tree-nodes compose by RequestContainerDisplay & DownloadDisplay

    # TreeBox := Is the final widget
    # NestedTree := Permit to merge different type of tree together
    # CollapsibleArrowTree := CollapsibleTree with Arrow Decoration
    # SimpleTree := Tree data structure in concrete

    def __init__(self, rcList=None):
        if rcList is None:
            rcList = []
        self.rcList = rcList
        self.tree = self.generateTree()
        self.tree.collapse_all()
        super().__init__(self.tree)

    def addRequest(self, rc: RequestContainer, index=-1):
        self.rcList.insert(index, rc)
        self.createAndAppendBranch(rc, index)
        rc.registerChangeNotify(self.rcNotify)
        super().refresh()

    def rmRequest(self, rc: RequestContainer):
        try:
            index = self.rcList.index(rc)
        except:
            print("Index not found")
            return
        self.rcList.pop(index)
        self.requestTreeList.pop(index)
        super().refresh()
        return index

    def changeRequest(self, rcOld, rcNew):
        self.addRequest(rcNew, self.rmRequest(rcOld))
        return

    def generateTree(self):
        # Example:
        # rc = ListRequest("https://www.egr.msu.edu/~khalil/NonlinearSystems/Sample/Lect_", ".pdf", 1, 5)
        # subBranch = [(DownloadDisplay(ExampleItem), None),(DownloadDisplay(ExampleItem), None)]
        # branch = (RequestContainerDisplay(rc), subBranch)
        # requestTreeList = [branch]

        # requestTreeList = [
        #     (RequestContainerDisplay(
        #         ListRequest("https://www.egr.msu.edu/~khalil/NonlinearSystems/Sample/Lect_", ".pdf", 1, 5)), [
        #          (DownloadDisplay(ExampleItem), None),
        #          (FocusableText('Mid Grandchild Two'), None),
        #      ]),
        #     branch
        # ]

        # Recursive mode
        for rc in self.rcList:
            self.createAndAppendBranch(rc)
        requestTree = NestedTree(CollapsibleArrowTree(SimpleTree(self.requestTreeList)))

        # define most out tree
        mainTree = SimpleTree(
            [
                (FocusableText('Download List:'),
                 [
                     (requestTree, None),
                     (FocusableText('...'), None)  # todo: Connect AddRequest
                 ]
                 )
            ]
        )

        # mainTree = SimpleTree([(FocusableText('Download List:'), [(requestTreeList, None)])])  # end SimpleTree constructor

        return NestedTree(ArrowTree(mainTree))

    def createAndAppendBranch(self, rc: RequestContainer, index=-1):
        # todo: capire perchè inserisce nella posizone dopo
        rcd = RequestContainerDisplay(rc, self)
        subBranch = rcd.subBranch
        branch = (RequestContainerDisplay(rc, self), subBranch)
        self.requestTreeList.insert(index, branch)

    def keypress(self, size, key):
        # First get the current focus
        focus = self.get_focus()
        # Than execcute the command anyway
        if key == "c" or key == "e":
            key = key.upper()
        super().keypress(size, key)

        # Finaly, if key was 'left' and focus no change than i'm on the root and the user want go out
        if key == 'left' and focus == self.get_focus():
            return key

    # Notify Callback
    def rcNotify(self, rcNotify: RequestContainer):
        # todo: Quando rc notifica il proprio cambiamento, questa funzione deve richiamare generateTree e riassegnarla
        # Ricordando di chiamare super()..refresh()  # callback for the Main loop to recalculate all the windows
        pass
