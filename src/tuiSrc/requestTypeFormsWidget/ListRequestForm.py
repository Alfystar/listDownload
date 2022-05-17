import urwid

from src.listDownloadSrc.requestTypes.ListRequest import ListRequest


class ListRequestForm(urwid.WidgetWrap):
    signals = ['close']
    formCompleteNotify = None
    formAbortNotify = None

    def __init__(self, formCompleteNotify=None):
        self.formCompleteNotify = formCompleteNotify

        listBody = [urwid.AttrMap(urwid.Text("Parametri", 'center'), 'heading'), urwid.Divider()]

        # Input cell
        self.parametricPath = urwid.Edit(
            u"              «Use '#' for index, as many as the minimum digit you need»\nPath       := ")
        self.startIndexText = urwid.Edit(u"StartIndex := ")
        self.endIndexText = urwid.Edit(u"EndIndex   := ")

        self.resetParam()

        # Button send
        self.enterButton = urwid.AttrMap(urwid.Button("Add download request"), 'popbg')
        urwid.connect_signal(self.enterButton.original_widget, 'click', self.formComplete)

        # Info Area
        self.infoText = urwid.Text("Info Area:\n", align='center')

        listBody.append(self.parametricPath)
        listBody.append(self.startIndexText)
        listBody.append(self.endIndexText)
        listBody.append(urwid.Divider())
        listBody.append(self.enterButton)
        listBody.append(urwid.Divider())
        listBody.append(self.infoText)

        list = urwid.ListBox(urwid.SimpleFocusListWalker(listBody))
        list.set_focus = 0

        super().__init__(urwid.LineBox(list))

    # todo: finito lo sviluppo mettere i corretti valori di default
    def resetParam(self, base="", startIndex=0, endIndex=0):
        # default Val
        self.parametricPath.set_edit_text(base)
        self.startIndexText.set_edit_text(str(startIndex))
        self.endIndexText.set_edit_text(str(endIndex))

    def getDimension(self):
        return {'left': 0, 'top': -2, 'overlay_width': 90, 'overlay_height': 15}

    def formComplete(self, button):
        parametricPathStr = self.parametricPath.get_edit_text()
        startIndexStr = self.startIndexText.get_edit_text()
        endIndexStr = self.endIndexText.get_edit_text()

        if len(parametricPathStr) == 0:
            self.infoText.set_text("Info Area:\nParametricPath Missing, please add parametric_url")
            return
        if not startIndexStr.isnumeric():
            self.infoText.set_text("Info Area:\nStart index isn't number, please insert a number")
            return
        if not endIndexStr.isnumeric():
            self.infoText.set_text("Info Area:\nEnd index isn't number, please insert a number")
            return

        valid = True
        if self.formCompleteNotify is not None:
            rc = ListRequest(parametricPathStr, int(startIndexStr), int(endIndexStr))
            valid = self.formCompleteNotify(rc)

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
