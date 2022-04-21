import urwid

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
    # Popup Palette
    ('popbg', 'white', 'dark blue')
]

focus_map = {
    'heading': 'focus heading',
    'options': 'focus options',
    'line': 'focus line'}


# Creo l'istanza eseguibile
def uiStart(topWidget):
    global loop
    screen = urwid.raw_display.Screen()
    screen.set_terminal_properties(256)
    loop = urwid.MainLoop(topWidget, palette=palette,
                          screen=screen,
                          unhandled_input=global_input,
                          pop_ups=True
                          )
    loop.run()


def global_input(key):
    if key in ('q', 'Q'):
        raise urwid.ExitMainLoop()


def coolButton(caption):
    buttonCool = urwid.Button("")
    super(urwid.Button, buttonCool).__init__(
        urwid.AttrMap(urwid.SelectableIcon([u'  \N{BULLET} ', caption], 2), None, 'selected'))
    return buttonCool


# We use selectable Text widgets for our example..
# Selezionabili ma non modificabili, se non fossero selezionabili, il cursore li salterebbe!

class FocusableText(urwid.WidgetWrap):
    """Selectable Text used for nodes in our example"""

    def __init__(self, txt):
        t = urwid.Text(txt)
        w = urwid.AttrMap(t, 'DownloadItem', 'DownloadItemFocus')
        urwid.WidgetWrap.__init__(self, w)

    def selectable(self):
        return True

    def keypress(self, size, key):
        return key
