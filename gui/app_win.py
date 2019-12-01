"""GUI class definition for main window
"""

from datetime import datetime, timedelta

import re

import sqlite3

import threading

from tkinter import (
    BOTTOM, CENTER, DoubleVar, DISABLED, HORIZONTAL,
    Menu, StringVar, SUNKEN, TOP, W, X, YES
)

from tkinter.ttk import Button, Entry, Frame, Label, LabelFrame, Menubutton, Panedwindow

from tkinter.messagebox import showerror, showinfo

from serial import Serial
from serial.serialutil import SerialException

from gui.about_win import AboutWin

from gui.autocomplete_entry import AutocompleteEntry

from gui.app_def import get_app_definitions


class AppWin(Frame):

    def __init__(self, master=None):

        # Declarations
        ###############

        self.LIMIT_ACESS = 60 * 5

        # variable used to hold control time of acess
        # of this app
        self.done_time = None

        # variable hold the top level instance
        # to login auth window
        self._frm_login = None

        # User login variable

        self._user_login = None

        # variable hold the session/user info
        self._lbl_info = None

        # Main Menu variable

        self._menubtn = None

        # Menu creating
        self._pref_opts = None

        # Entry widget to collect
        # ID code used to identify
        # weight and humidity  of grain
        self._ety_qrbarcode = None

        # Pannel Window that contains
        # LabelFrames widgets for weight and humidity
        # founded in database
        self._pw_db_values = None

        # LabelFrame widget that contains
        # Labels filled with values of weidght
        # and humidity recovered from database
        self._lblfrm_db_values = None

        # Label holds the value of weight recovered
        # from database
        self._lbl_db_weight = None

        # Label holds the value of humidity recovered
        # from database
        self._lbl_db_humidity = None

        # Pannel Window that contains
        # LabelFrames widgets for weight and humidity
        self._pw_wei_hum = None

        # LabelFrame widget that contains
        # Entry widget for weidght
        self._lblfrm_weight = None

        # Entry Widget to collect grain weight
        # from G810 machine
        self._ety_weight = None

        # DoubleVar variable to hold the weight value
        # between the Entry widget and to send to a database
        self._ety_weight_portion_var = DoubleVar(master, value=0.0)

        # LabelFrame widget that contains
        # Entry widget for humidity
        self._lblfrm_hum = None

        # Entry Widget to collect grain humidity
        # from 3100 machine family
        self._ety_humidity = None

        # DoubleVar variable to hold the humidity value
        # between the Entry widget and to send to a database
        self._ety_humidity_portion_var = DoubleVar(master, value=0.0)

        # variable used to hold Serial instance
        # for 3100 indicator
        self._ind3100 = Serial()

        # Define a thread used after
        # open the serial to collect the
        # data and prevent the freeze of
        # application when the hardware is off

        self._thread_weight_is_running = True

        self._thr_read_weight_serial = threading.Thread(target=self._weight_collect_loop)
        self._thr_read_weight_serial.setDaemon(True)

        # variable used to hold Serial instance
        # for g810 humidity measurer
        self._g810 = Serial()

        # Define a thread used after
        # open the serial to collect the
        # data and prevent the freeze of
        # application when the hardware is off

        self._thread_hum_is_running = True

        self._thr_read_hum_serial = threading.Thread(target=self._hum_collect_loop)
        self._thr_read_hum_serial.setDaemon(True)

        self._con_db_grains = sqlite3.connect('grains.data')

        # GUI section
        ###############

        # root Tk
        self._master = master

        # set the title bar of the app
        self._master.title(
            get_app_definitions('app_root_title')
        )

        # Prevent the app closing before
        # undone some necessary process
        self._master.protocol("WM_DELETE_WINDOW", self._close_app)

        Frame.__init__(self, master)

        self._add_title_app()

        self._build_menu()

        self._add_ipt_id_code()

        self._add_database_values_panel()

        self._add_weight_humidity_panel()

        self._status_info()


    # properties
    #############

    # 3100 Weight property

    @property
    def weight_portion(self):
        return self._ety_weight_portion_var.get()

    @weight_portion.setter
    def weight_portion(self, value):
        self._ety_weight_portion_var.set(value)

    # G810 humidity property

    @property
    def humidity_portion(self):
        return self._ety_humidity_portion_var.get()

    @humidity_portion.setter
    def humidity_portion(self, value):
        self._ety_humidity_portion_var.set(value)

    def _close_app(self):
        """some processes be undone before the system tkinter deletion/destroy

        :return: None
        """

        self._con_db_grains.close()
        self._thread_weight_is_running = False
        self._thread_hum_is_running = False

        if self._ind3100:
            self._ind3100.cancel_read()
            self._ind3100.close()

        if self._g810:
            self._g810.cancel_read()
            self._g810.close()

        self._master.destroy()

    def _show_sobre(self):

        AboutWin(self._master)

    def _build_menu(self):

        # Main Menu
        self._menubtn = Menubutton(self._master, text=get_app_definitions('about_menu_config'))

        # Menu creating
        self._pref_opts = Menu(self._menubtn, tearoff=False)

        # linking each other
        self._menubtn.config(menu=self._pref_opts)

        # adding options
        self._pref_opts.add_command(
            label=get_app_definitions('about_menu_about'),
            command=self._show_sobre
        )

        self._pref_opts.add_command(
            label=get_app_definitions('about_menu_exit'),
            command=self._close_app
        )

        # align left
        self._menubtn.pack(anchor=W, fill=X)

    def _add_title_app(self):
        """define the Title application Label

        :return: None
        """

        Label(
            self,
            font='size 16 bold',
            text='{0}\n{1}'.format(
                get_app_definitions('app_title_01'),
                get_app_definitions('app_title_02')
            ),
            background=get_app_definitions('app_title_bkgr'),
            foreground=get_app_definitions('app_title_frgr')
        ).pack(
            fill=X,
            expand=YES,
            anchor=CENTER
        )

    def _add_ipt_id_code(self):
        """define the id code input widget

        :return:None
        """

        Label(
            self,
            font='size 13 bold',
            text=get_app_definitions('app_label_edit'),
            background=get_app_definitions('app_lbledt_bkgr'),
            foreground=get_app_definitions('app_lbledt_frgr')
        ).pack(
            anchor=W,
            side=TOP,
            fill=X
        )

        self._ety_qrbarcode = AutocompleteEntry(
            None,
            self,
            font='Courier 14 bold'
        )

        self._ety_qrbarcode.pack(fill=X)

        self._ety_qrbarcode.focus()

    def _add_database_values_panel(self):

        self._pw_db_values = Panedwindow(self, orient=HORIZONTAL)

        self._pw_db_values.pack(fill=X, expand=True)

        self._lblfrm_db_values = LabelFrame(
            self._pw_wei_hum,
            text=get_app_definitions('labelframe_db_values_caption')
        )

        self._pw_db_values.add(self._lblfrm_db_values)

        Label(
            self._lblfrm_db_values,
            font='size 13 bold',
            text=get_app_definitions('label_db_weight')
        ).grid(row=0, column=0, sticky=W)

        self._lbl_db_weight = Label(
            self._lblfrm_db_values,
            font='size 13 bold'
        ).grid(row=0, column=1)

        Label(
            self._lblfrm_db_values,
            font='size 13 bold',
            text=get_app_definitions('label_db_humidi')
        ).grid(row=1, column=0)

        self._lbl_db_humidity = Label(
            self._lblfrm_db_values,
            font='size 13 bold'
        ).grid(row=1, column=1)

    def _add_weight_humidity_panel(self):
        """define the main Pannel Widget

        :return: None
        """

        self._pw_wei_hum = Panedwindow(self, orient=HORIZONTAL)

        self._pw_wei_hum.pack()

        self._lblfrm_weight = LabelFrame(
            self._pw_wei_hum,
            text=get_app_definitions('labelframe_weight_caption')
        )

        self._pw_wei_hum.add(self._lblfrm_weight)

        self._ety_weight = Entry(
            self._lblfrm_weight,
            font='Courier 32 bold',
            justify=CENTER,
            width=6,
            textvariable=self._ety_weight_portion_var
        )

        self._ety_weight.pack(padx=5, pady=5)

        self._ety_weight.config(state=DISABLED)

        Button(
            self._lblfrm_weight,
            text=get_app_definitions('btn_save_weight'),
            command = self._save_weight_portion
        ).pack(fill=X)

        self._lblfrm_hum = LabelFrame(
            self._pw_wei_hum,
            text=get_app_definitions('labelframe_humidity_caption')
        )

        self._pw_wei_hum.add(self._lblfrm_hum)

        self._ety_humidity = Entry(
            self._lblfrm_hum,
            font='Courier 32 bold',
            justify=CENTER,
            width=6,
            textvariable=self._ety_humidity_portion_var
        )

        self._ety_humidity.pack(padx=5, pady=5)

        self._ety_humidity.config(state=DISABLED)

        Button(
            self._lblfrm_hum,
            text=get_app_definitions('btn_save_humidity'),
            command=self._save_humidity_portion
        ).pack(fill=X)

    def _status_info(self):

        self._lbl_info = Label(
            self,
            text='\n',
            borderwidth=1,
            relief=SUNKEN,
            anchor=W,
            font="Courier 10 bold"
        )

        self._lbl_info.pack(side=BOTTOM, fill=X)

    def _conn_serials(self):
        """connect to 3100 indicator and G810 by their respectively serials

        :return: None
        """

        self._start_session()

        if not self._ind3100.is_open:
            try:

                # apply serial config
                self._ind3100.baudrate = 19200
                self._ind3100.port = 'COM10'
                self._ind3100.open()

                # start thread
                self._thr_read_weight_serial.start()

            except SerialException as e:
                self._ind3100.close()

        if not self._g810.is_open:
            try:

                # apply serial config
                self._g810.baudrate = 4800
                self._g810.port = '/dev/ttyS0'

                self._g810.rts = None
                self._g810.dtr = None

                self._g810.open()

                # start thread
                self._thr_read_hum_serial.start()

            except SerialException as e:
                self._g810.close()

    def _weight_collect_loop(self):
        """loop to always capture the new data from 3100 hardware

        :return: None
        """

        while self._thread_weight_is_running:

            if self._ind3100.is_open:

                try:
                    serial_data = str(self._ind3100.readline())
                except SerialException as e:
                    self._thread_weight_is_running = False
                    self.master.after(2000, self._dlg_error_system)
                    continue

                values_found = re.findall(
                    '(-?\d+,\d+)',
                    serial_data
                )

                if len(values_found) > 0:
                    weight_read = float(values_found[0].replace(',', '.'))
                    self.weight_portion = weight_read
                else:
                    self.weight_portion = 0.

    def _hum_collect_loop(self):
        """loop to always capture the new data from g810 hardware

        :return: None
        """

        while self._thread_hum_is_running:

            if self._g810.is_open:

                try:
                    serial_data = str(self._g810.readline())
                except SerialException as e:
                    self._thread_hum_is_running = False
                    self.master.after(2000, self._dlg_error_system)

                values_found = serial_data.split(';')

                if len(values_found) > 1:
                    values_found = float(values_found[1])
                    if values_found > 0.:
                        hum_read = values_found
                        self.humidity_portion = hum_read
                    else:
                        self.humidity_portion = 0.

    def _dlg_error_system(self):

        showerror(
                get_app_definitions('ex_failure_01'),
                get_app_definitions('ex_failure_02')
        )

        self._close_app()

    def _start_session(self):

        self.done_time = datetime.now() + timedelta(seconds=self.LIMIT_ACESS)

    def _save_weight_portion(self):

        showinfo('Saving...', 'Persisting weight - {0}'.format(self._ety_qrbarcode.get()))
        # TODO 2019-11-16
        # insert records for tests
        # create method list_qrbarcodes_db_values to get the id of qrbarcodes
        # test the autocomplete entry
        # go on to persist data

    def _save_humidity_portion(self):

        showinfo('Saving...', 'Persisting humidity...')
        # TODO
        # test if has a valid id code
        # connect with database
        # persist

    def get_tk_root(self):

        return self._master

    def set_logged_user(self, login_name):

        self._user_login = login_name