import urwid


def makeTopWindows():
    txt = urwid.Text(u"Hello World")
    top = urwid.Filler(txt, 'top')
    return top
