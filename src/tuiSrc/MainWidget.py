from .CommandMenu import *
from .DownloadTree import *
from ..listDownloadSrc.requestTypes.ListRequest import ListRequest


class MainWidget(urwid.WidgetWrap):
    topWindow = None  # The most high widget level , it contain everything
    originalBody = None  # Variable for store real body when Form steal the scene

    downloadTreeView = None

    def __init__(self):
        # Genero il TopLevel Widget, il quale è un frame (con le sue 3 Zone)
        self.topWindow = urwid.Frame(self.makeBody(), self.makeHeader(), self.makeFooter())
        super().__init__(self.topWindow)

    def makeHeader(self):
        # big title
        bt = urwid.BigText(('title', " List Download "), urwid.font.HalfBlock5x4Font())
        bt = urwid.AttrMap(bt, 'streak')
        bt = urwid.Padding(bt, "center", None)
        # Versioning info
        version = urwid.Text(('banner', u" Version 2.0.0 "), align='right')

        # Final mount
        head = urwid.Pile([bt, version])
        return head

    def makeBody(self):
        # todo: da rimuovere, presenti solo per debug
        RequestList = [ListRequest("https://www.egr.msu.edu/~khalil/NonlinearSystems/Sample/Lect_", ".pdf", 1, 5),
                       ListRequest("https://www.egr.msu.edu/~khalil/NonlinearSystems/Sample/Lect_", ".pdf", 15, 20)]
        self.downloadTreeView = DownloadTree(RequestList)
        leftSide = urwid.Overlay(self.downloadTreeView, urwid.SolidFill("-"),
                                 align='left', width=('relative', 100),
                                 valign='bottom', height=('relative', 100),
                                 top=1)
        rightSide = CommandMenu(addDownloadEvent=self.addRequestComplete_callBack)

        top = urwid.Columns([('weight', 2, rightSide), ('weight', 7, leftSide)])
        return top

    def makeFooter(self):
        return urwid.LineBox(urwid.Pile([
            urwid.Text("Program key"),
            urwid.Text("CommandList := ←↑↓→ navigate, 'Enter' to select form button."),
            urwid.Text("DownloadTree:= ←↑↓→ navigate, -/+ collapse/expand, C/E allVariant, '['/']' Same level move."),
            # urwid.Divider()
        ]))

    """
    Callbacks Zone
    """

    def addRequestComplete_callBack(self, rc):
        # rc = ListRequest("https://www.egr.msu.edu/~khalil/NonlinearSystems/Sample/Lect_", ".pdf", 1, 5)
        try:
            self.downloadTreeView.addRequest(rc)
        except Exception as e:
            return str(e)
        return True
