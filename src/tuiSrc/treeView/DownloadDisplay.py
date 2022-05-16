"""
This class display the status of a specific download
"""
import urwid
from urwid import ACTIVATE
from urwid.util import is_mouse_press

from src.listDownloadSrc.DownloadItem import DownloadItem


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

    def __init__(self, item: DownloadItem, dadUpdateFunction=None, selectable: bool = True):
        self.item = item
        self.item.registerDownloadUpdateNotify(self.downloadNotify)
        self.item.registerCompleteUpdateNotify(self.completeNotify)
        if dadUpdateFunction is not None:
            self.dataChangeNotify = dadUpdateFunction

        self._selectable = selectable

        self.name = urwid.Text(" " + self.item.name, align='left')
        self.bar = urwid.ProgressBar('normal', 'complete', self.item.downloadStatus(), satt='c')
        self.policy = urwid.Text(self.item.filePolicy.name, align='center')
        self.size = urwid.Text(self.item.memStatus(), align='center')
        self.speed = urwid.Text(self.item.speedStatus(), align='center')

        top = urwid.Columns([('weight', 8, self.name),
                             ('weight', 4, self.bar),
                             ('weight', 1, self.policy),
                             ('weight', 4, self.size),
                             ('weight', 2, self.speed)]
                            , dividechars=0)
        top = urwid.AttrMap(top, 'DownloadItem', 'DownloadItemFocus')
        super().__init__(top)

        # urwid.connect_signal(self, 'click', self.clickEvent)

    def itemUpdateData(self):
        self.name.set_text(" " + self.item.name)
        self.bar.set_completion(self.item.downloadStatus())
        self.policy.set_text(self.item.filePolicy.name)
        self.size.set_text(self.item.memStatus())
        self.speed.set_text(self.item.speedStatus())

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
        """Send 'click' signal on right button press"""
        if button != 1 or not is_mouse_press(event):
            return False

        self._emit('click')
        return True

    i = 0

    # Click
    # def clickEvent(self, objectEvent):
    #     self.i = self.i + 1
    #     self.name.set_text(["Cliccato ", str(self.i), " Volte"])

    # Notify Callback
    def downloadNotify(self, objectNotify: DownloadItem):
        self.itemUpdateData()
        if self.dataChangeNotify is not None:
            self.dataChangeNotify()

    def completeNotify(self, objectNotify: DownloadItem):
        self.itemUpdateData()
        if self.dataChangeNotify is not None:
            self.dataChangeNotify()
        # newTop = urwid.Columns([urwid.AttrMap(self.name, 'banner'), self.bar, self.size], dividechars=1)
        # top = urwid.AttrMap(newTop, 'DownloadItem', 'DownloadItemFocus')
        # self._wrapped_widget = top
