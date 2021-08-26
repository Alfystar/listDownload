from urwidtrees.widgets import TreeBox
from urwidtrees.tree import SimpleTree
from urwidtrees.nested import NestedTree
from urwidtrees.decoration import ArrowTree, CollapsibleArrowTree  # decoration

import urwid
from urwid import ACTIVATE
from urwid.util import is_mouse_press

# todo: remove ExampleItem & ListRequest, is only for debug
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
        if self._command_map[key] != ACTIVATE:
            return key

        self._emit('click')

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


class RequestContainerDisplay(urwid.WidgetWrap):
    rc: RequestContainer = None
    subBranch = []

    # Download Display Objects
    info: urwid.Text = None
    bar: urwid.ProgressBar = None
    speed: urwid.Text = None

    def __init__(self, rc: RequestContainer):
        self.rc = rc
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

        urwid.WidgetWrap.__init__(self, top)

    def generateSubBranch(self): # Generate subBranch for the tree
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
        if(memTot != 0):
            self.bar.set_completion(memCur/memTot)
        else:
            self.bar.set_completion(0)
        self.speed.set_text(bytesConvert(curSpeed)+"/s")


    def selectable(self):
        return True


class DownloadTree(TreeBox):
    # Data List
    rcList: list = []  # List of the different RequestContainer, used to generate theirs item list

    tree = None # Global Object for the tree
    requestTreeList = []  # List of the Tree-nodes compose by RequestContainerDisplay & DownloadDisplay

    # TreeBox := Is the final widget
    # NestedTree := Permit to merge different type of tree together
    # CollapsibleArrowTree := CollapsibleTree with Arrow Decoration
    # SimpleTree := Tree data structure in concrete

    def __init__(self, rcList=[]):
        self.rcList = rcList
        self.tree = self.generateTree()
        self.tree.collapse_all()
        super().__init__(self.tree)

    def addRequest(self, rc: RequestContainer):
        self.rcList.append(rc)
        rc.registerChangeNotify(self.rcNotify)
        self.createAndAppendBranch(rc)
        # self.tree = self.generateTree()
        # super().__init__(self.tree)
        super().refresh()

    def rmRequest(self, rc: RequestContainer):
        try:
            index = self.rcList.index(rc)
        except:
            print("Index not found")
            return
        self.rcList.pop(index)
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
                     (FocusableText('...'), None)           # todo: Connect AddRequest
                 ]
                 )
            ]
        )

        # mainTree = SimpleTree([(FocusableText('Download List:'), [(requestTreeList, None)])])  # end SimpleTree constructor

        return NestedTree(ArrowTree(mainTree))

    def createAndAppendBranch(self, rc: RequestContainer):
        ItemList = rc.generateItem()
        rcd = RequestContainerDisplay(rc)
        subBranch = rcd.subBranch
        branch = (RequestContainerDisplay(rc), subBranch)
        # (requestTree, None)
        self.requestTreeList.append(branch)
        # self.requestTreeList.append((branch, None))

    def keypress(self, size, key):
        # First get the current focus
        focus = self.get_focus()
        # Than execute the command anyway
        super().keypress(size, key)

        # Finaly, if key was 'left' and focus no change than i'm on the root and the user want go out
        if key == 'left' and focus == self.get_focus():
            return key

    # Notify Callback
    def rcNotify(self, rcNotify: RequestContainer):
        # todo: Quando rc notifica il proprio cambiamento, questa funzione deve richiamare generateTree e riassegnarla
        # Ricordando di chiamare super()..refresh()  # callback for the Main loop to recalculate all the windows
        pass
