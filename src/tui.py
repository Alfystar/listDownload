import urwid


def exit_on_q(key):
    if key in ('q', 'Q'):
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
        def __init__(self, caption, callback):
            super(MenuButton, self).__init__("")
            urwid.connect_signal(self, 'click', callback)
            self._w = urwid.AttrMap(urwid.SelectableIcon(
                [u'  \N{BULLET} ', caption], 2), None, 'selected')

    class SubMenu(urwid.WidgetWrap):
        def __init__(self, caption, choices):
            super(SubMenu, self).__init__(MenuButton(
                [caption, u"\N{HORIZONTAL ELLIPSIS}"], self.open_menu))
            line = urwid.Divider(u'\N{LOWER ONE QUARTER BLOCK}')
            listbox = urwid.ListBox(urwid.SimpleFocusListWalker([
                                                                    urwid.AttrMap(urwid.Text([u"\n  ", caption]),
                                                                                  'heading'),
                                                                    urwid.AttrMap(line, 'line'),
                                                                    urwid.Divider()] + choices + [urwid.Divider()]))
            self.menu = urwid.AttrMap(listbox, 'options')

        def open_menu(self, button):
            top.open_box(self.menu)

    class Choice(urwid.WidgetWrap):
        def __init__(self, caption):
            super(Choice, self).__init__(
                MenuButton(caption, self.item_chosen))
            self.caption = caption

        def item_chosen(self, button):
            response = urwid.Text([u'  You chose ', self.caption, u'\n'])
            done = MenuButton(u'Ok', exit_program)
            response_box = urwid.Filler(urwid.Pile([response, done]))
            top.open_box(urwid.AttrMap(response_box, 'options'))

    def exit_program(key):
        raise urwid.ExitMainLoop()

    menu_top = SubMenu(u'Main Menu', [
        SubMenu(u'Applications', [
            SubMenu(u'Accessories', [
                Choice(u'Text Editor'),
                Choice(u'Terminal'),
            ]),
        ]),
        SubMenu(u'System', [
            SubMenu(u'Preferences', [
                Choice(u'Appearance'),
            ]),
            Choice(u'Lock Screen'),
        ]),
    ])

    class HorizontalBoxes(urwid.Columns):
        def __init__(self):
            super(HorizontalBoxes, self).__init__([], dividechars=1)

        def open_box(self, box):
            if self.contents:
                del self.contents[self.focus_position + 1:]
            self.contents.append((urwid.AttrMap(box, 'options', focus_map),
                                  self.options('given', 24)))
            self.focus_position = len(self.contents) - 1

    top = HorizontalBoxes()
    top.open_box(menu_top.menu)
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
