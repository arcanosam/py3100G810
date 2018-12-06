"""GUI class definition for main window
"""

import re

import threading

from tkinter import (
    CENTER, DoubleVar, DISABLED, HORIZONTAL,
    StringVar, TOP, W, X, YES
)

from tkinter.ttk import Button, Entry, Frame, Label, LabelFrame, Panedwindow

from tkinter.messagebox import askyesno, showinfo

from serial import Serial
from serial.serialutil import SerialException

from gui.app_def import get_app_definitions


class AppWin(Frame):

    def __init__(self, master=None, **kw):

        # Declarations
        ###############

        # Entry widget to collect
        # ID code used to identify
        # weight and humidity  of grain
        self._ety_qrbarcode = None

        # Variable to get the ide code of
        # Entry wiget, that will identify
        # the grain portion
        self._ety_qrbarcode_var = StringVar()

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

        self._thread_is_running = True

        self._thr_read_weight_serial = threading.Thread(target=self._collecting_loop)
        self._thr_read_weight_serial.setDaemon(True)

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

        Frame.__init__(self, master, **kw)

        self._add_title_app()

        self._add_ipt_id_code()

        self._add_database_values_panel()

        self._add_weight_humidity_panel()

        # Final app sets
        #################

        self._master.after(500, self._conn_serials)

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

        self._thread_is_running = False

        if self._ind3100:
            self._ind3100.cancel_read()
            self._ind3100.close()

        self._master.destroy()

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

        self._ety_qrbarcode = Entry(
            self,
            font='Courier 14 bold',
            textvariable=self._ety_qrbarcode_var
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

    def _conn_serials(self):
        """connect to 3100 indicator and G810 by their respectively serials

        :return: None
        """

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

    def _collecting_loop(self):
        """loop to always capture the new data from both hardwares

        :return: None
        """

        while self._thread_is_running:

            if self._ind3100.is_open:

                try:
                    serial_data = str(self._ind3100.readline())
                except SerialException as e:
                    self._thread_is_running = False
                    self.master.after(2000, self._dlg_restart_collect)
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

    def _dlg_restart_collect(self):

        if askyesno(
                get_app_definitions('ex_failure_01'),
                get_app_definitions('ex_failure_02')
        ):

            self._thread_is_running = True
        else:
            self._close_app()

    def _save_weight_portion(self):

        showinfo('Saving...', 'Persisting weight...')
        # TODO
        # test if has a valid id code
        # connect with database
        # persist

    def _save_humidity_portion(self):

        showinfo('Saving...', 'Persisting humidity...')
        # TODO
        # test if has a valid id code
        # connect with database
        # persist
