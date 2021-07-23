from secrets import *
from openpyxl import Workbook, load_workbook
from asnake.aspace import ASpace
from asnake.client import ASnakeClient

aspace = ASpace(baseurl=as_api, username=as_un, password=as_pw)
client = ASnakeClient(baseurl=as_api, username=as_un, password=as_pw)
client.authorize()

excel_file = "data/ms4401 do.xlsx"
digital_objects = load_workbook(excel_file)
sheet = digital_objects.active
for row in sheet.iter_rows(min_row=2, values_only=True):
    archobj_name = row[2]
    search_archobjs = client.get_paged(f"/repositories/{4}/search", params={"q": 'title:' + archobj_name,
                                       "type": ['archival_object']})
    for results in search_archobjs:
        print(results)
