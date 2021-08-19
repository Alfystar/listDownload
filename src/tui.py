import urwid
from .tuiSrc.CommandMenu import *

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
    ('selected', 'white', 'dark blue')
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
    leftSide = urwid.Overlay(urwid.Filler(urwid.Edit()), urwid.SolidFill('/'),
                             align='center', width=('relative', 80),
                             valign='middle', height=('relative', 80))
    top = urwid.Columns(
        [('weight', 1, rightSide), ('weight', 2, leftSide)
         ])
    return top


def makeFooter():
    return urwid.LineBox(urwid.Pile([
        urwid.Text("Create Equipment"),
        urwid.Text("Arrow: ←↑↓→ keys navigate, 'Enter' to select form button. 'Esc' to come back."),
        urwid.Text("Mouse is valid input."),
        # urwid.Divider()
    ]))


def makeTopWindows():
    top = urwid.Frame(makeBody(), makeHeader(), makeFooter())
    return top


def exitTUI():
    raise urwid.ExitMainLoop()
