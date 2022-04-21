import urwid


class PopUpDialogDefault(urwid.WidgetWrap):
    """A dialog that appears with nothing but a close button """
    signals = ['close']

    def __init__(self):
        close_button = urwid.Button("that's pretty cool")
        urwid.connect_signal(close_button, 'click', lambda button: self._emit("close"))
        pile = urwid.Pile([urwid.Text(
            "^^  I'm attached to the widget that opened me. "
            "Try resizing the window!\n"), close_button])
        fill = urwid.Filler(pile)
        self.__super.__init__(urwid.AttrWrap(fill, 'popbg'))


class PopUpContainer(urwid.PopUpLauncher):
    popUpWidgetRef = PopUpDialogDefault()
    widgetSizeRef = {'left': 0, 'top': -2, 'overlay_width': 60, 'overlay_height': 15}

    def __init__(self, popUpActivatorWidget, openSignalName='click', popUpWidget=None, popUpWidgetSize=None):
        super(PopUpContainer, self).__init__(popUpActivatorWidget)

        # Riassegno le variabili passate
        if popUpWidget is not None:
            self.popUpWidgetRef = popUpWidget
        if popUpWidgetSize is not None:
            self.widgetSizeRef = popUpWidgetSize

        # Quando l'attivatore emette il segnale di apertura, io apro il popup
        urwid.connect_signal(popUpActivatorWidget, openSignalName, lambda button: (self.open_pop_up()))

    def create_pop_up(self):  # deve ritornare il widget da assegnare come popup
        # Collego il segnale di chiusura del widget popup alla funzione di chiusura del popup
        urwid.connect_signal(self.popUpWidgetRef, 'close', lambda button: self.close_pop_up())
        return self.popUpWidgetRef

    def get_pop_up_parameters(self):  # assegna posizione relativa rispetto pulsante
        return self.widgetSizeRef
