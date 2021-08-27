import urwid
from .DownloadTree import *


class RequestForm(urwid.WidgetPlaceholder):
    formCompleteNotify = None
    formAbortNotify = None

    def __init__(self, formCompleteNotify=None, formAbortNotify=None):
        self.formCompleteNotify = formCompleteNotify
        self.formAbortNotify = formAbortNotify

        close_button = urwid.Button("Click Me")
        urwid.connect_signal(close_button, 'click', self.formComplete)

        super().__init__(urwid.LineBox(urwid.Overlay(urwid.Filler(urwid.Padding(close_button, 'center', 15)),
                                                           urwid.SolidFill("\N{FULL BLOCK}"),
                                                           align='center', width=('relative', 100),
                                                           valign='middle', height=('relative', 100),
                                                           top=1, bottom=1, left=2, right=2)))

    def formComplete(self, button):
        if self.formCompleteNotify is not None:
            self.formCompleteNotify()

    def keypress(self, size, key):
        return key
