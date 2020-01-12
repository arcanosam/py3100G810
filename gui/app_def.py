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
        'db_failure_06': 'Database Error - Search ID exists',
        'db_failure_07': 'Database Error - Clean database',
        'menu_db_clean': 'Clean database',
        'dlg_tt_rec_save': 'Record updated!',
        'dlg_tt_weight_savemsg': 'The weigth value was persisted with successful',
        'dlg_reset_frm': 'Reset formulary',
        'dlg_reset_msg': 'Do you want clean the formulary?',
        'dlg_tt_humid_savemsg': 'The humidity value was persisted with successful',
        'dlg_tt_rec404': 'Record not found!',
        'dlg_tt_rec404msg': 'There isn\'t no records select',
        'dlg_csv_export_tt': 'CSV File name',
        'dlg_csv_expOK_tt': 'Exported successful!',
        'dlg_csv_expOk_msg': 'All data was sucessfuly exported to csv file',
        'dlg_clean_db_tt': 'Clean database',
        'dlg_clean_db_msg': 'Do you want clean the database?',
        'dlg_csv_exp_can_tt': 'CSV Export',
        'dlg_ope_can_msg': 'The operation was canceled',
        'dlg_backup_tt': 'Backup all data',
        'dlg_backup_msg': 'Do you want make a backup of all data, before clean database?',
        'dlg_backupCan_tt': 'Backup canceled',
        'dlg_backupCan_msg': ''.join([
            'You canceled the backup operation!\n\n',
            'For safety, the cleanup of database was cancelled too.\n\n'
            'Try again, but this time, you can choose',
            ' to not make a backup of all data.'
        ]),
        'dlg_cleandbOk_tt': 'Clean Database',
        'dlg_cleandbOk_msg': 'The database was reset for his default settings'

    }[app_prop]
