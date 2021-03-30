from openpyxl import Workbook
from secrets import *
from asnake.aspace import ASpace
from asnake.client import ASnakeClient

aspace = ASpace(baseurl=as_api, username=as_un, password=as_pw)
client = ASnakeClient(baseurl=as_api, username=as_un, password=as_pw)
client.authorize()

wb = Workbook()
wb.active
subjects = wb.create_sheet("Subjects")
subjects.title = "Subjects"
agents = wb.create_sheet("Agents")
agents.title = "Agents"
sheet = wb.get_sheet_by_name("Sheet")
wb.remove(sheet)
print(wb.sheetnames)

headers = ["Title", "URI", "Action", "Merge Into (Optional)"]


def write_headers(sheet):
    header_index = 0
    for row in sheet.iter_rows(min_row=1, max_col=4):
        for cell in row:
            sheet[cell.coordinate] = headers[header_index]
            header_index += 1


def write_data(sheet, data_list):
    data_index = 0
    for data in data_list:
        for row in sheet.iter_rows(min_row=1, max_col=4):
            for cell in row:
                while data_index <= 1:
                    sheet[cell.coordinate] = data[data_index]
                    data_index += 1


def get_subjects(client):
    subjects = []
    arc_subjects = client.get("/subjects", params={"all_ids": True}).json()
    for subject in arc_subjects:
        subject_data = client.get(f"/subjects/{subject}").json()
        subjects.append((subject_data["uri"], subject_data["title"]))
    return subjects


subjects = get_subjects(client)

# write_headers(subjects)
# write_headers(agents)
# wb.save("reports/subjects_agents.xlsx")
