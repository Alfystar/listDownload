import urwid
from .DownloadTree import *

class MenuButton(urwid.Button):
    def __init__(self, caption, callback, param):
        super(MenuButton, self).__init__("")
        urwid.connect_signal(self, 'click', callback, param)
        self._w = urwid.AttrMap(urwid.SelectableIcon(
            [u'  \N{BULLET} ', caption], 2), None, 'selected')


class CommandMenu(urwid.WidgetPlaceholder):
    downloadTree: DownloadTree = None
    def __init__(self, downloadTree: DownloadTree):
        self.downloadTree = downloadTree

        choices = [("Add Download", self.add_Request),
                   #("Change Download", self.add_Request),
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

    def add_Request(self, button, choice):
        #todo: Creare widget popup per chiedere i dati parametrici all'utente
        rc = ListRequest("https://www.egr.msu.edu/~khalil/NonlinearSystems/Sample/Lect_", ".pdf", 1, 5)
        self.downloadTree.addRequest(rc)


    def exit_program(self, button):
        raise urwid.ExitMainLoop()
