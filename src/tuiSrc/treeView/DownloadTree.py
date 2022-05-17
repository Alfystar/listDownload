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
    treeNodeList = []  # List of the Tree-nodes typically compose by RequestContainerDisplay & DownloadDisplay

    # TreeBox := Is the final widget
    # NestedTree := Permit to merge different type of tree together
    # CollapsibleArrowTree := CollapsibleTree with Arrow Decoration
    # SimpleTree := Tree data structure in concrete

    def __init__(self, rcList=None):
        # Define the base shape of the tree (with no element)
        # last element have to be a NestedTree,
        # otherwise during deletion of node the library isn't able to recreate the structure
        endTree = NestedTree(SimpleTree([(FocusableText('...'), None)]))
        self.treeNodeList = [FocusableText('Download List:'), [(endTree, None)]]
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
            editForm.resetParam(rcd.rc.parametricUrl, rcd.rc.startNum, rcd.rc.endNum))
        popUpBranch = PopUpContainer(rcd, 'click', openFunc, editForm, editForm.getDimension())

        branch = (popUpBranch, rcd.subBranch)  # Punto per il sotto livello direttamente la lista corretta

        newRequestBranch = NestedTree(CollapsibleArrowTree(SimpleTree([branch])))
        newRequestBranch.collapse_all()

        self.treeNodeList[1].insert(index, (newRequestBranch, None))
        super().refresh()

    def rmRequest(self, rcd: RequestContainerDisplay):
        # Find the subRequestTree of interest
        for subRequestTree in self.treeNodeList[1]:
            # Cerco ricorsivamente dentro tutti i decorator quanti sono i decorator usati
            rcdIterator = subRequestTree[0]._lookup_entry(subRequestTree[0], []).base_widget
            if rcdIterator == rcd:
                self.treeNodeList[1].remove(subRequestTree)
                break
        super().refresh()

    def downloadStart(self):
        items = []
        for subRequestTree in self.treeNodeList[1]:
            # Cerco ricorsivamente dentro tutti i decorator quanti sono i decorator usati
            rcdIterator = subRequestTree[0]._lookup_entry(subRequestTree[0], []).base_widget
            try:
                for rc in rcdIterator.subBranch:
                    items.append(rc[0].item)
                    a = 1
            except:
                # Era il FocusableText finale, lo evito
                pass
        return items

    def keypress(self, size, key):
        if key == 'left':  # Go back to the command only if in top level tree
            # Save current focus position (before apply the command)
            focus = self.get_focus()
            super().keypress(size, key)
            # Now, if focus not change than I'm on the root node and the user want go out, else the key was just used
            if focus == self.get_focus():
                return key  # Key not use to move
            else:
                return None  # Key used to move the focus

        # UpperCase the "c" and "e" key to open the tree
        if key == "c" or key == "e":
            key = key.upper()
        return super().keypress(size, key)

    # Notify Callback
    # def rcNotify(self, rcNotify: RequestContainer):
    #     # todo: Quando rc notifica il proprio cambiamento, questa funzione deve richiamare generateTree e riassegnarla
    #     # Ricordando di chiamare super()..refresh()  # callback for the Main loop to recalculate all the windows
    #     pass
