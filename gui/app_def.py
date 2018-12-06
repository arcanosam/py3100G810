"""Definitions for this application

    Titles, labels, edits
        colors foreground/background
    Default text labels etc
"""


def get_app_definitions(app_prop):

    return {
        'app_root_title': ' py3100G810 - Grains weight and humidity collector',
        'app_title_01': '   py3100G810 - Grains weight and  ',
        'app_title_02': '              humidity collector',
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
        ])

    }[app_prop]
