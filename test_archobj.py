import pandas
from asnake.client import ASnakeClient
import asnake.logging as logging
from secrets import *

logging.setup_logging(level='DEBUG')

# Example template
# from asnake.client import ASnakeClient  # import the ArchivesSnake client
#
# client = ASnakeClient(baseurl="http://localhost:8089", username="admin", password="admin")
# # replace http://localhost:8089 with your ArchivesSpace API URL and admin for your username and password
#
# client.authorize()  # authorizes the client
#
# archival_object = client.get("/repositories/2/archival_objects/48")
# # replace 2 for your repository ID and 48 with your archival object ID. Find these in the URI of your archival
# # object in the staff interface
#
# print(archival_object.json())
# # Output: {"lock_version":0,"position":0,"publish":true,"ref_id":"ref01_uqj","title":"Archival Object",...}

client = ASnakeClient(baseurl=as_api_stag, username=as_un, password=as_pw)
client.authorize()


# Create an Archival Object
# test_ao1_shell = """{"jsonmodel_type": "archival_object", "publish": True, "external_ids": [], "subjects": [], "linked_events": [], "extents": \[\{"number": "2", "portion": "whole", "extent_type": "folder(s)", "jsonmodel_type": "extent"\}\], "lang_materials": [], "dates": \[\{"expression": "1927, 1929","begin": "1927", "end": "1929", "date_type": "inclusive", "label": "creation", "jsonmodel_type": "date"\}\], "external_documents": [], "rights_statements": [], "linked_agents": [], "is_slug_auto": True, "restrictions_apply": False, "ancestors": [], "instances": [], "notes": [], "ref_id": "20029191", "level": "file", "title": "Archival Object title", "resource": \{"ref": "/repositories/2/resources/5783"\}}"""
# test_ao = {"jsonmodel_type": "archival_object",
#             "publish": True,
#             "external_ids": [],
#             "subjects": [],  # TODO: fill this out
#             "linked_events": [],
#             "extents": [{"number": "2",
#                          "portion": "whole",
#                          "extent_type": "folder(s)",
#                          "jsonmodel_type": "extent"}],
#             "lang_materials": [],  # TODO: fill this out
#             "dates": [
#                 {"expression": "1927, 1929",
#                  "begin": "1927",
#                  "end": "1929",
#                  "date_type": "inclusive",
#                  "label": "creation",
#                  "jsonmodel_type": "date"}],
#             "external_documents": [],
#             "rights_statements": [],
#             "linked_agents": [],
#             "is_slug_auto": True,
#             "restrictions_apply": False,
#             "ancestors": [],
#             "instances": [],
#             "notes": [],
#             "ref_id": "20029191",  # TODO: Can leave this out
#             "level": "file",
#             "title": "Archival Object title",
#             "resource": {"ref": "/repositories/2/resources/5783"}
#             }
#
# create_ao = client.post('repositories/2/archival_objects', json=test_ao)
# print(create_ao.json())
#
# test_ao = {'lock_version': 0, 'position': 0, 'publish': True, 'ref_id': 'ref15_eju',
#            'title': '<emph render="bold">I. Correspondence/Speech</emph>',
#            'display_string': '<emph render="bold">I. Correspondence/Speech</emph>, 1927, 1929',
#            'restrictions_apply': False,
#            'created_by': 'admin', 'last_modified_by': 'admin', 'create_time': '2020-12-14T16:30:36Z',
#            'system_mtime': '2021-01-15T18:49:04Z', 'user_mtime': '2020-12-14T16:30:36Z', 'suppressed': False,
#            'is_slug_auto': True, 'level': 'subseries', 'jsonmodel_type': 'archival_object', 'external_ids': [
#         {'external_id': '14', 'source': 'Archivists Toolkit Database::RESOURCE_COMPONENT', 'created_by': 'admin',
#          'last_modified_by': 'admin', 'create_time': '2020-12-14T16:30:36Z', 'system_mtime': '2020-12-14T16:30:36Z',
#          'user_mtime': '2020-12-14T16:30:36Z', 'jsonmodel_type': 'external_id'}], 'subjects': [], 'linked_events': [],
#            'extents': [{'lock_version': 0, 'number': '2', 'created_by': 'admin', 'last_modified_by': 'admin',
#                         'create_time': '2020-12-14T16:30:36Z', 'system_mtime': '2020-12-14T16:30:36Z',
#                         'user_mtime': '2020-12-14T16:30:36Z', 'portion': 'whole', 'extent_type': 'folder(s)',
#                         'jsonmodel_type': 'extent'}], 'lang_materials': [], 'dates': [
#         {'lock_version': 0, 'expression': '1927, 1929', 'begin': '1927', 'end': '1929', 'created_by': 'admin',
#          'last_modified_by': 'admin', 'create_time': '2020-12-14T16:30:36Z', 'system_mtime': '2020-12-14T16:30:36Z',
#          'user_mtime': '2020-12-14T16:30:36Z', 'date_type': 'inclusive', 'label': 'creation',
#          'jsonmodel_type': 'date'}],
#            'external_documents': [], 'rights_statements': [], 'linked_agents': [],
#            'ancestors': [{'ref': '/repositories/2/archival_objects/1', 'level': 'series'},
#                          {'ref': '/repositories/2/resources/1', 'level': 'collection'}], 'instances': [], 'notes': [
#         {'jsonmodel_type': 'note_multipart', 'subnotes': [{
#             'content': "Correspondence pertains to Russell's election as Speaker and to legislation for improving Georgia roads. Speech includes handwritten notes and text for an Armistice Day speech at Barnesville, Georgia.\n\n",
#             'jsonmodel_type': 'note_text', 'publish': True}],
#          'type': 'scopecontent', 'persistent_id': 'bbb503e1e26081d83d4d46818d9a50db', 'publish': True}],
#            'uri': '/repositories/2/archival_objects/2', 'repository': {'ref': '/repositories/2'},
#            'resource': {'ref': '/repositories/2/resources/1'}, 'parent': {'ref': '/repositories/2/archival_objects/1'},
#            'has_unpublished_ancestor': False}


# Update an Archival Object
# original_ao = client.get("/repositories/2/archival_objects/707460").json()
# new_ao = original_ao
# new_ao["title"] = "New title"
# update_ao = client.post("/repositories/2/archival_objects/707460", json=new_ao)
# print(update_ao.json())


# Set the parent/position of an Archival Object in a tree
# set_child_position = client.post("/repositories/2/archival_objects/707460/parent", params={"parent": 707458,
#                                                                                            "position": 2})
# print(set_child_position.json())


# Get an Archival Object by ID
# ao_1 = client.get("/repositories/2/archival_objects/2")
# print(ao_1.json())


# Get the children of an Archival Object
# get_children = client.get("/repositories/2/archival_objects/707458/children")
# print(get_children.json())


# Get the previous record in the tree for an Archival Object
# get_previous_ao = client.get("/repositories/2/archival_objects/707461/previous")
# print(get_previous_ao.json())


# Get a list of Archival Objects for a Repository
# get_repo_aos_allids = client.get("repositories/6/archival_objects", params={"all_ids": True})
# get_repo_aos_set = client.get("repositories/2/archival_objects", params={"id_set": [227012, 227013, 227014]})
# get_repo_aos_pages = client.get("repositories/2/archival_objects", params={"page": 1, "page_size": 10})
#
# print(get_repo_aos_allids.json())
# print(get_repo_aos_set.json())
# print(get_repo_aos_pages.json())



# Delete an Archival Object
# delete_ao = client.delete("/repositories/2/archival_objects/707461")
# print(delete_ao.json())


# Publish an Archival Object and all its sub-records and components
# publish_ao = client.post("/repositories/2/archival_objects/226994/publish")
# print(publish_ao.json())


# Unpublish an Archival Object and all its sub-records and components
# unpublish_ao = client.post("/repositories/2/archival_objects/226994/unpublish")
# print(unpublish_ao.json())


# Get a list of record types in the graph of an archival object
# get_ao_types = client.get("/repositories/2/archival_objects/226994/models_in_graph")
# print(get_ao_types.json())
