"""Definitions for this application

    Titles, labels, edits
        colors foreground/background
    Default text labels etc
"""

import configparser

# Load COM ports for each device from INI file
lang_ini = configparser.ConfigParser()

lang_ini.read('lang.ini')


def get_app_definitions(app_prop):

    app_definitions = {
        'app_root_title': {
            'en': ' py3100G810 - Grains weight and humidity collector',
            'ptBr': ' py3100G810 - Coletor de peso e umidade de graos'
        },
        'app_title_01': {
            'en': '   py3100G810 - Grains weight ',
            'ptBr': '   py3100G810 - Coletor de peso '
        },
        'app_title_02': {
            'en': '         and humidity collector',
            'ptBr': '            e umidade de graos'
        },
        'app_title_bkgr': {
            'en': 'light blue',
            'ptBr': 'light blue'
        },
        'app_title_frgr': {
            'en': 'dark green',
            'ptBr': 'dark green'
        },
        'app_label_edit': {
            'en': 'ID code:',
            'ptBr': 'Identificador:'
        },
        'app_lbledt_bkgr': {
            'en': 'white',
            'ptBr': 'white'
        },
        'app_lbledt_frgr': {
            'en': 'green',
            'ptBr': 'green'
        },
        'labelframe_db_values_caption': {
            'en': 'Database values found for this id above:',
            'ptBr': 'Valores encontrados no banco de dados para este identificador:'
        },
        'label_db_weight': {
            'en': 'Weight: ',
            'ptBr': 'Peso: '
        },
        'label_db_humidi': {
            'en': 'Humidity: ',
            'ptBr': 'Umidade: '
        },
        'labelframe_weight_caption': {
            'en': 'Weight:',
            'ptBr': 'Peso: '
        },
        'labelframe_humidity_caption': {
            'en': 'Humidity:',
            'ptBr': 'Umidade: '
        },
        'btn_save_weight': {
            'en': 'Save weight',
            'ptBr': 'Salvar peso'
        },
        'btn_save_humidity': {
            'en': 'Save humidity',
            'ptBr': 'Salvar umidade'
        },
        'ex_failure_01': {
            'en': 'Reading failure',
            'ptBr': 'Falha de leitura'
        },
        'ex_failure_02': {
            'en': ''.join([
                'A failure was identified during reading from 3100 weighing indicators.\n',
                'Click in Yes to restart the data reading or No to quit this application.'
            ]),
            'ptBr': ''.join([
                'Uma falha foi identificada durante a leitura da balanca.\n',
                'Clique em \'Sim\' para reiniciar a leitura de dados ou em \'Nao\'\n',
                ' para finalizar a aplicacao.'
            ])
        },
        'lgn_dlg_close_title': {
            'en': 'Exit',
            'ptBr': 'Sair'
        },
        'lgn_dlg_close_txt': {
            'en': 'Would like to finish the application?',
            'ptBr': 'Gostaria de encerrar a aplicacao?'
        },
        'title_menu': {
            'en': 'Options',
            'ptBr': 'Opcoes'
        },
        'menu_csv_export': {
            'en': 'Export all data',
            'ptBr': 'Exportar todos os dados'
        },
        'menu_about': {
            'en': 'About...',
            'ptBr': 'Sobre...'
        },
        'menu_exit': {
            'en': 'Exit',
            'ptBr': 'Sair'
        },
        'about_win_btn': {
            'en': 'OK',
            'ptBr': 'OK'
        },
        'title_id_code_404': {
            'en': 'Id not found!',
            'ptBr': 'Identificador nao encontrado'
        },
        'ask_id_code_to_save': {
            'en': 'Would you like to save as new ID?',
            'ptBr': 'Gostaria de salvar como novo identificador?'
        },
        'title_id_code_saved': {
            'en': 'New Code Id added',
            'ptBr': 'Novo identificador adicionado'
        },
        'msg_id_code_saved': {
            'en': 'The new code ID was inserted with successful',
            'ptBr': 'Novo identificador foi inserido com sucesso'
        },
        'db_failure_01': {
            'en': 'Database Error - Insert new code ID',
            'ptBr': 'Erro banco - Insercao de novo identificador'
        },
        'db_failure_02': {
            'en': 'Database Error - Search previous data',
            'ptBr': 'Erro banco - Pesquisando dados existentes'
        },
        'db_failure_03': {
            'en': 'Database Error - Update weight data',
            'ptBr': 'Erro banco - Atualizando valor do peso'
        },
        'db_failure_04': {
            'en': 'Database Error - Update humidity data',
            'ptBr': 'Erro banco - Atualizando valor da umidade'
        },
        'db_failure_05': {
            'en': 'Database Error - CSV exporting',
            'ptBr': 'Erro banco - Exportacao em CSV'
        },
        'db_failure_06': {
            'en': 'Database Error - Search ID exists',
            'ptBr': 'Erro banco - Pesquisando identificador no banco'
        },
        'db_failure_07': {
            'en': 'Database Error - Clean database',
            'ptBr': 'Erro banco - Limpeza do banco de dados'
        },
        'menu_db_clean': {
            'en': 'Clean database',
            'ptBr': 'Limpando banco de dados'
        },
        'dlg_tt_rec_save': {
            'en': 'Record updated!',
            'ptBr': 'Registro atualizado!'
        },
        'dlg_tt_weight_savemsg': {
            'en': 'The weigth value was persisted with successful',
            'ptBr': 'O valor do peso foi salvo com sucesso'
        },
        'dlg_reset_frm': {
            'en': 'Reset formulary',
            'ptBr': 'Limpar formulario'
        },
        'dlg_reset_msg': {
            'en': 'Do you want clean the formulary?',
            'ptBr': 'Deseja limpar o formulario?'
        },
        'dlg_tt_humid_savemsg': {
            'en': 'The humidity value was persisted with successful',
            'ptBr': 'O valor da umidade foi salvo com sucesso'
        },
        'dlg_tt_rec404': {
            'en': 'Record not found!',
            'ptBr': 'Registro nao encontrado'
        },
        'dlg_tt_rec404msg': {
            'en': 'There isn\'t no records select',
            'ptBr': 'Nao ha registros selecionados'
        },
        'dlg_csv_export_tt': {
            'en': 'CSV File name',
            'ptBr': 'Nome do arquivo CSV'
        },
        'dlg_csv_expOK_tt': {
            'en': 'Exported successful!',
            'ptBr': 'Exportacao efetuada com sucesso'
        },
        'dlg_csv_expOk_msg': {
            'en': 'All data was sucessfuly exported to csv file',
            'ptBr': 'Todos os dados foram exportados com sucesso para o arquivo CSV'
        },
        'dlg_clean_db_tt': {
            'en': 'Clean database',
            'ptBr': 'Limpeza de banco'
        },
        'dlg_clean_db_msg': {
            'en': 'Do you want clean the database?',
            'ptBr': 'Deseja remover TODOS os dado do banco?'
        },
        'dlg_csv_exp_can_tt': {
            'en': 'CSV Export',
            'ptBr': 'Exportarcao CSV'
        },
        'dlg_ope_can_msg': {
            'en': 'The operation was canceled',
            'ptBr': 'A operacao foi cancelada'
        },
        'dlg_backup_tt': {
            'en': 'Backup all data',
            'ptBr': 'Backup de todos os dados'
        },
        'dlg_backup_msg': {
            'en': 'Do you want make a backup of all data, before clean database?',
            'ptBr': 'Deseja fazer backup de todos os dados, antes da limpreza do banco de dados?'
        },
        'dlg_backupCan_tt': {
            'en': 'Backup canceled',
            'ptBr': 'Backup cancelado'
        },
        'dlg_backupCan_msg': {
            'en': ''.join([
                'You canceled the backup operation!\n\n',
                'For safety, the cleanup of database was cancelled too.\n\n'
                'Try again, but this time, you can choose',
                ' to not make a backup of all data.'
            ]),
            'ptBr': ''.join([
                'Voce cancelou esta operacao!\n\n',
                'Por precaucao, a limpeza do banco de dados sera cancelada.\n\n'
                'Tente novamente, mas desta vez escolha a opcao',
                ' de nao fazer o backup de todos os dados.'
            ])
        },
        'dlg_cleandbOk_tt': {
            'en': 'Clean Database',
            'ptBr': 'Limpeza do banco de dados'
        },
        'dlg_cleandbOk_msg': {
            'en': 'The database was reset for his default settings',
            'ptBr': 'O banco de dados foi restaurado em suas configuracoes originais.'
        }
    }

    value = app_definitions.get(app_prop)
    app_lang = lang_ini.get('lang', 'app-lang')

    if app_lang in value.keys():
        return value.get(app_lang)

    return value.get('en')
