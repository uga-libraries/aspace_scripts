import PySimpleGUI as psg
import threading
import gc
import json
import sys

from secrets import *
from openpyxl import load_workbook
from asnake.aspace import ASpace
from asnake.client import ASnakeClient

# digobj_file = "data/ms4401 do.xlsx"
# dotemp_file = "data/bulk_import_DO_template.xlsx"


WRITE_DOS_THREAD = '-DOS_THREAD-'
DOSWRITE_PROGRESS_THREAD = '-WRITE_PROGRESS-'
# aspace = ASpace(baseurl=as_api, username=as_un, password=as_pw)
# client = ASnakeClient(baseurl=as_api, username=as_un, password=as_pw)
# client.authorize()


def gui():
    gc.disable()
    defaults = psg.UserSettings()
    close_program, client = get_aspace_log(defaults)
    if close_program is True:
        sys.exit()
    main_layout = [[psg.FileBrowse(' Select Digital Objects File ', file_types=(("Excel Files", "*.xlsx"),),
                                   target=defaults['_DO_FILE_']),
                    psg.InputText(default_text=defaults['_DO_FILE_'], key='_DO_FILE_')],  # TODO: Expand to CSVs
                   [psg.FileBrowse(' Select Template ', file_types=(("Excel Files", "*.xlsx"),),
                                   target=defaults['_DOTEMP_FILE_']),
                    psg.InputText(default_text=defaults['_DOTEMP_FILE_'], key='_DOTEMP_FILE_')],  # TODO: Expand to CSVs
                   [psg.Button(' Start ', key='_WRITE_DOS_', disabled=False)],
                   [psg.Output(size=(80, 18), key="_output_")]]
    window = psg.Window('Write Digital Objects to Template', layout=main_layout)
    while True:
        gc.collect()
        event, values = window.read()
        if event == psg.WINDOW_CLOSED or event == 'Exit':
            break
        if event == '_WRITE_DOS_':
            if not values['_DO_FILE_']:
                psg.popup('Please select a digital objects file')
            elif not values['_DOTEMP_FILE_']:
                psg.popup('Please select a digital object template')
            else:
                defaults['_DO_FILE_'] = values['_DO_FILE_']
                defaults['_DOTEMP_FILE_'] = values['_DOTEMP_FILE_']
                dos_thread = threading.Thread(target=write_digobjs, args=(values['_DO_FILE_'], values['_DOTEMP_FILE_'],
                                                                          client))
                window[f'{"_WRITE_DOS_"}'].update(disabled=True)
                dos_thread.start()
        if event == WRITE_DOS_THREAD:
            window[f'{"_WRITE_DOS_"}'].update(disabled=False)


def write_digobjs(digobj_file, dotemp_file, client):
    digobj_wb = load_workbook(digobj_file)
    digobj_sheet = digobj_wb.active
    dotemp_wb = load_workbook(dotemp_file)
    dotemp_sheet = dotemp_wb.active
    columns = [4, 6, 7, 8, 9, 10]
    write_row_index = 6
    for row in digobj_sheet.iter_rows(min_row=2, values_only=True):
        digobj_id = row[0]
        digobj_title = row[2]
        digobj_url = row[3]
        digobj_date = row[5]
        digobj_publish = row[8]
        search_archobjs = client.get_paged(f"/repositories/{4}/search",
                                           params={"q": f'title:"{digobj_title}, {digobj_date}"',
                                                   "type": ['archival_object']})
        search_results = []
        for results in search_archobjs:
            search_results.append(results)
        if len(search_results) > 1:  # TODO: elegant way for user to select which option from multiple found objects
            print(f'{digobj_title}, {digobj_date}')
            for result in search_results:
                print(result)
        else:
            for result in search_results:
                uri = result["uri"]
                resource_uri = result["resource"]
        column_map = {4: resource_uri, 6: uri, 7: digobj_id, 8: digobj_title, 9: digobj_publish, 10: digobj_url}
        for column in columns:
            dotemp_sheet.cell(row=write_row_index, column=column).value = column_map[column]
        write_row_index += 1
        print(column_map)
        dotemp_wb.save(dotemp_file)
    digobj_wb.close()
    dotemp_wb.close()


def get_aspace_log(defaults, as_un=None, as_pw=None, as_ap=None, as_client=None):
    """
    Gets a user's ArchiveSpace credentials.
    There are 3 components to it, the setup code, correct_creds while loop, and the window_asplog_active while loop. It
    uses ASnake.client to authenticate and stay connected to ArchivesSpace. Documentation for ASnake can be found here:
    https://archivesspace-labs.github.io/ArchivesSnake/html/index.html
    For an in-depth review on how this code is structured, see the wiki:
    https://github.com/uga-libraries/ASpace_Batch_Export-Cleanup-Upload/wiki/Code-Structure#get_aspace_log
    Args:
        defaults (UserSetting class): contains the data from defaults.json file, all data the user has specified as default
        as_un (str, optional): user's ArchivesSpace username
        as_pw (str, optional): user's ArchivesSpace password
        as_ap (str, optional): the ArchivesSpace API URL
        as_client (ASnake.client object, optional): the ArchivesSpace ASnake client for accessing and connecting to the API
    Returns:
        as_username (str): user's ArchivesSpace username
        as_password (str): user's ArchivesSpace password
        as_api (str): the ArchivesSpace API URL
        close_program (bool): if a user exits the popup, this will return true and end run_gui()
        client (ASnake.client object): the ArchivesSpace ASnake client for accessing and connecting to the API
    """
    as_username = as_un
    as_password = as_pw
    as_api = as_ap
    client = as_client
    asp_version = None
    save_button_asp = " Save and Continue "
    window_asplog_active = True
    correct_creds = False
    close_program = False
    while correct_creds is False:
        asplog_col1 = [[psg.Text("ArchivesSpace username:", font=("Roboto", 11))],
                       [psg.Text("ArchivesSpace password:", font=("Roboto", 11))],
                       [psg.Text("ArchivesSpace API URL:", font=("Roboto", 11))]]
        asplog_col2 = [[psg.InputText(focus=True, key="_ASPACE_UNAME_")],
                       [psg.InputText(password_char='*', key="_ASPACE_PWORD_")],
                       [psg.InputText(defaults["as_api"], key="_ASPACE_API_")]]
        layout_asplog = [
            [psg.Column(asplog_col1, key="_ASPLOG_COL1_", visible=True),
             psg.Column(asplog_col2, key="_ASPLOG_COL2_", visible=True)],
            [psg.Button(save_button_asp, bind_return_key=True, key="_SAVE_CLOSE_LOGIN_")]
        ]
        window_login = psg.Window("ArchivesSpace Login Credentials", layout_asplog)
        while window_asplog_active is True:
            event_log, values_log = window_login.Read()
            if event_log == "_SAVE_CLOSE_LOGIN_":
                try:
                    connect_client = ASnakeClient(baseurl=values_log["_ASPACE_API_"],
                                                  username=values_log["_ASPACE_UNAME_"],
                                                  password=values_log["_ASPACE_PWORD_"])
                    connect_client.authorize()
                    client = connect_client
                    defaults["as_api"] = values_log["_ASPACE_API_"]

                    window_asplog_active = False
                    correct_creds = True
                except Exception as e:
                    error_message = ""
                    if ":" in str(e):
                        error_divided = str(e).split(":")
                        for line in error_divided:
                            error_message += line + "\n"
                    else:
                        error_message = str(e)
                    psg.Popup("Your username and/or password were entered incorrectly. Please try again.\n\n" +
                              error_message)
            if event_log is None or event_log == 'Cancel':
                window_login.close()
                window_asplog_active = False
                correct_creds = True
                close_program = True
                break
        window_login.close()
    return close_program, client


gui()
