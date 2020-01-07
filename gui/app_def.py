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
        'labelframe_db_values_caption': 'Database values found for this id above:',
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
        'lgn_dlg_close_title': 'Exit',
        'lgn_dlg_close_txt': 'Would like to finish the application?',
        'title_menu': 'Options',
        'menu_csv_export': 'Export all data',
        'menu_about': 'About...',
        'menu_exit': 'Exit',
        'about_win_btn': 'OK',
        'title_id_code_404': 'Id not found!',
        'ask_id_code_to_save': 'Would you like to save as new ID?',
        'title_id_code_saved': 'New Code Id added',
        'msg_id_code_saved': 'The new code ID was inserted with successful',
        'db_failure_01': 'Database Error - Insert new code ID',
        'db_failure_02': 'Database Error - Search previous data',
        'db_failure_03': 'Database Error - Update weight data',
        'db_failure_04': 'Database Error - Update humidity data',
        'db_failure_05': 'Database Error - CSV exporting',
        'db_failure_06': 'Database Error - Search ID exists'
    }[app_prop]
