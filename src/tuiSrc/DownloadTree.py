from urwidtrees.widgets import TreeBox
from urwidtrees.tree import SimpleTree
from urwidtrees.nested import NestedTree
from urwidtrees.decoration import ArrowTree, CollapsibleArrowTree  # decoration

import urwid
from urwid import ACTIVATE
from urwid.util import is_mouse_press

from ..listDownloadSrc.userRequestSubSystem import RequestContainer
from ..listDownloadSrc.downloadSubSystem import DownloadItem, ExampleItem


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

    def __init__(self, item: DownloadItem, selectable: bool = True):
        self.item = item
        self.item.registerDownloadUpdateNotify(self.downloadNotify)
        self.item.registerCompleteUpdateNotify(self.completeNotify)

        self._selectable = selectable

        self.itemUpdateData()

        top = urwid.Columns([self.name,self.bar, self.policy, self.size, self.speed] , dividechars=1)
        top = urwid.AttrMap(top, 'DownloadItem', 'DownloadItemFocus')

        urwid.WidgetWrap.__init__(self, top)

        # todo: generare il segnale per il click sulla riga
        urwid.connect_signal(self, 'click', self.clickEvent)

    def itemUpdateData(self):
        self.name = urwid.Text(self.item.name, align='left')
        self.bar = urwid.ProgressBar('normal', 'complete', self.item.downloadStatus(), satt='c')
        self.policy = urwid.Text(self.item.filePolicy.name, align='center')
        self.size = urwid.Text(self.item.memStatus(), align='right')
        self.speed = urwid.Text(self.item.speedStatus(), align='right')

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
        super().refresh()

    def completeNotify(self, objectNotify: DownloadItem):
        self.itemUpdateData()
        newTop = urwid.Columns([urwid.AttrMap(self.name, 'banner'), self.bar, self.size], dividechars=1)
        urwid.WidgetWrap.__init__(self, newTop)
        super().refresh()


class RequestConteinerDisplay(urwid.WidgetWrap):
    pass


class DownloadTree(TreeBox):
    rcObj: RequestContainer = None  # The Object contain the information to generate the item Request

    # TreeBox := Is the final widget
    # NestedTree := Permit to merge different type of tree together
    # CollapsibleArrowTree := CollapsibleTree with Arrow Decoration
    # SimpleTree := Tree data structure in concrete

    def __init__(self, RequestContainerObj: RequestContainer):
        self.rcObj = RequestContainerObj
        self.rcObj.registerChangeNotify(self.rcNotify)
        # w = tree  # urwid.AttrMap(tree, 'body', 'focus')
        # urwid.WidgetDecoration.__init__(self, w)
        tree = NestedTree(CollapsibleArrowTree(self.generateTree()))
        super().__init__(tree)

    def generateTree(self):
        # todo, create method in class to ask at rcObj to generate the tree structure
        return SimpleTree([(FocusableText('Download List:'), [
            (FocusableText('Mid Grandchild One'), [
                (DownloadDisplay(ExampleItem), [
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
                        (FocusableText('Mid Grandchild One'), [
                            (FocusableText('Mid Grandchild One'), None),
                            (FocusableText('Mid Grandchild Two'), [
                                (FocusableText('Mid Grandchild One'), None),
                                (FocusableText('Mid Grandchild Two'), None),
                            ]),
                        ]),
                        (FocusableText('Mid Grandchild Two'), [
                            (FocusableText('Mid Grandchild One'), None),
                            (FocusableText('Mid Grandchild Two'), None),
                        ]),
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

    # Notify Callback
    def rcNotify(self, rcNotify: RequestContainer):
        # todo: Quando rc notifica il proprio cambiamento, questa funzione deve richiamare generateTree e riassegnarla
        # Ricordando di chiamare super()..refresh()  # callback for the Main loop to recalculate all the windows
        pass
