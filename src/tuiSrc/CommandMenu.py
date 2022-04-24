from src.tuiSrc.PopUpContainer import PopUpContainer
from src.tuiSrc.requestTypeFormsWidget.ListRequestForm import *
from src.tuiSrc.tuiGlobal import coolButton


class CommandMenu(urwid.WidgetPlaceholder):

    # ***Event are calls-back, called when button are clicked, they recive: ***Event(button, choiseStr)
    def __init__(self, addDownloadEvent=None, downloadStartEvent=None):

        body = [urwid.AttrMap(urwid.Text('Command', 'center'), 'heading'), urwid.Divider()]

        # Add Download
        addButton = coolButton("Add Download")
        addForm = ListRequestForm(formCompleteNotify=addDownloadEvent)
        addPopUp = PopUpContainer(addButton, 'click', None, addForm, addForm.getDimension())
        body.append(urwid.AttrMap(addPopUp, None, focus_map='reversed'))

        # GlobalSetting
        globButton = coolButton("Global Setting")
        globPopUp = PopUpContainer(globButton)
        body.append(urwid.AttrMap(globPopUp, None, focus_map='reversed'))

        # Save Setting
        saveButton = coolButton("Save Setting")
        savePopUp = PopUpContainer(saveButton)
        body.append(urwid.AttrMap(savePopUp, None, focus_map='reversed'))

        # Start Download
        startButton = coolButton("Start Download")
        if downloadStartEvent is not None:
            urwid.connect_signal(startButton, 'click', downloadStartEvent)
        body.append(urwid.AttrMap(startButton, None, focus_map='reversed'))

        listCommand = urwid.ListBox(urwid.SimpleFocusListWalker(body))
        super().__init__(urwid.Padding(listCommand, left=2, right=2))

    # Debug Event
    def item_chosen(self, button, choice):
        response = urwid.Text([u'You chose "', choice, u'"\n'])
        done = urwid.Button(u'Ok')
        urwid.connect_signal(done, 'click', self.exit_program)
        self.original_widget = urwid.Filler(urwid.Pile([response, urwid.AttrMap(done, None, focus_map='reversed')]))

    def exit_program(self, button):
        raise urwid.ExitMainLoop()
