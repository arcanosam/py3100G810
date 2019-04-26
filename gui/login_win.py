""" Python Tkinter Login/Pass Window

    Author: Kyle Kowalczyk
    Description: Username and password entry box
    Python Interpreter: v2.7.13
    Original Source: https://smallguysit.com/index.php/2017/03/13/python-tkinter-password-entry-box/

    #TODO
    - Should edit to integrate with an auth source

"""

from tkinter import BOTH, END, S, Toplevel, YES
from tkinter.ttk import Button, Entry, Label
from tkinter.messagebox import askyesno, showwarning

import ldap

from gui.app_def import get_app_definitions


class LoginWin(Toplevel):

    def __init__(self, master=None):

        self.ety_username = None

        self.ety_password = None

        self.btn_login = None

        # root Tk
        self._parent = master

        Toplevel.__init__(self, master)

        self.w = 381
        self.h = 347

        ws = self._parent.get_tk_root().winfo_screenwidth()
        hs = self._parent.get_tk_root().winfo_screenheight()

        # center window
        self.geometry(
            '%dx%d+%d+%d' % (
                self.w,
                self.h,
                (ws / 2) - (self.w / 2),
                (hs / 2) - (self.h / 2)
            )
        )

        self.resizable(width=False, height=False)

        self.transient(master)

        self.focus_force()  # added
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self._must_login)

        self.bind("<Configure>", self._move_me)

        self._add_title_login()

        self._wgt_username()

        self._wgt_password()

        self._btn_login()

        self._parent.after(1000, self.ety_username.focus)

        self.wait_window(self)

    def _clear_widget(self, event):
        """
            will clear out any entry boxes defined below when the user shifts
            focus to the widgets defined below
        :param event:
        :return:
        """

        if self.ety_username == self.focus_get() and \
                self.ety_username.get() == get_app_definitions('lgn_fld_dflt_user'):
            self.ety_username.delete(0, END)

        elif self.ety_password == self.ety_password.focus_get() and \
                self.ety_password.get() == get_app_definitions('lgn_fld_dflt_pwd'):
            self.ety_password.delete(0, END)

    def _repopulate_defaults(self, event):
        """
            will repopulate the default text previously inside the entry boxes defined below if
            the user does not put anything in while focused and changes focus to another widget
        :param event:
        :return:
        """

        if self.ety_username != self.focus_get() and self.ety_username.get() == '':
            self.ety_username.insert(0, get_app_definitions('lgn_fld_dflt_user'))

        elif self.ety_password != self.focus_get() and self.ety_password.get() == '':
            self.ety_password.insert(0, get_app_definitions('lgn_fld_dflt_pwd'))

    def _must_login(self):

        if askyesno(
            get_app_definitions('lgn_dlg_close_title'),
            get_app_definitions('lgn_dlg_close_txt')
        ):
            self._parent.get_tk_root().destroy()

    def _do_login(self, *event):
        """
            Able to be called from a key binding or a button click because of the '*event'
        :param event:
        :return:
        """

        if get_app_definitions('LDAP_ENABLED'):
            self._ldap_auth()
        else:
            self._parent.set_logged_user('anon')

            self.destroy()

    def _ldap_auth(self):

        con = ldap.initialize(
            get_app_definitions('lgn_ldap_addr'),
            bytes_mode=False
        )

        try:
            con.simple_bind_s(
                get_app_definitions('lgn_ldap_dnbind').format(
                    self.ety_username.get()
                ),
                self.ety_password.get()
            )

            self._parent.set_logged_user(self.ety_username.get())

            self.destroy()

        except ldap.INVALID_CREDENTIALS as exc:

            self.ety_username.unbind('<FocusOut>')
            self.ety_password.unbind('<FocusOut>')

            showwarning(
                get_app_definitions('lgn_dlg_wrn_title'),
                get_app_definitions('lgn_dlg_wrn_desc01').format(
                    exc.args[0]['desc']
                )
            )

            self.ety_password.bind('<FocusOut>', self._repopulate_defaults)
            self.ety_username.bind('<FocusOut>', self._repopulate_defaults)

        except ldap.UNWILLING_TO_PERFORM as exc:

            self.ety_password.unbind('<FocusOut>')

            showwarning(
                get_app_definitions('lgn_dlg_wrn_title'),
                get_app_definitions('lgn_dlg_wrn_desc02').format(
                    exc.args[0]['desc']
                )
            )

            self.ety_password.bind('<FocusOut>', self._repopulate_defaults)

        except ldap.INVALID_DN_SYNTAX as exc:

            self.ety_username.unbind('<FocusOut>')

            showwarning(
                get_app_definitions('lgn_dlg_wrn_title'),
                get_app_definitions('lgn_dlg_wrn_desc03').format(
                    exc.args[0]['desc']
                )
            )

            self.ety_username.bind('<FocusOut>', self._repopulate_defaults)

    def _move_me(self, event):

        ws = self._parent.get_tk_root().winfo_screenwidth()
        hs = self._parent.get_tk_root().winfo_screenheight()

        self.geometry(
            '%dx%d+%d+%d' % (
                self.w,
                self.h,
                (ws / 2) - (self.w / 2),
                (hs / 2) - (self.h / 2)
            )
        )

    def _add_title_login(self):
        """define the Title login Label

        :return: None
        """

        Label(
            self,
            font='size 16 bold',
            text=get_app_definitions('lgn_frm_label_title'),
            background='dark blue',
            foreground='green'
        ).pack(
            fill=BOTH,
            expand=YES,
            anchor=S
        )

    def _wgt_username(self):

        self.ety_username = Entry(self)

        self.ety_username.insert(0, get_app_definitions('lgn_fld_dflt_user'))

        self.ety_username.bind('<FocusIn>', self._clear_widget)

        self.ety_username.bind('<FocusOut>', self._repopulate_defaults)

        self.ety_username.pack()

    def _wgt_password(self):

        self.ety_password = Entry(self, show='*')

        self.ety_password.insert(0, get_app_definitions('lgn_fld_dflt_pwd'))

        self.ety_password.bind('<FocusIn>', self._clear_widget)

        self.ety_password.bind('<FocusOut>', self._repopulate_defaults)

        self.ety_password.bind('<Return>', self._do_login)

        self.ety_password.pack()

    def _btn_login(self):

        self.btn_login = Button(
            self,
            text=get_app_definitions('lgn_form_btn_caption'),
            command=self._do_login
        )

        self.btn_login.bind('<Return>', self._do_login)

        self.btn_login.pack()
