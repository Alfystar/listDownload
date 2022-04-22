from src.tuiSrc.PopUpContainer import PopUpContainer
from src.tuiSrc.requestTypeFormsWidget.ListRequestForm import *
from src.tuiSrc.tuiGlobal import coolButton


class CommandMenu(urwid.WidgetPlaceholder):

    # ***Event are calls-back, called when button are clicked, they recive: ***Event(button, choiseStr)
    def __init__(self, addDownloadEvent=None, globSetEvent=None, saveEvent=None, LoadEvent=None,
                 downloadStartEvent=None):
        requestForm = ListRequestForm(formCompleteNotify=addDownloadEvent)

        choices = [("Add Download", requestForm, requestForm.getDimension()),
                   # ("Change Download", self.add_Request),
                   ("Global Setting", None, None,),
                   ("Save Setting", None, None,),
                   ("Load Setting", None, None,),
                   ("Start Download", None, None,),
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
            button = PopUpContainer(coolButton(c[0]), 'click',None, c[1], c[2])
            body.append(urwid.AttrMap(button, None, focus_map='reversed'))
        return urwid.ListBox(urwid.SimpleFocusListWalker(body))

    def item_chosen(self, button, choice):
        response = urwid.Text([u'You chose "', choice, u'"\n'])
        done = urwid.Button(u'Ok')
        urwid.connect_signal(done, 'click', self.exit_program)
        self.original_widget = urwid.Filler(urwid.Pile([response, urwid.AttrMap(done, None, focus_map='reversed')]))

    def exit_program(self, button):
        raise urwid.ExitMainLoop()
