from secrets import *
from openpyxl import Workbook, load_workbook
from asnake.aspace import ASpace
from asnake.client import ASnakeClient

aspace = ASpace(baseurl=as_api, username=as_un, password=as_pw)
client = ASnakeClient(baseurl=as_api, username=as_un, password=as_pw)
client.authorize()

digobj_file = "data/ms4401 do.xlsx"
digital_objects_wb = load_workbook(digobj_file)
digobj_sheet = digital_objects_wb.active
for row in digobj_sheet.iter_rows(min_row=2, values_only=True):
    digobj_id = row[1]
    digobj_title = row[2]
    digobj_url = row[3]
    digobj_date = row[5]
    digobj_publish = row[6]
    search_archobjs = client.get_paged(f"/repositories/{4}/search",
                                       params={"q": f'title:"{digobj_title}, {digobj_date}"',
                                               "type": ['archival_object']})
    search_results = []
    for results in search_archobjs:
        search_results.append(results)
    if len(search_results) > 1:
        print(f'{digobj_title}, {digobj_date}')
        for result in search_results:
            print(result)
    else:
        for result in search_results:
            uri = result["uri"]

    dotemp_file = "data/bulk_import_DO_template.xlsx"
    dotemp_wb = load_workbook(dotemp_file)
    dotemp_sheet = dotemp_wb.active
    columns = [6, 7, 8, 9, 10]
    column_map = {6: uri, 7: digobj_id, 8: digobj_title, 9: digobj_publish, 10: digobj_url}
    row_index = 6
    for temp_row in dotemp_sheet.iter_rows(max_col=10):
        column_index = 0
        for cell in temp_row:
            if not column_index > 4:
                dotemp_sheet.cell(row=row_index, column=columns[column_index]).value = column_map[columns[column_index]]
                dotemp_wb.save(dotemp_file)
                column_index += 1
        row_index += 1
    #     row[5] = uri
    #     row[6] = digobj_id
    #     row[7] = digobj_title
    #     row[8] = digobj_publish
    #     row[9] = digobj_url
digital_objects_wb.close()
dotemp_wb.close()
