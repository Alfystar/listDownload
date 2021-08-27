import urwid
from .DownloadTree import *


class MenuButton(urwid.Button):
    def __init__(self, caption, callback, param):
        super(MenuButton, self).__init__("")
        if callback is not None:
            urwid.connect_signal(self, 'click', callback, param)
        self._w = urwid.AttrMap(urwid.SelectableIcon(
            [u'  \N{BULLET} ', caption], 2), None, 'selected')


class CommandMenu(urwid.WidgetPlaceholder):

    # ***Event are calls-back, called when button are clicked, they recive: ***Event(button, choiseStr)
    def __init__(self, addDownloadEvent=None, globSetEvent=None, saveEvent=None, LoadEvent=None,
                 downloadStartEvent=None):
        choices = [("Add Download", addDownloadEvent),
                   # ("Change Download", self.add_Request),
                   ("Global Setting", globSetEvent),
                   ("Save Setting", saveEvent),
                   ("Load Setting", LoadEvent),
                   ("Start Download", downloadStartEvent),
                   ]
        super().__init__(urwid.Padding(self.menu(u'Command', choices), left=2, right=2))

    def menu(self, title, choices):
        """
        @title      := Title of the columns
        @choices    := List of Tuple, each touple are (ButtonName:str, Callback)
        """
        body = [urwid.AttrMap(urwid.Text(title, 'center'), 'heading'), urwid.Divider()]

        # Draw the element passed form choices
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

    # def keypress(self, size, key):
    #     return key
