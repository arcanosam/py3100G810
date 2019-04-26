"""About window
"""

from tkinter import DISABLED, END, Toplevel, WORD
from tkinter.ttk import Button
from tkinter.scrolledtext import ScrolledText

from gui.app_def import get_app_definitions


class AboutWin(Toplevel):

    def __init__(self, master=None):

        # root Tk
        self._parent = master

        Toplevel.__init__(self, master)

        w = self.master.winfo_width()
        h = self.master.winfo_height()

        ws = master.winfo_screenwidth()
        hs = master.winfo_screenheight()

        # center window
        self.geometry(
            '%dx%d+%d+%d' % (
                w,
                h,
                (ws / 2) - (w / 2),
                (hs / 2) - (h / 2)
            )
        )

        self.resizable(width=False, height=False)

        self.transient(master)

        self.focus_force()  # added
        self.grab_set()

        self.grid_propagate(False)

        # implement stretchability
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.txt = ScrolledText(self, wrap=WORD)
        self.txt['font'] = ('Courier New', '10')
        # ensure a consistent GUI size

        self.txt.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)

        with open('./LICENSE') as f:
            license_text = f.read()

        quote = """LICENÇA
=====================================
Este software usa código livre do projeto https://github.com/arcanosam/py3100G810 cuja licença é reproduzida abaixo:


{0}


Demais códigos livre reutilizados/readaptados:
=====================================

KYLE KOWALCZYK - Python Tkinter Password Entry Box
Origem: https://smallguysit.com/index.php/2017/03/13/python-tkinter-password-entry-box/


ActiveState Code - An Entry With Autocompletion For The Tkinter GUI (Python Recipe) 
Origem: http://code.activestate.com/recipes/578253-an-entry-with-autocompletion-for-the-tkinter-gui/
""".format(license_text)

        f.close()

        self.txt.insert(END, quote)

        self.txt.config(state=DISABLED)

        Button(
            self,
            text=get_app_definitions('about_win_btn'),
            command=self.destroy
        ).grid(row=1, column=0, padx=2, pady=2)

    def _close_about(self):

        self.destroy()
