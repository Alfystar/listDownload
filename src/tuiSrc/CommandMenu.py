import urwid


class MenuButton(urwid.Button):
    def __init__(self, caption, callback, param):
        super(MenuButton, self).__init__("")
        urwid.connect_signal(self, 'click', callback, param)
        self._w = urwid.AttrMap(urwid.SelectableIcon(
            [u'  \N{BULLET} ', caption], 2), None, 'selected')


class CommandMenu(urwid.WidgetPlaceholder):
    def __init__(self):
        choices = [("Add Download", self.item_chosen),
                   ("Change Download", self.item_chosen),
                   ("Global Setting", self.item_chosen),
                   ("Save Setting", self.item_chosen),
                   ("Load Setting", self.item_chosen),
                   ("Start Download", self.item_chosen),
                   ]
        self.original_widget = urwid.Padding(self.menu(u'Command', choices), left=2, right=2)

    def menu(self, title, choices):
        """
        @title      := Title of the columns
        @choices    := List of Tuple, each touple are (ButtonName:str, Callback)
        """
        body = [urwid.AttrMap(urwid.Text(title, 'center'), 'heading'), urwid.Divider()]

        for c in choices:
            button = MenuButton(c[0], c[1], c[0])
            body.append(urwid.AttrMap(button, None, focus_map='reversed'))
        return urwid.ListBox(urwid.SimpleFocusListWalker(body))

    def item_chosen(self, button, choice):
        response = urwid.Text([u'You chose "', choice, u'"\n'])
        done = urwid.Button(u'Ok')
        urwid.connect_signal(done, 'click', self.exit_program)
        self.original_widget = urwid.Filler(urwid.Pile([response, urwid.AttrMap(done, None, focus_map='reversed')]))

    def exit_program(self, button):
        raise urwid.ExitMainLoop()
