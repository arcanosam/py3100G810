"""entry point for Pysync-dev module
"""

from tkinter import Tk, BOTH

from gui.app_win import AppWin


if __name__ == '__main__':

    root = Tk()

    py3100g810_app = AppWin(root)

    py3100g810_app.pack(fill=BOTH, expand=1)

    root.mainloop()
