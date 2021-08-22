import urwid
from .CommandMenu import *
from .DownloadTree import *

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
    ('body', 'white', 'black'),
    ('focus', 'light gray', 'dark blue', 'standout'),
    ('bars', 'dark blue', 'light gray', ''),
    ('arrowtip', 'light blue', 'light gray', ''),
    ('connectors', 'light red', 'light gray', ''),
]

focus_map = {
    'heading': 'focus heading',
    'options': 'focus options',
    'line': 'focus line'}


def makeHeader():
    # big title
    bt = urwid.BigText(('title', " List Download "), urwid.font.HalfBlock5x4Font())
    bt = urwid.AttrMap(bt, 'streak')
    bt = urwid.Padding(bt, "center", None)
    # Versioning info
    version = urwid.Text(('banner', u" Version 2.0.0 "), align='right')

    # Final mount
    head = urwid.Pile([bt, version])
    return head


def makeBody():
    rightSide = CommandMenu()
    leftSide = DownloadTree(RequestConteiner())
    # leftSide = urwid.Overlay(urwid.Filler(urwid.Edit()), urwid.SolidFill('/'),
    #                          align='center', width=('relative', 80),
    #                          valign='middle', height=('relative', 80))
    top = urwid.Columns(
        [('weight', 1, rightSide), ('weight', 3, leftSide)
         ])
    return top


def makeFooter():
    return urwid.LineBox(urwid.Pile([
        urwid.Text("Program key"),
        urwid.Text("CommandList := ←↑↓→ navigate, 'Enter' to select form button."),
        urwid.Text("DownloadTree:= ←↑↓→ navigate, -/+ collapse/expand, C/E allVariant, '['/']' Same level move"),
        # urwid.Divider()
    ]))


def makeTopWindows():
    top = urwid.Frame(makeBody(), makeHeader(), makeFooter())
    return top


def exitTUI():
    raise urwid.ExitMainLoop()
