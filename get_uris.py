import PySimpleGUI as psg
import sys
import json
from openpyxl import load_workbook
from asnake.client import ASnakeClient


def gui():
    defaults = psg.UserSettings()
    close_program, client, repositories = get_aspace_log(defaults)
    if close_program is True:
        sys.exit()
    main_layout = [[psg.Text("Choose your repository:", font=("Roboto", 12))],
                   [psg.DropDown([repo for repo in repositories.keys()], readonly=True,
                                 default_value=defaults["repo_default"], key="_REPO_SELECT_",),
                    psg.Button(" SAVE ", key="_SAVE_REPO_")],
                   [psg.FileBrowse(' Select Digital Objects File ', file_types=(("Excel Files", "*.xlsx"),),),
                    psg.InputText(default_text=defaults['_DO_FILE_'], key='_DO_FILE_')],
                   [psg.FileBrowse(' Select Template ', file_types=(("Excel Files", "*.xlsx"),),),
                    psg.InputText(default_text=defaults['_DOTEMP_FILE_'], key='_DOTEMP_FILE_')],
                   [psg.Button(' START ', key='_WRITE_DOS_', disabled=False)],
                   [psg.Output(size=(80, 18), key="_output_")]]
    window = psg.Window('Write Digital Objects to Template', layout=main_layout)
    while True:
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
                write_digobjs(values['_DO_FILE_'], values['_DOTEMP_FILE_'], client,
                              repositories[values["_REPO_SELECT_"]], window)
        if event == "_SAVE_REPO_":
            defaults["repo_default"] = values["_REPO_SELECT_"]


def write_digobjs(digobj_file, dotemp_file, client, repo, gui_window):
    gui_window[f'{"_WRITE_DOS_"}'].update(disabled=True)
    digobj_wb = load_workbook(digobj_file)
    digobj_sheet = digobj_wb.active
    dotemp_wb = load_workbook(dotemp_file)
    dotemp_sheet = dotemp_wb.active
    columns = [4, 6, 7, 8, 9, 10]
    write_row_index = 6
    total_digobjs = 0
    for row in digobj_sheet.iter_rows(min_row=2, values_only=True):
        total_digobjs += 1
        digobj_id = row[0]
        digobj_title = row[2]
        digobj_url = row[3]
        digobj_date = row[5]
        digobj_publish = row[8]
        search_archobjs = client.get_paged(f"/repositories/{repo}/search",
                                           params={"q": f'title:"{digobj_title} , {digobj_date}"',
                                                   "type": ['archival_object']})
        search_results = []
        for results in search_archobjs:
            search_results.append(results)
        if len(search_results) > 1:
            multresults_layout = [[psg.Text(f'\n\nFound multiple options for\n{digobj_title}, {digobj_date}\n\n'
                                            f'Choose one of the following:\n')],
                                  [psg.Listbox([f'{results["title"]}' for results in search_results], size=(80, 5),
                                               key="_ARCHOBJ_FILE_")],
                                  [psg.Button(" SELECT ", key="_SELECT_ARCHOBJ_")]]
            multresults_window = psg.Window("Multiple Results for Archival Object", multresults_layout)
            selection = True
            while selection is True:
                multresults_event, multresults_values = multresults_window.Read()
                if multresults_event == "_SELECT_ARCHOBJ_":
                    for result in search_results:
                        print(multresults_values["_ARCHOBJ_FILE_"])
                        if result["title"] == multresults_values["_ARCHOBJ_FILE_"][0]:
                            uri = result["uri"]
                            resource_uri = result["resource"]
                            selection = False
                            multresults_window.close()
                            break
        else:
            for result in search_results:
                uri = result["uri"]
                resource_uri = result["resource"]
        column_map = {4: resource_uri, 6: uri, 7: digobj_id, 8: digobj_title, 9: digobj_publish, 10: digobj_url}
        for column in columns:
            dotemp_sheet.cell(row=write_row_index, column=column).value = column_map[column]
        write_row_index += 1
        print(column_map)
        try:
            dotemp_wb.save(dotemp_file)
        except Exception as e:
            print(f'\n\nFailed opening {dotemp_file}. Please close the record before trying again.\nError: {e}')
            gui_window[f'{"_WRITE_DOS_"}'].update(disabled=False)
            return
    digobj_wb.close()
    dotemp_wb.close()
    print(f'\n{"*"*112}\n{" "*40}Finished writing {total_digobjs} to {dotemp_sheet}\n{"*"*112}')
    gui_window[f'{"_WRITE_DOS_"}'].update(disabled=False)


def get_aspace_log(defaults):
    """
    Gets a user's ArchiveSpace credentials.
    There are 3 components to it, the setup code, correct_creds while loop, and the window_asplog_active while loop. It
    uses ASnake.client to authenticate and stay connected to ArchivesSpace. Documentation for ASnake can be found here:
    https://archivesspace-labs.github.io/ArchivesSnake/html/index.html
    Args:
        defaults (UserSetting class): contains the data from defaults.json file, all data the user has specified as default
    Returns:
        close_program (bool): if a user exits the popup, this will return true and end run_gui()
        connect_client (ASnake.client object): the ArchivesSpace ASnake client for accessing and connecting to the API
    """
    connect_client = None
    repositories = {}
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
                    defaults["as_api"] = values_log["_ASPACE_API_"]
                    repo_results = connect_client.get('/repositories')
                    repo_results_dec = json.loads(repo_results.content.decode())
                    for result in repo_results_dec:
                        uri_components = result["uri"].split("/")
                        repositories[result["name"]] = int(uri_components[-1])
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
    return close_program, connect_client, repositories


gui()
