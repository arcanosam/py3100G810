"""GUI class definition for main window
"""

from tkinter import CENTER, TOP, W, X, YES

from tkinter.ttk import Entry, Frame, Label

from gui.app_def import get_app_definitions


class AppWin(Frame):

    def __init__(self, master=None, **kw):

        self.bar_qr_code = None

        # root Tk
        self.master = master

        self.master.title(
            get_app_definitions('app_root_title')
        )

        Frame.__init__(self, master, **kw)

        self.add_title_app()

        self.add_ipt_id_code()

    def add_title_app(self):

        Label(
            self,
            font='size 16 bold',
            text='{0}\n{1}'.format(
                get_app_definitions('app_title_01'),
                get_app_definitions('app_title_02')
            ),
            background='light blue',
            foreground='dark green'
        ).pack(
            fill=X,
            expand=YES,
            anchor=CENTER
        )

    def add_ipt_id_code(self):

        Label(
            self,
            font='size 13 bold',
            text=get_app_definitions('app_label_edit'),
            background='white',
            foreground='green'
        ).pack(
            anchor=W,
            side=TOP,
            fill=X
        )

        self.bar_qr_code = Entry(
            self,
            font='Courier 14 bold'
        )

        self.bar_qr_code.pack(fill=X)

        self.bar_qr_code.focus()
