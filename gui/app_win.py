"""GUI class definition for main window
"""

from tkinter import (
    BOTH, BOTTOM, CENTER, DoubleVar, DISABLED,
    HORIZONTAL, StringVar, SUNKEN, TOP, W, X, YES
)

from tkinter.ttk import Button, Entry, Frame, Label, LabelFrame, Panedwindow

from gui.app_def import get_app_definitions


class AppWin(Frame):

    def __init__(self, master=None, **kw):

        # Entry widget to collect
        # ID code used to identify
        # weight and humidity  of grain

        self.bar_qr_code = None

        # Pannel Window that contains
        # LabelFrames widgets for weight and humidity
        self.pw_wei_hum = None

        # LabelFrame widget that contains
        # Entry widget for weidght
        self.lblfrm_weight = None

        # Entry Widget to collect grain weight
        # from G810 machine
        self.ety_weight = None

        # DoubleVar variable to hold the weight value
        # between the Entry widget and to send to a database
        self.weight_portion = DoubleVar(master, value=0.0)

        # LabelFrame widget that contains
        # Entry widget for humidity
        self.lblfrm_hum = None

        # Entry Widget to collect grain humidity
        # from 3100 machine family
        self.ety_humidity = None

        # DoubleVar variable to hold the humidity value
        # between the Entry widget and to send to a database
        self.humidty_portion = DoubleVar(master, value=0.0)

        # variable hold the instance of button
        # that performs rading of grain weights
        self.btn_read_weight = None

        # variable hold the instance of button
        # that performs rading of grain humidity
        self.btn_read_humidity = None

        # variable hold the instance of button
        # that show info the current situation
        # of application execution
        self.stb_info = None

        # variable used to define the current
        # context of the application on a label
        # used as status bar
        self.app_status = StringVar()

        # root Tk
        self.master = master

        self.master.title(
            get_app_definitions('app_root_title')
        )

        Frame.__init__(self, master, **kw)

        self.add_title_app()

        self.add_ipt_id_code()

        self.add_weight_humidity_panel()

        self.add_reading_buttons()

        self.button_persist_data()

        self.status_bar_info()

        self.app_status.set('Application ready.')

    def add_title_app(self):
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

    def add_ipt_id_code(self):
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

        self.bar_qr_code = Entry(
            self,
            font='Courier 14 bold'
        )

        self.bar_qr_code.pack(fill=X)

        self.bar_qr_code.focus()

    def add_weight_humidity_panel(self):
        """define the main Pannel Widget

        :return: None
        """

        self.pw_wei_hum = Panedwindow(self, orient=HORIZONTAL)

        self.pw_wei_hum.pack()

        self.lblfrm_weight = LabelFrame(
            self.pw_wei_hum,
            text=get_app_definitions('labelframe_weight_caption')
        )

        self.pw_wei_hum.add(self.lblfrm_weight)

        self.ety_weight = Entry(
            self.lblfrm_weight,
            font='Courier 32 bold',
            justify=CENTER,
            width=6,
            textvariable=self.weight_portion
        )

        self.ety_weight.pack(padx=5, pady=5)

        self.ety_weight.config(state=DISABLED)

        self.lblfrm_hum = LabelFrame(
            self.pw_wei_hum,
            text=get_app_definitions('labelframe_humidity_caption')
        )

        self.pw_wei_hum.add(self.lblfrm_hum)

        self.ety_humidity = Entry(
            self.lblfrm_hum,
            font='Courier 32 bold',
            justify=CENTER,
            width=6,
            textvariable=self.humidty_portion
        )

        self.ety_humidity.pack(padx=5, pady=5)

        self.ety_humidity.config(state=DISABLED)

    def add_reading_buttons(self):
        """Buttons that trigger the data reading from the hardwares

        :return: None
        """

        self.btn_read_weight = Button(
            self.lblfrm_weight,
            text=get_app_definitions('read_grain_weight')
        )

        self.btn_read_weight.pack(fill=BOTH, expand=YES)

        self.btn_read_humidity = Button(
            self.lblfrm_hum,
            text=get_app_definitions('read_grain_humidity')
        )

        self.btn_read_humidity.pack(fill=BOTH, expand=YES)

    def button_persist_data(self):

        Button(
            self,
            text=get_app_definitions('button_text_save_data')
        ).pack(fill=X)

    def status_bar_info(self):

        self.stb_info = Label(
            self,
            borderwidth=1,
            relief=SUNKEN,
            anchor=W,
            textvariable=self.app_status
        )

        self.stb_info.pack(side=BOTTOM, fill=X)
