import mysql.connector as mysql
from mysql.connector import errorcode
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill
from secrets import *


def connect_db():
    try:
        staging_connect = mysql.connect(user=as_dbstag_un,
                                        password=as_dbstag_pw,
                                        host=as_dbstag_host,
                                        database=as_dbstag_database,
                                        port=as_dbstag_port)
    except mysql.Error as error:
        if error.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your username or password")
        elif error.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(error)
    else:
        print(staging_connect)
        staging_cursor = staging_connect.cursor()
        return staging_connect, staging_cursor


def query_database(connection, cursor, statement):
    cursor.execute(statement)
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return results


def generate_spreadsheet():
    wb = Workbook()
    data_spreadsheet = 'reports/data_audit.xlsx'
    wb.save(data_spreadsheet)
    return wb, data_spreadsheet


def cuids(wb):
    comp_uniqid = wb.create_sheet("Component Unique Identifiers")
    comp_uniqid.title = "Component Unique Identifiers"
    headers = ["Repository", "Resource ID", "RefID", "Archival Object Title", "Component Unique Identifier"]
    header_index = 0
    for row in comp_uniqid.iter_rows(min_row=1, max_col=5):
        for cell in row:
            comp_uniqid[cell.coordinate] = headers[header_index]
            comp_uniqid[cell.coordinate].font = Font(bold=True, underline='single')
            header_index += 1
    cuid_statement = ('SELECT repo.name AS Repository, resource.identifier AS Resource_ID, ao.ref_id AS Ref_ID, '
                      'ao.title AS Archival_Object_Title, ao.component_id AS Component_Unique_Identifier '
                      'FROM archival_object AS ao '
                      'JOIN repository AS repo ON repo.id = ao.repo_id '
                      'JOIN resource ON resource.id = ao.root_record_id '
                      'WHERE component_id is not Null '
                      'AND resource.publish is True '
                      'AND ao.publish is True')
    connection, cursor = connect_db()
    results = query_database(connection, cursor, cuid_statement)
    redone_results = []
    for result in list(results):
        new_result = list(result)
        res_id_list = new_result[1].strip('[').strip(']').replace('"', '').split(',')
        combined_id = ''
        for id_comp in res_id_list:
            if id_comp != 'null':
                combined_id += id_comp + '-'
        new_result[1] = combined_id[:-1]
        redone_results.append(new_result)
    for result in redone_results:
        comp_uniqid.append(result)


def tcnb(wb):
    tc_nobar = wb.create_sheet("Top Containers - No Barcodes")
    tc_nobar.title = "Top Containers - No Barcodes"
    headers = ["Repository", "Resource ID", "RefID", "Archival Object Title", "Top Container Indicator",
               "Container Type"]
    header_index = 0
    for row in tc_nobar.iter_rows(min_row=1, max_col=6):
        for cell in row:
            tc_nobar[cell.coordinate] = headers[header_index]
            tc_nobar[cell.coordinate].font = Font(bold=True, underline='single')
            header_index += 1
    tcnb_statement = ('SELECT repo.name AS Repository, resource.identifier AS Resource_ID, '
                      'ao.ref_id AS Linked_Archival_Object_REFID, ao.title AS Linked_Archival_Object_Title, '
                      'top_container.indicator, CONVERT(ev.value using utf8) AS Container_Type '
                      'FROM top_container '
                      'JOIN top_container_link_rlshp AS top_rlsh ON top_rlsh.top_container_id = top_container.id '
                      'JOIN sub_container ON top_rlsh.sub_container_id = sub_container.id '
                      'JOIN instance ON instance.id = sub_container.instance_id '
                      'JOIN archival_object AS ao ON ao.id = instance.archival_object_id '
                      'JOIN repository AS repo ON repo.id = ao.repo_id '
                      'JOIN resource ON resource.id = ao.root_record_id '
                      'JOIN enumeration_value AS ev ON ev.id = top_container.type_id '
                      'WHERE top_container.barcode is NULL AND ao.publish is True AND resource.publish is True')
    connection, cursor = connect_db()
    results = query_database(connection, cursor, tcnb_statement)
    redone_results = []
    for result in list(results):
        new_result = list(result)
        res_id_list = new_result[1].strip('[').strip(']').replace('"', '').split(',')
        combined_id = ''
        for id_comp in res_id_list:
            if id_comp != 'null':
                combined_id += id_comp + '-'
        new_result[1] = combined_id[:-1]
        redone_results.append(new_result)
    for result in redone_results:
        tc_nobar.append(result)


def subject_lookalikes():
    pass


def agents_lookalikes():
    pass


def check_controlled_vocabs(wb, terms, vocab, vocab_num):
    vocab_sheet = wb.create_sheet(f"{vocab}")
    vocab_sheet.title = f"{vocab}"
    write_row_index = 2
    headers = [f"{vocab}", "Read Only?", "Suppressed?"]
    header_index = 0
    for row in vocab_sheet.iter_rows(min_row=1, max_col=3):
        for cell in row:
            vocab_sheet[cell.coordinate] = headers[header_index]
            vocab_sheet[cell.coordinate].font = Font(bold=True, underline='single')
            header_index += 1
    statement = (f'SELECT CONVERT(ev.value using utf8) AS {vocab}, ev.readonly AS Read_Only, '
                 f'ev.suppressed AS Suppressed '
                 f'FROM enumeration_value AS ev '
                 f'WHERE enumeration_id = {vocab_num}')
    connection, cursor = connect_db()
    results = query_database(connection, cursor, statement)
    checked_results = []
    for result in list(results):
        single_row = list(result)
        list_index = 0
        for value in single_row:
            if value == 0:
                single_row[list_index] = False
            elif value == 1:
                single_row[list_index] = True
            list_index += 1
        checked_results.append(single_row)
    for result in checked_results:
        vocab_sheet.append(result)
        if result[0] not in terms:
            for cell in vocab_sheet[f'{write_row_index}:{write_row_index}']:
                cell.fill = PatternFill(start_color='FFFF0000',
                                        end_color='FFFF0000',
                                        fill_type='solid')
        write_row_index += 1


def run():
    workbook, spreadsheet = generate_spreadsheet()
    cuids(workbook)
    tcnb(workbook)
    controlled_vocabs = {"Finding_Aid_Status_Terms": [["completed", "unprocessed", "in_process", "problem"], 21],
                         "Name_Sources": [["local", "naf", "ingest"], 4],
                         "Instance_Types": [["audio", "books", "digital_object", "graphic_materials", "maps",
                                             "microform", "mixed_materials", "moving_images", "electronic_records",
                                             "artifacts"], 22],
                         "Extent_Types": [["linear_feet", "box(es)", "item(s)", "gigabyte(s)", "pages", "volume(s)",
                                           "moving_image(s)", "interview(s)", "minutes", "folder(s)",
                                           "sound_recording(s)", "photograph(s)", "oversize_folders"], 14],
                         "Digital_Object_Types": [["cartographic", "mixed_materials", "moving_image",
                                                   "software_multimedia", "sound_recording", "still_image", "text"],
                                                  12],
                         "Container_Types": [["box", "folder", "oversized_box", "oversized_folder", "reel", "roll",
                                              "portfolio", "item", "volume", "physdesc", "electronic_records", "carton",
                                              "drawer", "cassette", "rr", "cs"], 16],
                         "Accession_Resource_Types": [["collection", "papers", "records"], 7]}
    for term, info in controlled_vocabs.items():
        check_controlled_vocabs(workbook, info[0], term, info[1])
    workbook.remove(workbook["Sheet"])
    workbook.save(spreadsheet)


run()
