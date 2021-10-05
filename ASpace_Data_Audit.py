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


def artypes(wb):
    accession_res_types = ["collection", "papers", "records"]
    ar_types = wb.create_sheet("Accession Resource Types")
    ar_types.title = "Accession Resource Types"
    write_row_index = 2
    headers = ["Accession Resource Type", "Read Only?", "Suppressed?"]
    header_index = 0
    for row in ar_types.iter_rows(min_row=1, max_col=3):
        for cell in row:
            ar_types[cell.coordinate] = headers[header_index]
            ar_types[cell.coordinate].font = Font(bold=True, underline='single')
            header_index += 1
    artypes_statement = ('SELECT CONVERT(ev.value using utf8) AS Accession_Resource_Type, ev.readonly AS Read_Only, '
                         'ev.suppressed AS Suppressed '
                         'FROM enumeration_value AS ev '
                         'WHERE enumeration_id = 7')
    connection, cursor = connect_db()
    results = query_database(connection, cursor, artypes_statement)
    checked_results = []
    for result in list(results):
        single_row = list(result)
        list_index = 0
        for value in single_row:
            if value == 0:
                print(value)
                single_row[list_index] = False
            elif value == 1:
                single_row[list_index] = True
            list_index += 1
        checked_results.append(single_row)
    for result in checked_results:
        ar_types.append(result)
        if result[0] not in accession_res_types:
            for cell in ar_types[f'{write_row_index}:{write_row_index}']:
                cell.fill = PatternFill(start_color='FFFF0000',
                                        end_color='FFFF0000',
                                        fill_type='solid')
        write_row_index += 1


def run():
    workbook, spreadsheet = generate_spreadsheet()
    cuids(workbook)
    tcnb(workbook)
    artypes(workbook)
    workbook.remove(workbook["Sheet"])
    workbook.save(spreadsheet)


run()
