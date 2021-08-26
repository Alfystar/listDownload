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

        # self.original_widget = urwid.Text("CIAOOOO")
        # self.original_widget = urwid.SolidFill("/")
        self.original_widget = urwid.Filler(urwid.Padding(close_button, 'center', 15))

    def formComplete(self, button):
        if self.formCompleteNotify is not None:
            self.formCompleteNotify()

    def keypress(self, size, key):
        return key
