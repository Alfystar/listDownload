import urwid
from .DownloadTree import *


class PopUpDialog(urwid.WidgetWrap):
    """A dialog that appears with nothing but a close button """
    signals = ['close']

    def __init__(self):
        close_button = urwid.Button("that's pretty cool")
        urwid.connect_signal(close_button, 'click', lambda button: self._emit("close"))
        pile = urwid.Pile([urwid.Text(
            "^^  I'm attached to the widget that opened me. "
            "Try resizing the window!\n"), close_button])
        fill = urwid.Filler(pile)
        self.__super.__init__(urwid.AttrWrap(fill, 'popbg'))


class RequestForm(urwid.WidgetWrap):
    signals = ['close']
    formCompleteNotify = None
    formAbortNotify = None

    def __init__(self, formCompleteNotify=None):
        self.formCompleteNotify = formCompleteNotify

        listBody = [urwid.AttrMap(urwid.Text("Parametri", 'center'), 'heading'), urwid.Divider()]

        # Input cell
        self.basePath = urwid.Edit(u"BasePath   := ")
        self.endPath = urwid.Edit(u"EndPath    := ")
        self.startIndexText = urwid.Edit(u"StartIndex := ")
        self.endIndexText = urwid.Edit(u"EndIndex   := ")
        self.nDigitText = urwid.Edit(u"Digit n°   := ")

        self.resetParam()

        # Button send
        self.enterButton = urwid.AttrMap(urwid.Button("Add download request"), 'popbg')
        urwid.connect_signal(self.enterButton.original_widget, 'click', self.formComplete)

        # Info Area
        self.infoText = urwid.Text("Info Area:\n", align='center')

        listBody.append(self.basePath)
        listBody.append(self.endPath)
        listBody.append(self.startIndexText)
        listBody.append(self.endIndexText)
        listBody.append(self.nDigitText)
        listBody.append(urwid.Divider())
        listBody.append(self.enterButton)
        listBody.append(urwid.Divider())
        listBody.append(self.infoText)

        list = urwid.ListBox(urwid.SimpleFocusListWalker(listBody))
        list.set_focus = 0

        super().__init__(urwid.LineBox(list))

    def resetParam(self, base="https://www.egr.msu.edu/~khalil/NonlinearSystems/Sample/Lect_", end=".pdf", startIndex=0, endIndex=0, digit=2):
        # default Val
        self.basePath.set_edit_text(base)
        self.endPath.set_edit_text(end)

        self.startIndexText.set_edit_text(str(startIndex))
        self.endIndexText.set_edit_text(str(endIndex))
        self.nDigitText.set_edit_text(str(digit))

    def getDimension(self):
        return {'left': 0, 'top': -2, 'overlay_width': 90, 'overlay_height': 15}

    def formComplete(self, button):
        basePathStr = self.basePath.get_edit_text()
        endPathStr = self.endPath.get_edit_text()
        startIndexStr = self.startIndexText.get_edit_text()
        endIndexStr = self.endIndexText.get_edit_text()
        nDigitStr = self.nDigitText.get_edit_text()

        if len(basePathStr) == 0:
            self.infoText.set_text("Info Area:\nBasePath Missing, please add base_url")
            return
        if len(endPathStr) == 0:
            self.infoText.set_text("Info Area:\nEndPath Missing, please add end_url")
            return
        if not startIndexStr.isnumeric():
            self.infoText.set_text("Info Area:\nStart index isn't number, please insert a number")
            return
        if not endIndexStr.isnumeric():
            self.infoText.set_text("Info Area:\nEnd index isn't number, please insert a number")
            return
        if not nDigitStr.isnumeric():
            self.infoText.set_text("Info Area:\nDigit number isn't number, please insert a number")
            return

        valid = True
        if self.formCompleteNotify is not None:
            valid = self.formCompleteNotify(basePathStr, endPathStr,
                                            int(startIndexStr), int(endIndexStr), int(nDigitStr))

        if type(valid) != str:
            self._emit("close")
        else:
            self.infoText.set_text("Info Area:\n" + valid)

    def keypress(self, size, key):
        if key == 'esc':
            self._emit("close")
            return None
        if key == 'enter':  # Se premo enter è come se premessi il pulsante di chiusura
            self.formComplete(self.enterButton)
            return None
        return super().keypress(size, key)
