# This script attempts to run SQL updates on Archivists' Toolkit databases for cleanup before migrating to ArchivesSpace
import MySQLdb as sql
from secrets import *

# harg_conn = sql.connect(host=sql_host, port=sql_port, user=sql_user, passwd=sql_passwd, database=atk_dlg)
# harg_cursor = harg_conn.cursor()
# russ_conn = sql.connect(host=sql_host, port=sql_port, user=sql_user, passwd=sql_passwd, database=atk_russ)
# russ_cursor = russ_conn.cursor()

hargrett_updates = ["UPDATE DigitalObjects SET repositoryId=4 WHERE repositoryId=6 AND metsIdentifier LIKE 'harg%';",
                    "UPDATE DigitalObjects SET repositoryId=9 WHERE metsIdentifier LIKE 'hmap%';",
                    "UPDATE ResourcesComponents SET subdivisionIdentifier = '' WHERE NOT subdivisionIdentifier='';",
                    """UPDATE ArchDescriptionRepeatingData SET noteContent = REPLACE(noteContent, '<p xmlns="urn:isbn:1-931666-22-9" xmlns:ns2="http://www.w3.org/1999/xlink">', '') WHERE INSTR(noteContent, '<p xmlns:ns2="urn:isbn:1-931666-22-9" xmlns:ns1="http://www.w3.org/1999/xlink">') OR INSTR(noteContent, '<p xmlns="urn:isbn:1-931666-22-9" xmlns:ns2="http://www.w3.org/1999/xlink">');""",
                    """UPDATE ArchDescriptionRepeatingData SET noteContent = REPLACE(noteContent, '<p xmlns:ns2="urn:isbn:1-931666-22-9" xmlns:ns1="http://www.w3.org/1999/xlink">', '') WHERE INSTR(noteContent, '<p xmlns:ns2="urn:isbn:1-931666-22-9" xmlns:ns1="http://www.w3.org/1999/xlink">') OR INSTR(noteContent, '<p xmlns="urn:isbn:1-931666-22-9" xmlns:ns2="http://www.w3.org/1999/xlink">');""",
                    """UPDATE ResourcesComponents SET resourceLevel = 'file' WHERE resourceLevel = 'collection';""",
                    {"Digital_Objects": ["harg0802-001-001-001", "harg00-16-001-001", "harg00-16-001-002",
                                         "harg00-16-001-003", "harg00-16-001-005", "harg00-16-001-006",
                                         "harg00-16-001-007", "harg00-16-001-008", "harg00-16-001-009",
                                         "harg00-16-001-010", "harg00-16-002a-001", "harg00-16-002a-002",
                                         "harg00-16-002a-003", "harg00-16-002a-004", "harg00-16-002a-005",
                                         "harg00-16-002a-006", "harg00-16-002a-007", "harg00-16-002a-008",
                                         "harg00-16-002a-009", "harg00-16-002a-010", "harg00-16-002a-011",
                                         "harg00-16-002a-012", "harg00-16-002a-013", "harg00-16-002a-014",
                                         "harg00-16-002a-015", "harg00-16-002a-016", "harg00-16-002a-017",
                                         "harg00-16-002a-018", "harg00-16-002a-019", "harg00-16-002a-020",
                                         "harg00-16-002b-001", "harg00-16-002b-002", "harg00-16-002b-003",
                                         "harg00-16-002b-004", "harg00-16-002b-005", "harg97-106-001-006",
                                         "harg97-106-001-007", "harg97-106-016-006", "harg10-110-073-001",
                                         "harg10-110-073-002", "harg10-110-073-003", "harg10-110-073-004",
                                         "harg10-110-073-005", "harg10-110-073-006", "harg10-110-074-001",
                                         "harg10-110-074-002", "harg10-110-074-003", "harg10-110-074-004",
                                         "harg10-110-074-005", "harg10-110-074-006", "harg10-110-074-007",
                                         "harg10-110-074-008", "harg10-110-075-001", "harg10-110-075-002",
                                         "harg10-110-075-003", "harg10-110-075-004", "harg10-110-075-005",
                                         "harg10-110-075-006", "harg10-110-075-007", "harg10-110-075-008",
                                         "harg10-110-075-009", "harg10-110-076-001", "harg10-110-076-002",
                                         "harg10-110-076-003", "harg10-110-076-004", "harg10-110-076-005",
                                         "harg10-110-076-006", "harg10-110-076-007", "harg10-110-076-008",
                                         "harg10-110-076-009", "harg10-110-076-010"]}]

russell_updates = ["UPDATE FileVersions SET useStatement='Audio-Streaming' WHERE useStatement='Audio streaming' OR useStatement='Audio-streaming'; OR useStatement='audio_streaming';",
                   "UPDATE FileVersions SET eadDaoShow='replace' WHERE eadDaoShow='onLoad' OR eadDaoShow='onload';",
                   """UPDATE ArchDescriptionRepeatingData SET noteContent = REPLACE(noteContent, '<p xmlns="urn:isbn:1-931666-22-9" xmlns:ns2="http://www.w3.org/1999/xlink">', '') WHERE INSTR(noteContent, '<p xmlns:ns2="urn:isbn:1-931666-22-9" xmlns:ns1="http://www.w3.org/1999/xlink">') OR INSTR(noteContent, '<p xmlns="urn:isbn:1-931666-22-9" xmlns:ns2="http://www.w3.org/1999/xlink">');""",
                   """UPDATE ArchDescriptionRepeatingData SET noteContent = REPLACE(noteContent, '<p xmlns:ns2="urn:isbn:1-931666-22-9" xmlns:ns1="http://www.w3.org/1999/xlink">', '') WHERE INSTR(noteContent, '<p xmlns:ns2="urn:isbn:1-931666-22-9" xmlns:ns1="http://www.w3.org/1999/xlink">') OR INSTR(noteContent, '<p xmlns="urn:isbn:1-931666-22-9" xmlns:ns2="http://www.w3.org/1999/xlink">');""",
                   "UPDATE ArchDescriptionInstances SET instanceType = 'Graphic materials' WHERE resourceComponentId = 55585;",
                   "UPDATE ResourcesComponents SET extentType = 'photograph(s)' WHERE resourceComponentId = 104406;"]

print("Updating Hargrett database...\n")
# for command in hargrett_updates:
#     if isinstance(command, dict):
#         metsids = list(command.values())
#         record_count = 0
#         for do_id in metsids[0]:
#             do_command = "UPDATE DigitalObjects SET repositoryId=6 WHERE metsIdentifier='{}';".format(do_id)
#             harg_cursor.execute(do_command)
#             harg_conn.commit()
#             record_count += harg_cursor.rowcount
#         print("UPDATE DigitalObjects SET repositoryId=6 WHERE metsIdentifier='{}';" + ":\n", record_count,
#               "record(s) affected")
#     else:
#         harg_cursor.execute(command)
#         print(command + ":\n", harg_cursor.rowcount, "record(s) affected")
# print("Done \n" + "-"*100)
#
# print("Updating Russell database...\n")
# for command in russell_updates:
#     russ_cursor.execute(command)
#     print(command + ":\n", russ_cursor.rowcount, "record(s) affected")
# print("Done \n" + "-"*100)

ids = ["harg0802-001-001-001", "harg00-16-001-001", "harg00-16-001-002",
                                         "harg00-16-001-003", "harg00-16-001-005", "harg00-16-001-006",
                                         "harg00-16-001-007", "harg00-16-001-008", "harg00-16-001-009",
                                         "harg00-16-001-010", "harg00-16-002a-001", "harg00-16-002a-002",
                                         "harg00-16-002a-003", "harg00-16-002a-004", "harg00-16-002a-005",
                                         "harg00-16-002a-006", "harg00-16-002a-007", "harg00-16-002a-008",
                                         "harg00-16-002a-009", "harg00-16-002a-010", "harg00-16-002a-011",
                                         "harg00-16-002a-012", "harg00-16-002a-013", "harg00-16-002a-014",
                                         "harg00-16-002a-015", "harg00-16-002a-016", "harg00-16-002a-017",
                                         "harg00-16-002a-018", "harg00-16-002a-019", "harg00-16-002a-020",
                                         "harg00-16-002b-001", "harg00-16-002b-002", "harg00-16-002b-003",
                                         "harg00-16-002b-004", "harg00-16-002b-005", "harg97-106-001-006",
                                         "harg97-106-001-007", "harg97-106-016-006", "harg10-110-073-001",
                                         "harg10-110-073-002", "harg10-110-073-003", "harg10-110-073-004",
                                         "harg10-110-073-005", "harg10-110-073-006", "harg10-110-074-001",
                                         "harg10-110-074-002", "harg10-110-074-003", "harg10-110-074-004",
                                         "harg10-110-074-005", "harg10-110-074-006", "harg10-110-074-007",
                                         "harg10-110-074-008", "harg10-110-075-001", "harg10-110-075-002",
                                         "harg10-110-075-003", "harg10-110-075-004", "harg10-110-075-005",
                                         "harg10-110-075-006", "harg10-110-075-007", "harg10-110-075-008",
                                         "harg10-110-075-009", "harg10-110-076-001", "harg10-110-076-002",
                                         "harg10-110-076-003", "harg10-110-076-004", "harg10-110-076-005",
                                         "harg10-110-076-006", "harg10-110-076-007", "harg10-110-076-008",
                                         "harg10-110-076-009", "harg10-110-076-010"]
for id in ids:
    print(id)
