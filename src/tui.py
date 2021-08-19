import urwid


def exitTUI():
    raise urwid.ExitMainLoop()


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
    class MenuButton(urwid.Button):
        def __init__(self, caption, callback, param):
            super(MenuButton, self).__init__("")
            urwid.connect_signal(self, 'click', callback, param)
            self._w = urwid.AttrMap(urwid.SelectableIcon(
                [u'  \N{BULLET} ', caption], 2), None, 'selected')

    def menu(title, choices):
        """
        @title      := Title of the columns
        @choices    := List of Tuple, each touple are (ButtonName:str, Callback)
        """
        body = [urwid.AttrMap(urwid.Text(title, 'center'), 'heading'), urwid.Divider()]

        for c in choices:
            button = MenuButton(c[0], c[1], c[0])
            body.append(urwid.AttrMap(button, None, focus_map='reversed'))
        return urwid.ListBox(urwid.SimpleFocusListWalker(body))

    def item_chosen(button, choice):
        response = urwid.Text([u'You chose "', choice, u'"\n'])
        done = urwid.Button(u'Ok')
        urwid.connect_signal(done, 'click', exit_program)
        main.original_widget = urwid.Filler(urwid.Pile([response,
                                                        urwid.AttrMap(done, None, focus_map='reversed')]))

    def exit_program(button):
        raise urwid.ExitMainLoop()

    choices =[ ("Add Download", item_chosen),
               ("Change Download", item_chosen),
               ("Global Setting", item_chosen),
               ("Save Setting", item_chosen),
               ("Load Setting", item_chosen),
               ("Start Download", item_chosen),
               ]

    main = urwid.Padding(menu(u'Command', choices), left=2, right=2)
    # top = urwid.Columns([menuOption, urwid.SolidFill('/')])
    top = urwid.Columns(
        [('weight', 1, main), ('weight', 2, urwid.Overlay(urwid.Filler(urwid.Edit()), urwid.SolidFill('/'),
                                                          align='center', width=('relative', 80),
                                                          valign='middle', height=('relative', 80)))
         ])

    # top = urwid.Columns([menuOption, urwid.Filler(urwid.Text("ciao"))])
    return top
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
