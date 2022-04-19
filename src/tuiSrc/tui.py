import urwid

from .CommandMenu import *
from .RequestForm import *
from .DownloadTree import *


class mainWidget(urwid.WidgetWrap):
    topWindow = None  # The most high widget level , it contain everything
    originalBody = None  # Variable for store real body when Form steal the scene

    downloadTreeView = None
    loop: urwid.MainLoop = None

    palette = [
        ('reversed', 'standout', ''),
        ('title', 'dark cyan', 'black'),
        ('banner', 'black', 'light gray'),
        ('streak', 'black', 'dark red'),
        ('bg', 'black', 'dark blue'),
        (None, 'light gray', 'black'),
        ('heading', 'black', 'light gray'),
        ('line', 'black', 'light gray'),
        ('options', 'dark gray', 'black'),
        ('focus heading', 'white', 'dark red'),
        ('focus line', 'black', 'dark red'),
        ('focus options', 'black', 'light gray'),
        ('selected', 'white', 'dark blue'),
        # TreeView Palette
        ('body', 'white', 'black'),
        ('focus', 'black', 'dark red', 'standout'),
        ('bars', 'dark blue', 'light gray', ''),
        ('arrowtip', 'light blue', 'light gray', ''),
        ('connectors', 'light red', 'light gray', ''),
        # Download Tree item:
        ('DownloadItem', 'white', 'black'),  # like body
        ('DownloadItemFocus', 'light gray', 'dark blue'),
        # ProgressBar Palette
        ('normal', 'black', 'light gray'),
        ('complete', 'black', 'dark red'),
        ('normalTot', 'black', 'light blue'),
        ('completeTot', 'black', 'dark green'),
    ]

    focus_map = {
        'heading': 'focus heading',
        'options': 'focus options',
        'line': 'focus line'}

    def __init__(self):
        self.topWindow = self.makeTopWindows()
        super().__init__(self.topWindow)
        screen = urwid.raw_display.Screen()
        screen.set_terminal_properties(256)
        self.loop = urwid.MainLoop(self, palette=self.palette,
                                   screen=screen,
                                   unhandled_input=self.global_input
                                   )

    def global_input(self, key):
        if key in ('q', 'Q'):
            raise urwid.ExitMainLoop()
        elif key == "r":
            self.loop.screen.stop()
            self.loop.screen.start()
            self.loop.draw_screen()

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

    """Callback chiamata dalla RequestForm quando è stata correttamente impostata"""
    def addRequestComplete_callBack(self):
        rc = ListRequest("https://www.egr.msu.edu/~khalil/NonlinearSystems/Sample/Lect_", ".pdf", 1, 5)
        self.downloadTreeView.addRequest(rc)

        # Restoro il body originale
        self.topWindow._body = self.originalBody

    def add_RequestForm(self, button, choice):
        print(button, choice)
        requestForm = RequestForm(self.addRequestComplete_callBack)

        # Show on the display the Request Form
        self.topWindow._body = urwid.Overlay(requestForm , self.originalBody,
                                             align='center', width=('relative', 70),
                                             valign='bottom', height=('relative', 70))
        # self.topWindow._body = requestForm


    def makeBody(self):
        RequestList = [ListRequest("https://www.egr.msu.edu/~khalil/NonlinearSystems/Sample/Lect_", ".pdf", 1, 5),
                       ListRequest("https://www.egr.msu.edu/~khalil/NonlinearSystems/Sample/Lect_", ".pdf", 15, 20)]
        self.downloadTreeView = DownloadTree(RequestList)
        leftSide = urwid.Overlay(self.downloadTreeView, urwid.SolidFill("-"),
                                 align='left', width=('relative', 100),
                                 valign='bottom', height=('relative', 100),
                                 top=1)
        rightSide = CommandMenu(addDownloadEvent=self.add_RequestForm)

        top = urwid.Columns([('weight', 2, rightSide), ('weight', 7, leftSide)])
        return top

    def makeFooter(self):
        return urwid.LineBox(urwid.Pile([
            urwid.Text("Program key"),
            urwid.Text("CommandList := ←↑↓→ navigate, 'Enter' to select form button."),
            urwid.Text("DownloadTree:= ←↑↓→ navigate, -/+ collapse/expand, C/E allVariant, '['/']' Same level move"),
            # urwid.Divider()
        ]))

    def makeTopWindows(self):
        self.originalBody = self.makeBody()
        self.topWindow = urwid.Frame(self.originalBody, self.makeHeader(), self.makeFooter())
        return self.topWindow

    def exitTUI(self):
        raise urwid.ExitMainLoop()

    # def keypress(self, size, key):
    #     return key
