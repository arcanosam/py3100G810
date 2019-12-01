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

        quote = """LICENÇA
=====================================
Este software usa código livre do projeto https://github.com/arcanosam/py3100G810 cuja licença é reproduzida abaixo:


MIT License

Copyright (c) 2019 Samuel Teixeira Santos

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


Demais códigos livre reutilizados/readaptados:
=====================================

KYLE KOWALCZYK - Python Tkinter Password Entry Box
Origem: https://smallguysit.com/index.php/2017/03/13/python-tkinter-password-entry-box/


ActiveState Code - An Entry With Autocompletion For The Tkinter GUI (Python Recipe) 
Origem: http://code.activestate.com/recipes/578253-an-entry-with-autocompletion-for-the-tkinter-gui/
"""
        self.txt.insert(END, quote)

        self.txt.config(state=DISABLED)

        Button(
            self,
            text=get_app_definitions('about_win_btn'),
            command=self.destroy
        ).grid(row=1, column=0, padx=2, pady=2)

    def _close_about(self):

        self.destroy()
