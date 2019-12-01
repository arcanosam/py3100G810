"""implementing an autocomplete entry widget in tkinter

    Original source:
        http://code.activestate.com/recipes/578253-an-entry-with-autocompletion-for-the-tkinter-gui/

    #TODO
    - Should must edit to integrate with the database
"""

from tkinter import ACTIVE, END, Listbox, StringVar
from tkinter.ttk import Entry
import re


class AutocompleteEntry(Entry):

    def __init__(self, list_qrbarcodes_db_values, *args, **kwargs):

        Entry.__init__(self, *args, **kwargs)

        self.list_qrbarcodes_db_values = list_qrbarcodes_db_values

        self.lb = None

        self._after_id = None

        self.var = StringVar()

        self.config(textvariable=self.var)

        # self.var.trace('w', self.changed)

        self.bind('<Return>', self.selection)
        self.bind('<Right>', self.selection)
        self.bind('<Up>', self.up)
        self.bind('<Down>', self.down)
        self.bind('<Key>', self.handle_wait)

        self.lb_up = False

    def handle_wait(self, event):
        # cancel the old job
        if self._after_id is not None:
            self.after_cancel(self._after_id)

        # create a new job
        self._after_id = self.after(1000, self.changed)

    def changed(self, name=None, index=None, mode=None):

        if self.var.get() == '':
            if hasattr(self, 'lb'):
                if self.lb:
                    self.lb.destroy()
                self.lb_up = False

        else:
            words = self.comparison()

            if words:
                if not self.lb_up:

                    self.lb = Listbox(
                        height=len(words),
                        font=self.cget('font')
                    )
                    self.lb.bind('<Double-Button-1>', self.selection)
                    self.lb.bind('<Right>', self.selection)
                    self.lb.place(
                        x=self.winfo_x(),
                        y=self.winfo_y() + self.winfo_height()
                    )
                    self.lb_up = True

                self.lb.delete(0, END)
                for w in words:
                    self.lb.insert(END, w)
            else:
                if self.lb_up:
                    self.lb.destroy()
                    self.lb_up = False

    def selection(self, event):

        if self.lb_up:
            self.var.set(self.lb.get(ACTIVE))
            self.lb.destroy()
            self.lb_up = False
            self.icursor(END)

    def up(self, event):

        if self.lb_up:
            if self.lb.curselection() == ():
                index = '0'
            else:
                index = self.lb.curselection()[0]
            if index != '0':
                self.lb.selection_clear(first=index)
                index = str(int(index) - 1)
                self.lb.selection_set(first=index)
                self.lb.activate(index)

    def down(self, event):

        if self.lb_up:
            if self.lb.curselection() == ():
                index = '0'
            else:
                index = self.lb.curselection()[0]
            if index != END:
                self.lb.selection_clear(first=index)
                index = str(int(index) + 1)
                self.lb.selection_set(first=index)
                self.lb.activate(index)

    def comparison(self):
        pattern = re.compile('.*' + self.var.get() + '.*')
        return [w for w in self.list_qrbarcodes_db_values() if re.match(pattern, w)]
