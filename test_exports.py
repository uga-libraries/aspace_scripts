from asnake.client import ASnakeClient
from secrets import *

# as_repo = input("Enter ArchivesSpace repository #: ")
client = ASnakeClient(baseurl=as_api, username=as_username, password=as_password)
client.authorize()

# Dublin Core XML
# do_dc = client.get("/repositories/2/digital_objects/dublin_core/2679.xml")
# # print(do.content)
# with open("do_dublincore.xml", "wb") as file:
#     file.write(do_dc.content)
#     file.close()

# Dublin Core FMT
do_dc_fmt = client.get("/repositories/2/digital_objects/dublin_core/2679.fmt/metadata")
print(do_dc_fmt.content)
# with open("do_dc_fmt.json", "wb") as file:
#     file.write(do_dc_fmt.content)
#     file.close()

# METS XML
# mets_xml = client.get("/repositories/2/digital_objects/mets/2679.xml", params={"dmd": "PKG410P"})
# # print(mets_xml.content)
# with open("do_mets.xml", "wb") as file:
#     file.write(mets_xml.content)
#     file.close()
#
# # METS FMT
mets_fmt = client.get('/repositories/2/digital_objects/mets/2697.fmt/metadata')
print(mets_fmt.content)
# with open("do_mets.fmt", "wb") as file:
#     file.write(mets_fmt.content)
#     file.close()
#
# # MODS XML
# mods_xml = client.get('/repositories/2/digital_objects/mods/2679.xml')
# # print(mods_xml.content)
# with open("do_mods.xml", "wb") as file:
#     file.write(mods_xml.content)
#     file.close()
#
# # MODS FMT
mods_fmt = client.get('/repositories/2/digital_objects/mods/2679.fmt/metadata')
print(mods_fmt.content)
# with open("do_mods.fmt", "wb") as file:
#     file.write(mods_fmt.content)
#     file.close()
#
# # MARC21 FMT
marc21_fmt = client.get('/repositories/2/resources/marc21/577.:fmt/metadata',
                        params={"include_unpublished_marc": True})
print(marc21_fmt, marc21_fmt.content)
# with open("res_marc21.fmt", "wb") as file:
#     file.write(marc21_fmt.content)
#     file.close()
#
# # Resource FMT
res_fmt = client.get('/repositories/2/resource_descriptions/577.:fmt/metadata',
                     params={"fmt": "864442169P755"})
print(res_fmt, res_fmt.content)
# with open("resource.fmt", "wb") as file:
#     file.write(res_fmt.content)
#     file.close()
#
# # Labels FMT
labels_fmt = client.get('/repositories/2/resource_labels/577.:fmt/metadata')
print(labels_fmt, labels_fmt.content)
# with open("labels_metadata.fmt", "wb") as file:
#     file.write(labels_fmt.content)
#     file.close()
#
# # EAC-CPF XML
# eac_cpf_xml = client.get('/repositories/2/archival_contexts/people/159.xml')
# # print(eac_cpf_xml, eac_cpf_xml.content)
# with open("eac_cpf.xml", "wb") as file:
#     file.write(eac_cpf_xml.content)
#     file.close()
#
# # EAC-CPF FMT
eac_cpf_fmt = client.get('/repositories/2/archival_contexts/people/159.:fmt/metadata')
print(eac_cpf_fmt, eac_cpf_fmt.content)
# with open("eac_cpf.fmt", "wb") as file:
#     file.write(eac_cpf_fmt.content)
#     file.close()
#
# # EAC-CPF Corporate XML
# eac_cpf_corp_xml = client.get('/repositories/2/archival_contexts/corporate_entities/1238.xml')
# # print(eac_cpf_corp_xml, eac_cpf_corp_xml.content)
# with open("eac_cpf_corp.xml", "wb") as file:
#     file.write(eac_cpf_corp_xml.content)
#     file.close()
#
# # EAC-CPF Corporate FMT
eac_cpf_corp_fmt = client.get('/repositories/2/archival_contexts/corporate_entities/1238.:fmt/metadata')
print(eac_cpf_corp_fmt, eac_cpf_corp_fmt.content)
# with open("eac_cpf_corp.fmt", "wb") as file:
#     file.write(eac_cpf_corp_fmt.content)
#     file.close()
#
# # EAC-CPF Family XML
# eac_cpf_fam_xml = client.get('/repositories/2/archival_contexts/families/479.xml')
# # print(eac_cpf_fam_xml, eac_cpf_fam_xml.content)
# with open("eac_cpf_fam.xml", "wb") as file:
#     file.write(eac_cpf_fam_xml.content)
#     file.close()
#
# # EAC-CPF Family FMT
eac_cpf_fam_fmt = client.get('/repositories/2/archival_contexts/families/479.fmt/metadata')
print(eac_cpf_fam_fmt, eac_cpf_fam_fmt.content)
# with open("eac_cpf_fam.fmt", "wb") as file:
#     file.write(eac_cpf_fam_fmt.content)
#     file.close()
#
# # EAC-CPF Software XML
# eac_cpf_soft_xml = client.get('/repositories/2/archival_contexts/softwares/1.xml')
# # print(eac_cpf_soft_xml, eac_cpf_soft_xml.content)
# with open("eac_cpf_soft.xml", "wb") as file:
#     file.write(eac_cpf_soft_xml.content)
#     file.close()
#
# #EAC-CPF Software FMT
# eac_cpf_soft_fmt = client.get('/repositories/2/archival_contexts/softwares/1.:fmt/metadata')
# print(eac_cpf_soft_fmt, eac_cpf_soft_fmt.content)
# with open("eac_cpf_soft.fmt", "wb") as file:
#     file.write(eac_cpf_soft_fmt.content)
#     file.close()

