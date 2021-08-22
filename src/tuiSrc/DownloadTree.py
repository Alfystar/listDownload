from urwidtrees.widgets import TreeBox
from urwidtrees.tree import SimpleTree
from urwidtrees.nested import NestedTree
from urwidtrees.decoration import ArrowTree, CollapsibleArrowTree  # decoration
import urwid
from ..listDownloadSrc.ArgParse import RequestConteiner


# We use selectable Text widgets for our example..
# Selezionabili ma non modificabili, se non fossero selezionabili, il cursore li salterebbe!

class FocusableText(urwid.WidgetWrap):
    """Selectable Text used for nodes in our example"""

    def __init__(self, txt):
        t = urwid.Text(txt)
        w = urwid.AttrMap(t, 'body', 'focus')
        urwid.WidgetWrap.__init__(self, w)

    def selectable(self):
        return True

    def keypress(self, size, key):
        return key


class DownloadTree(TreeBox):
    rcObj: RequestConteiner = None  # The Object contain the information to generate the item Request

    # TreeBox := Is the final widget
    # NestedTree := Permit to merge different type of tree together
    # CollapsibleArrowTree := CollapsibleTree with Arrow Decoration
    # SimpleTree := Tree data structure in concrete

    def __init__(self, RequestContainerObj: RequestConteiner):
        self.rcObj = RequestContainerObj
        #w = tree  # urwid.AttrMap(tree, 'body', 'focus')
        #urwid.WidgetDecoration.__init__(self, w)
        tree = NestedTree(CollapsibleArrowTree(self.generateTree()))
        super().__init__(tree)



    def generateTree(self):
        # todo, create method in class to ask at rcObj to generate the tree structure
        return SimpleTree([(FocusableText('Mid Child Three'), [
            (FocusableText('Mid Grandchild One'), [
                (FocusableText('Mid Grandchild One'), [
                (FocusableText('Mid Grandchild One'), None),
                (FocusableText('Mid Grandchild Two'), [
                (FocusableText('Mid Grandchild One'), None),
                (FocusableText('Mid Grandchild Two'), None),
            ]),
            ]),
                (FocusableText('Mid Grandchild Two'), None),
            ]),
            (FocusableText('Mid Grandchild Two'), [
                (FocusableText('Mid Grandchild One'), [
                (FocusableText('Mid Grandchild One'), None),
                (FocusableText('Mid Grandchild Two'), None),
            ]),
                (FocusableText('Mid Grandchild Two'), [
                (FocusableText('Mid Grandchild One'), None),
                (FocusableText('Mid Grandchild Two'), [
                (FocusableText('Mid Grandchild One'), None),
                (FocusableText('Mid Grandchild Two'), None),
            ]),
            ]),
            ]),
        ]
                            )])

    def keypress(self, size, key):
        # First get the current focus
        focus = self.get_focus()
        # Than execute the command anyway
        super().keypress(size, key)

        # Finaly, if key was 'left' and focus no change than i'm on the root and the user want go out
        if key == 'left' and focus == self.get_focus():
            return key


