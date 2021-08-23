from urwidtrees.widgets import TreeBox
from urwidtrees.tree import SimpleTree
from urwidtrees.nested import NestedTree
from urwidtrees.decoration import ArrowTree, CollapsibleArrowTree  # decoration
import urwid
from ..listDownloadSrc.RequestContainer import RequestContainer
from ..listDownloadSrc.DownloadItem import DownloadItem, ExampleItem


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

    # Display Object
    name: urwid.Text = None
    bar: urwid.ProgressBar = None
    policy: urwid.Text = None
    size: urwid.Text = None
    speed: urwid.Text = None

    def __init__(self, item: DownloadItem):
        self.item = item
        self.item.registerChunkUpdateNotify(self.chunkNotify)
        self.item.registerCompleteUpdateNotify(self.compleateNotify)

        self.name = urwid.Text("Name", align='left')
        self.bar = urwid.ProgressBar('normal', 'complete', 100)
        self.policy = urwid.Text("Policy", align='left')
        self.size = urwid.Text("curr MB/Total GB", align='right')
        self.speed = urwid.Text("Speed Mib/s", align='right')
        top = urwid.Columns([self.name, self.bar, self.size, self.speed], dividechars=1)
        top = urwid.AttrMap(top, 'body', 'focus')

        w = top
        urwid.WidgetWrap.__init__(self, w)

        # todo: generare il segnale per il click sulla riga
        urwid.connect_signal(self, 'click', self.clickEvent)

    def selectable(self):
        return True

    def keypress(self, size, key):
        return key

    i = 0
    # Click
    def clickEvent(self):
        self.i = self.i+1
        self.name.set_text(["Cliccato ", self.i ," Volte"])

    # Notify Callback
    def chunkNotify(self, rc: DownloadItem):
        # todo: Quando rc notifica il proprio cambiamento, questa funzione deve richiamare generateTree e riassegnarla
        # Ricordando di chiamare super()..refresh()  # callback for the Main loop to recalculate all the windows
        pass

    def compleateNotify(self, rc: DownloadItem):
        # todo: Quando rc notifica il proprio cambiamento, questa funzione deve richiamare generateTree e riassegnarla
        # Ricordando di chiamare super()..refresh()  # callback for the Main loop to recalculate all the windows
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
        return SimpleTree([(FocusableText('Mid Child Three'), [
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
    def rcNotify(self, rc: RequestContainer):
        # todo: Quando rc notifica il proprio cambiamento, questa funzione deve richiamare generateTree e riassegnarla
        # Ricordando di chiamare super()..refresh()  # callback for the Main loop to recalculate all the windows
        pass
