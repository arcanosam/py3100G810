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
        'labelframe_weight_caption': 'Weight:',
        'labelframe_humidity_caption': 'Humidity:',
        'read_grain_weight': 'Read weight',
        'read_grain_humidity': 'Read humidity',
        'button_text_save_data': 'Persist data'

    }[app_prop]
