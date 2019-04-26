"""entry point for Pysync-dev module
"""

from tkinter import Tk, BOTH

from gui.app_win import AppWin

def tk_configs(_master):

    w = 381
    h = 347

    # user screen(monitor) dimensions
    ws = _master.winfo_screenwidth()
    hs = _master.winfo_screenheight()

    # fixing minimal window size
    _master.minsize(w, h)

    # center window
    _master.geometry(
        '%dx%d+%d+%d' % (
            w,
            h,
            (ws / 2) - (w / 2),
            (hs / 2) - (h / 2)
        )
    )


if __name__ == '__main__':

    root = Tk()

    tk_configs(root)

    py3100g810_app = AppWin(root)

    py3100g810_app.pack()

    root.mainloop()
