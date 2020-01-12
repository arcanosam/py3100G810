"""GUI class definition for main window
"""

import configparser

import csv

import re

import sqlite3

import threading

from tkinter import (
    ACTIVE, BOTTOM, CENTER, DoubleVar, DISABLED,
    END, HORIZONTAL, Listbox, Menu, StringVar,
    SUNKEN, TOP, W, X, YES
)

from tkinter.ttk import Button, Entry, Frame, Label, LabelFrame, Menubutton, Panedwindow

from tkinter.messagebox import showerror, showinfo, askyesno

from tkinter.filedialog import asksaveasfilename

from serial import Serial
from serial.serialutil import SerialException

from gui.about_win import AboutWin

from gui.app_def import get_app_definitions

from dao.data_ids import DataIds


class AppWin(Frame):

    def __init__(self, master=None):

        # Declarations
        ###############

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

        # StringVar variable to hold the id code value
        # on the Entry widget
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

        # Class that implement persistance operations

        self._con_db_grains = DataIds(sqlite3.connect('grains.data'))

        # Id Code members to allow Entry Autocomplete Widget

        self._lb_auto_complete = None

        self._lb_auto_compl_after_id = None

        self._lb_auto_compl_is_up = False

        # Load COM ports for each device from INI file
        self._devices_ini = configparser.ConfigParser()

        self._devices_ini.read('devices.ini')

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

        self._con_db_grains.close_con()
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
        self._menubtn = Menubutton(self._master, text=get_app_definitions('title_menu'))

        # Menu creating
        self._pref_opts = Menu(self._menubtn, tearoff=False)

        # linking each other
        self._menubtn.config(menu=self._pref_opts)

        # adding options
        self._pref_opts.add_command(
            label=get_app_definitions('menu_csv_export'),
            command=self._save_exported_csv_file
        )

        self._pref_opts.add_separator()

        # adding options
        self._pref_opts.add_command(
            label=get_app_definitions('menu_db_clean'),
            command=self._clean_database
        )

        self._pref_opts.add_separator()

        self._pref_opts.add_command(
            label=get_app_definitions('menu_about'),
            command=self._show_sobre
        )

        self._pref_opts.add_command(
            label=get_app_definitions('menu_exit'),
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

        self._ety_qrbarcode = Entry(
            self,
            font='Courier 14 bold',
            textvariable=self._ety_qrbarcode_var
        )

        self._ety_qrbarcode.pack(fill=X)

        self._ety_qrbarcode.bind('<Escape>', self._lb_auto_compl_escape)
        self._ety_qrbarcode.bind('<Return>', self._lb_auto_compl_selection)
        self._ety_qrbarcode.bind('<Right>', self._lb_auto_compl_selection)
        self._ety_qrbarcode.bind('<Up>', self._lb_auto_compl_ev_up)
        self._ety_qrbarcode.bind('<Down>', self._lb_auto_compl_ev_down)
        self._ety_qrbarcode.bind('<Key>', self._lb_auto_compl_handle_wait)

        self._ety_qrbarcode.focus()

    def _lb_auto_compl_escape(self, event):

        if self._lb_auto_compl_is_up:
            self._lb_auto_complete.destroy()
            self._lb_auto_compl_is_up = False

    def _lb_auto_compl_selection(self, event):

        if self._lb_auto_compl_is_up:

            id_code_value = self._lb_auto_complete.get(ACTIVE)

            self._ety_qrbarcode_var.set(id_code_value[0])

            self.fill_with_previous_grain_data(id_code_value[0])

            self._lb_auto_complete.destroy()

            self._lb_auto_compl_is_up = False

            self._ety_qrbarcode.icursor(END)

    def _lb_auto_compl_ev_up(self, event):

        if self._lb_auto_compl_is_up:

            if self._lb_auto_complete.curselection() == ():
                index = '0'

            else:
                index = self._lb_auto_complete.curselection()[0]

            if index != '0':

                self._lb_auto_complete.selection_clear(first=index)

                index = str(int(index) - 1)

                self._lb_auto_complete.selection_set(first=index)
                self._lb_auto_complete.activate(index)

    def _lb_auto_compl_ev_down(self, event):

        if self._lb_auto_compl_is_up:

            if self._lb_auto_complete.curselection() == ():
                index = '0'

            else:
                index = self._lb_auto_complete.curselection()[0]

            if index != END:
                self._lb_auto_complete.selection_clear(first=index)

                index = str(int(index) + 1)

                self._lb_auto_complete.selection_set(first=index)
                self._lb_auto_complete.activate(index)

    def _lb_auto_compl_handle_wait(self, event):
        # cancel the old job
        if self._lb_auto_compl_after_id is not None:
            self.after_cancel(self._lb_auto_compl_after_id)

        self.fill_with_previous_grain_data(None)

        # create a new job
        self._lb_auto_compl_after_id = self.after(1000, self._lb_auto_compl_changed)

    def _lb_auto_compl_changed(self, name=None, index=None, mode=None):

        if self._ety_qrbarcode_var.get() == '':

            if hasattr(self, 'lb'):
                if self._lb_auto_complete:
                    self._lb_auto_complete.destroy()
                self._lb_auto_compl_is_up = False

        else:
            self._con_db_grains.clean_current_record()

            cmd_result = self._con_db_grains.search_grain_id_code(self._ety_qrbarcode_var.get())

            if cmd_result[0]:
                if not self._lb_auto_compl_is_up:

                    self._lb_auto_complete = Listbox(
                        height=len(cmd_result[1]),
                        font=self._ety_qrbarcode.cget('font')
                    )

                    self._lb_auto_complete.bind('<Double-Button-1>', self._lb_auto_compl_selection)

                    self._lb_auto_complete.bind('<Right>', self._lb_auto_compl_selection)

                    self._lb_auto_complete.place(
                        x=self._ety_qrbarcode.winfo_x()+2,
                        y=self._ety_qrbarcode.winfo_y() + self._ety_qrbarcode.winfo_height()*2
                    )

                    self._lb_auto_compl_is_up = True

                self._lb_auto_complete.delete(0, END)

                for id_found in cmd_result[1]:
                    self._lb_auto_complete.insert(END, id_found)

            elif cmd_result[1] is None:
                if self._lb_auto_compl_is_up:

                    self._lb_auto_complete.destroy()
                    self._lb_auto_compl_is_up = False

                    if askyesno(
                            get_app_definitions('title_id_code_404'),
                            get_app_definitions('ask_id_code_to_save')
                    ):
                        cmd_result = self._con_db_grains.insert_grain_id(self._ety_qrbarcode_var.get())

                        if cmd_result[0]:
                            showinfo(
                                get_app_definitions('title_id_code_saved'),
                                get_app_definitions('msg_id_code_saved')
                            )
                        else:
                            showinfo(
                                get_app_definitions('db_failure_01'),
                                cmd_result[1]
                            )
                else:
                    if askyesno(
                            get_app_definitions('title_id_code_404'),
                            get_app_definitions('ask_id_code_to_save')
                    ):
                        cmd_result = self._con_db_grains.insert_grain_id(self._ety_qrbarcode_var.get())

                        if cmd_result[0]:
                            showinfo(
                                get_app_definitions('title_id_code_saved'),
                                get_app_definitions('msg_id_code_saved')
                            )
                        else:
                            showinfo(
                                get_app_definitions('db_failure_01'),
                                cmd_result[1]
                            )
            else:
                showinfo(
                    get_app_definitions('db_failure_06'),
                    cmd_result[1]
                )

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
        )
        self._lbl_db_weight.grid(row=0, column=1)

        Label(
            self._lblfrm_db_values,
            font='size 13 bold',
            text=get_app_definitions('label_db_humidi')
        ).grid(row=1, column=0)

        self._lbl_db_humidity = Label(
            self._lblfrm_db_values,
            font='size 13 bold'
        )

        self._lbl_db_humidity.grid(row=1, column=1)

    def fill_with_previous_grain_data(self, id_code_value):

        weight_humidity_values = ('', '',)

        if id_code_value is not None:
            cmd_result = self._con_db_grains.search_grain_data(id_code_value)

            if cmd_result[0]:
                weight_humidity_values = cmd_result[1]
            else:
                showinfo(
                    get_app_definitions('db_failure_02'),
                    cmd_result[1]
                )
        else:
            self._con_db_grains.clean_current_record()

        self._lbl_db_weight.config(
            text=weight_humidity_values[0]  # weight
        )

        self._lbl_db_humidity.config(
            text=weight_humidity_values[1]  # humidity
        )

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
            command=self._save_weight_portion
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

        if not self._ind3100.is_open:
            try:

                # apply serial config
                self._ind3100.baudrate = 19200
                self._ind3100.port = self._devices_ini.get('3100').get('comPort')
                self._ind3100.open()

                # start thread
                self._thr_read_weight_serial.start()

            except SerialException as e:
                self._ind3100.close()

        if not self._g810.is_open:
            try:

                # apply serial config
                self._g810.baudrate = 4800
                self._g810.port = self._devices_ini.get('g810').get('comPort')

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

    def _save_weight_portion(self):

        if self._con_db_grains.get_current_record_id() is not None:

            import random
            cmd_result = self._con_db_grains.update_weigth_humidity_value(self.weight_portion+random.random())

            if cmd_result[0]:
                showinfo(
                    get_app_definitions('dlg_tt_rec_save'),
                    get_app_definitions('dlg_tt_weight_savemsg')
                )
            else:
                showinfo(
                    get_app_definitions('db_failure_03'),
                    cmd_result[1]
                )

            if askyesno(
                get_app_definitions('dlg_reset_frm'),
                get_app_definitions('dlg_reset_msg')
            ):
                self._ety_qrbarcode_var.set('')
                self.fill_with_previous_grain_data(None)
        else:
            showerror(
                get_app_definitions('dlg_tt_rec404'),
                get_app_definitions('dlg_tt_rec404msg')
            )

    def _save_humidity_portion(self):

        if self._con_db_grains.get_current_record_id() is not None:

            import random
            cmd_result = self._con_db_grains.update_weigth_humidity_value(self.humidity_portion+random.random(), False)

            if cmd_result[0]:
                showinfo(
                    get_app_definitions('dlg_tt_rec_save'),
                    get_app_definitions('dlg_tt_humid_savemsg')
                )
            else:
                showinfo(
                    get_app_definitions('db_failure_04'),
                    cmd_result[1]
                )

            if askyesno(
                    get_app_definitions('dlg_reset_frm'),
                    get_app_definitions('dlg_reset_msg')
            ):
                self._ety_qrbarcode_var.set('')
                self.fill_with_previous_grain_data(None)
        else:
            showerror(
                get_app_definitions('dlg_tt_rec404'),
                get_app_definitions('dlg_tt_rec404msg')
            )

    def _save_exported_csv_file(self, backup=None):

        csv_file_name = asksaveasfilename(
            title=get_app_definitions('dlg_csv_export_tt'),
            filetypes=(('csv files', '*.csv'),)
        )

        if len(csv_file_name):

            cmd_result = self._con_db_grains.get_all_grains()

            if cmd_result[0]:
                # Table headers.
                headers = ['code', 'weight', 'humidity', 'record date', 'update date']

                # Open CSV file for writing.
                with open(csv_file_name, 'w', newline='') as csv_file_handle:
                    csv_file_pointer = csv.writer(csv_file_handle)

                    # Add the headers and data to the CSV file.
                    csv_file_pointer.writerow(headers)
                    csv_file_pointer.writerows(cmd_result[1])

                showinfo(
                    get_app_definitions('dlg_csv_expOK_tt'),
                    get_app_definitions('dlg_csv_expOk_msg')
                )
            else:
                showinfo(
                    get_app_definitions('db_failure_05'),
                    cmd_result[1]
                )
        else:
            if backup is None:
                showinfo(
                    get_app_definitions('dlg_csv_exp_can_tt'),
                    get_app_definitions('dlg_ope_can_msg')
                )
            else:
                showinfo(
                    get_app_definitions('dlg_backupCan_tt'),
                    get_app_definitions('dlg_backupCan_msg')
                )

    def _clean_database(self):

        if askyesno(
            get_app_definitions('dlg_clean_db_tt'),
            get_app_definitions('dlg_clean_db_msg')
        ):
            if askyesno(
                get_app_definitions('dlg_backup_tt'),
                get_app_definitions('dlg_backup_msg')
            ):
                self._save_exported_csv_file(True)

                cmd_result = self._con_db_grains.rebuild_db()

                if cmd_result[0]:
                    showinfo(
                        get_app_definitions('dlg_cleandbOk_tt'),
                        get_app_definitions('dlg_cleandbOk_msg')
                    )
                else:
                    showinfo(
                        get_app_definitions('db_failure_07'),
                        cmd_result[1]
                    )
            else:
                cmd_result = self._con_db_grains.rebuild_db()

                if cmd_result[0]:
                    showinfo(
                        get_app_definitions('dlg_cleandbOk_tt'),
                        get_app_definitions('dlg_cleandbOk_msg')
                    )
                else:
                    showinfo(
                        get_app_definitions('db_failure_07'),
                        cmd_result[1]
                    )

        else:
            showinfo(
                get_app_definitions('menu_db_clean'),
                get_app_definitions('dlg_ope_can_msg')
            )