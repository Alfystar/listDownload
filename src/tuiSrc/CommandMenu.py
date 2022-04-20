import urwid
from .DownloadTree import *
from .RequestForm import *


class popUpButtonActivator(urwid.PopUpLauncher):
    popUpWidgetRef = PopUpDialog()
    widgetSizeRef = {'left': 0, 'top': -2, 'overlay_width': 60, 'overlay_height': 15}

    def __init__(self, caption, popUpWidget=None, widgedSize=None):
        # Genero il bottone, ma il nome lo scrivo attraverso l'icona selezionabile
        super(popUpButtonActivator, self).__init__(urwid.Button(caption))
        self.original_widget._w = urwid.AttrMap(urwid.SelectableIcon([u'  \N{BULLET} ', caption], 2), None, 'selected')

        # Riassegno le variabili passate
        if popUpWidget is not None:
            self.popUpWidgetRef = popUpWidget
        if widgedSize is not None:
            self.widgetSizeRef = widgedSize

        # Connetto il segnale per mostrare il popup
        urwid.connect_signal(self.original_widget, 'click', lambda button: (self.open_pop_up(), self.popUpWidgetRef.resetParam()))

    def create_pop_up(self):  # Genera in loco un widget, e in questo caso assegna al pulsante la chiusura
        urwid.connect_signal(self.popUpWidgetRef, 'close', lambda button: self.close_pop_up())
        return self.popUpWidgetRef

    def get_pop_up_parameters(self):  # assegna posizione relativa rispetto pulsante
        return self.widgetSizeRef


class CommandMenu(urwid.WidgetPlaceholder):

    # ***Event are calls-back, called when button are clicked, they recive: ***Event(button, choiseStr)
    def __init__(self, addDownloadEvent=None, globSetEvent=None, saveEvent=None, LoadEvent=None,
                 downloadStartEvent=None):
        requestForm = RequestForm(formCompleteNotify=addDownloadEvent)

        choices = [("Add Download", requestForm, requestForm.getDimension()),
                   # ("Change Download", self.add_Request),
                   ("Global Setting", None, None,),
                   ("Save Setting",  None, None,),
                   ("Load Setting",  None, None,),
                   ("Start Download",  None, None,),
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
            button = popUpButtonActivator(c[0], c[1], c[2])
            body.append(urwid.AttrMap(button, None, focus_map='reversed'))
        return urwid.ListBox(urwid.SimpleFocusListWalker(body))

    def item_chosen(self, button, choice):
        response = urwid.Text([u'You chose "', choice, u'"\n'])
        done = urwid.Button(u'Ok')
        urwid.connect_signal(done, 'click', self.exit_program)
        self.original_widget = urwid.Filler(urwid.Pile([response, urwid.AttrMap(done, None, focus_map='reversed')]))

    def exit_program(self, button):
        raise urwid.ExitMainLoop()
