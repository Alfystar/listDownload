import time

import urwid
from urwidtrees.decoration import ArrowTree, CollapsibleArrowTree  # decoration
from urwidtrees.nested import NestedTree
from urwidtrees.tree import SimpleTree
from urwidtrees.widgets import TreeBox

from src.listDownloadSrc.requestTypes import RequestContainer
from src.tuiSrc.PopUpContainer import PopUpContainer
from src.tuiSrc.requestTypeFormsWidget.ListRequestForm import ListRequestForm
from src.tuiSrc.treeView.RequestContainerDisplay import RequestContainerDisplay
from src.tuiSrc.tuiGlobal import FocusableText

"""
This class is the top level of the download tree
Is the conteiner for the leaf item (the active download)
Descend from TreeBox, a widget
"""


class DownloadTree(TreeBox):
    # Data List
    # rcList: list = []  # List of the different RequestContainer, used to generate theirs item list

    tree = None  # Global Object for the tree
    treeNodeList = []   # List of the Tree-nodes typically compose by RequestContainerDisplay & DownloadDisplay

    # TreeBox := Is the final widget
    # NestedTree := Permit to merge different type of tree together
    # CollapsibleArrowTree := CollapsibleTree with Arrow Decoration
    # SimpleTree := Tree data structure in concrete

    def __init__(self, rcList=None):

        # define most out tree
        self.treeNodeList = [FocusableText('Download List:'), [(FocusableText('...'), None)]]
        self.tree = NestedTree(ArrowTree(SimpleTree([self.treeNodeList])))
        self.tree.collapse_all()
        super().__init__(self.tree)

        # Load init Branch
        if rcList is None:
            rcList = []
        for rc in rcList:
            self.addRequest(rc)

    def addRequest(self, rc: RequestContainer, index=-1):
        rcd = RequestContainerDisplay(rc, self)
        editForm = ListRequestForm(formCompleteNotify=rcd.infoReset)
        openFunc = lambda: (
            editForm.resetParam(rcd.rc.baseUrl, rcd.rc.endUrl, rcd.rc.startNum, rcd.rc.endNum, rcd.rc.digit))
        popUpBranch = PopUpContainer(rcd, 'click', openFunc, editForm, editForm.getDimension())

        branch = (popUpBranch, rcd.subBranch)  # Punto per il sotto livello direttamente la lista corretta

        newRequestBranch = NestedTree(CollapsibleArrowTree(SimpleTree([branch])))
        newRequestBranch.collapse_all()

        self.treeNodeList[1].insert(index, (newRequestBranch, None))

        super().refresh()

    # def rmRequest(self, rcd: RequestContainerDisplay):
    #     try:
    #         index = self.rcList.index(rc)
    #     except:
    #         print("Index not found")
    #         time.sleep(2)
    #         return
    #     self.rcList.pop(index)
    #     self.treeNodeList[1].pop(index)
    #     super().refresh()
    #     return index
    #
    # def changeRequest(self, rcOld, rcNew):
    #     self.addRequest(rcNew, self.rmRequest(rcOld))
    #     return

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
    # def rcNotify(self, rcNotify: RequestContainer):
    #     # todo: Quando rc notifica il proprio cambiamento, questa funzione deve richiamare generateTree e riassegnarla
    #     # Ricordando di chiamare super()..refresh()  # callback for the Main loop to recalculate all the windows
    #     pass
