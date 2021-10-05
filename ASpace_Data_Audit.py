import mysql.connector as mysql
from mysql.connector import errorcode
from openpyxl import Workbook
from openpyxl.styles import Font
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


def component_unique_identifiers(connection, cursor, wb):
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
                      'WHERE component_id is not Null')
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


def run():
    workbook, spreadsheet = generate_spreadsheet()
    connection, cursor = connect_db()
    component_unique_identifiers(connection, cursor, workbook)
    workbook.remove(workbook["Sheet"])
    workbook.save(spreadsheet)


run()
