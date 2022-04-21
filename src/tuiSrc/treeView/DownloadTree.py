import time

from urwidtrees.decoration import ArrowTree, CollapsibleArrowTree  # decoration
from urwidtrees.nested import NestedTree
from urwidtrees.tree import SimpleTree
from urwidtrees.widgets import TreeBox

from src.listDownloadSrc.requestTypes import RequestContainer
from src.tuiSrc.treeView.RequestContainerDisplay import RequestContainerDisplay
from src.tuiSrc.tuiGlobal import FocusableText

"""
This class is the top level of the download tree
Is the conteiner for the leaf item (the active download)
Descend from TreeBox, a widget
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

        # Recursive mode
        for rc in self.rcList:
            self.createAndAppendBranch(rc)

        requestTree = NestedTree(CollapsibleArrowTree(SimpleTree(self.requestTreeList)))

        # define most out tree
        outline = [(FocusableText('Download List:'), [
            (requestTree, None),
            (FocusableText('...'), None)
        ]
                    )]
        mainTree = SimpleTree(outline)

        self.tree = NestedTree(ArrowTree(mainTree))

        self.tree.collapse_all()
        super().__init__(self.tree)

    def addRequest(self, rc: RequestContainer, index=-1):
        if index == -1:
            self.rcList.insert(index, rc)
        else:
            self.rcList.append(rc)
        self.createAndAppendBranch(rc, index)
        rc.registerChangeNotify(self.rcNotify)
        super().refresh()

    def rmRequest(self, rc: RequestContainer):
        try:
            index = self.rcList.index(rc)
        except:
            print("Index not found")
            time.sleep(2)
            return
        self.rcList.pop(index)
        self.requestTreeList.pop(index)
        super().refresh()
        return index

    def changeRequest(self, rcOld, rcNew):
        self.addRequest(rcNew, self.rmRequest(rcOld))
        return


    def createAndAppendBranch(self, rc: RequestContainer, index=-1):
        rcd = RequestContainerDisplay(rc, self)
        subBranch = rcd.subBranch
        branch = (RequestContainerDisplay(rc, self), subBranch)
        if index == -1:
            self.requestTreeList.append(branch)
        else:
            self.requestTreeList.insert(index, branch)

    def keypress(self, size, key):
        # UpperCase the "c" and "e" key to open the tree
        if key == "c" or key == "e":
            key = key.upper()
        super().keypress(size, key)

        # Go back to the command area if in top level tree
        # First get the current focus
        focus = self.get_focus()
        # Finaly, if key was 'left' and focus no change than i'm on the root and the user want go out
        if key == 'left' and focus == self.get_focus():
            return key

    # Notify Callback
    def rcNotify(self, rcNotify: RequestContainer):
        # todo: Quando rc notifica il proprio cambiamento, questa funzione deve richiamare generateTree e riassegnarla
        # Ricordando di chiamare super()..refresh()  # callback for the Main loop to recalculate all the windows
        pass
