"""GUI class definition for main window
"""


from tkinter.ttk import Frame


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
