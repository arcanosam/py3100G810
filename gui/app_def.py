"""Definitions for this application

    Titles, labels, edits
        colors foreground/background
    Default text labels etc
"""


def get_app_definitions(app_prop):

    return {
        'app_root_title': ' py3100G810 - Grains weight and humidity collector',
        'app_title_01': '   py3100G810 - Grains weight ',
        'app_title_02': '         and humidity collector',
        'app_title_bkgr': 'light blue',
        'app_title_frgr': 'dark green',
        'app_label_edit': 'ID code:',
        'app_lbledt_bkgr': 'white',
        'app_lbledt_frgr': 'green',
        'labelframe_db_values_caption': 'Database values found:',
        'label_db_weight': 'Weight: ',
        'label_db_humidi': 'Humidity: ',
        'labelframe_weight_caption': 'Weight:',
        'labelframe_humidity_caption': 'Humidity:',
        'btn_save_weight': 'Save weight',
        'btn_save_humidity': 'Save humidity',
        'ex_failure_01': 'Reading failure',
        'ex_failure_02': ''.join([
            'A failure was identified during reading from 3100 weighing indicators.\n',
            'Click in Yes to restart the data reading or No to quit this application.'
        ]),
        'LDAP_ENABLED': False,
        'lgn_fld_dflt_user': 'User',
        'lgn_fld_dflt_pwd': '     ',
        'lgn_dlg_close_title': 'Exit',
        'lgn_dlg_close_txt': 'Would like to finish the application?',
        'lgn_ldap_addr': 'ldap://',
        'lgn_ldap_dnbind': '',
        'lgn_dlg_wrn_title': 'Login Error',  # _wrn = warning
        'lgn_dlg_wrn_desc01': 'System Warning: Invalid password! ({0})',
        'lgn_dlg_wrn_desc02': 'System Warning: Blank password!({0})\n\nPlease fill in the field.',
        'lgn_dlg_wrn_desc03': 'System Warning: Blank user ({0})\n\nPlease fill in the field.',
        'lgn_frm_label_title': '               {0}\n       {1}'.format(
            'Authentication',
            'Login'
        ),
        'lgn_form_btn_caption': 'Login',
        'about_menu_config': 'Preferences',
        'about_menu_about': 'About...',
        'about_menu_exit': 'Exit',
        'about_win_btn': 'OK'

    }[app_prop]
