"""GUI class definition for main window
"""

from tkinter import CENTER, X, YES

from tkinter.ttk import Frame, Label


class AppWin(Frame):

    def __init__(self, master=None, **kw):

        # root Tk
        self.master = master

        self.master.title(kw.get(
            'app_title',
            ' py3100G810 - Collect of weight and humidity of grains'
            )
        )

        Frame.__init__(self, master, **kw)

        Label(
            self,
            font='size 16 bold',
            text='{0}\n{1}'.format(
                '   py3100G810 - Collect of weight  ',
                '           and humidity of grains'
            ),
            background='light blue',
            foreground='dark green'
        ).pack(
            fill=X,
            expand=YES,
            anchor=CENTER
        )
