# Tests suppression.rb endpoints for ArchivesSpace

import requests

from asnake.client import ASnakeClient
import asnake.logging as logging
from secrets import *

logging.setup_logging(level='DEBUG')

# cURL example template
# curl -s -F password="password" "http://localhost:8089/users/:your_username:/login"
# # Replace "password" with your password, "http://localhost:8089 with your ASpace API URL, and :your_username: with
# # your ArchivesSpace username
#
# set SESSION="session_id"
# # If using Git Bash, replace set with export
#
# curl -H "X-ArchivesSpace-Session: $SESSION" //
# "http://localhost:8089/date_calculator?record_uri=/repositories/{aspace_repository_id}/archival_objects/{aspace_object_id}"
# # Replace "http://localhost:8089" with your ASpace API URL, {aspace_repository_id} with the repository ID, and
# # {aspace_object_id} with the archival object ID

# Python example template
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
#
# req_auth = requests.post(as_api_stag + '/users/' + as_un + '/login?password=' + as_pw).json()
# session = req_auth['session']
# headers = {'X-ArchivesSpace-Session': session, 'Content-Type': 'application/json'}
#
# client = ASnakeClient(baseurl=as_api_stag, username=as_un, password=as_pw)
# client.authorize()


# ______Suppress Accession______
# ____PYTHON EXAMPLE____
    # suppress_accession = client.post("repositories/:repo_id:/accessions/:accession_id:/suppressed",
    #                                  params={"suppressed": True})
# Replace :repo_id: with the ArchivesSpace repository ID, :accession_id: with the ArchivesSpace ID of the accession, and
# change the "suppressed" value to True to suppress the accession or False to unsuppress the accession

    # print(suppress_accession.json())
# Output: {'status': 'Suppressed', 'id': 3828, 'suppressed_state': True}

# ____cURL EXAMPLE____
    # $ curl -X POST -H "X-ArchivesSpace-Session: $SESSION" "http://localhost:8089/repositories/:repo_id:/accessions/:accession_id:/suppressed?suppressed=true"
# Replace http://localhost:8089 with your ArchivesSpace API URL, :repo_id: with the ArchivesSpace repository ID,
# :accession_id: with the ArchivesSpace ID of the accession, and change the "suppressed" value to true to suppress the
# accession or false to unsuppress the accession

# Output: {"status":"Suppressed","id":3828,"suppressed_state":true}

#   % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
#                                  Dload  Upload   Total   Spent    Left  Speed
# 100    58  100    58    0     0    235      0 --:--:-- --:--:-- --:--:--   235{"status":"Suppressed","id":3828,"suppressed_state":true}


# ______Suppress Resource______
# ____PYTHON EXAMPLE____
    # suppress_resource = client.post("/repositories/:repo_id:/resources/:resource_id:/suppressed",
    #                                 params={"suppressed": False})
# Replace :repo_id: with the ArchivesSpace repository ID, :resource_id: with the ArchivesSpace ID of the resource, and
# change the "suppressed" value to True to suppress the resource or False to unsuppress the resource

    # print(suppress_resource.json())
# Output: {'status': 'Suppressed', 'id': 5812, 'suppressed_state': True}

# ____cURL EXAMPLE____
    # $ curl -X POST -H "X-ArchivesSpace-Session: $SESSION" "http://localhost:8089/repositories/:repo_id:/resources/:resource_id:/suppressed?suppressed=true"
# Replace http://localhost:8089 with your ArchivesSpace API URL, :repo_id: with the ArchivesSpace repository ID,
# :resource_id: with the ArchivesSpace ID of the resource, and change the "suppressed" value to true to suppress the
# resource or false to unsuppress the resource

# Output: {"status":"Suppressed","id":5812,"suppressed_state":true}

#   % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
#                                  Dload  Upload   Total   Spent    Left  Speed
# 100    58  100    58    0     0    276      0 --:--:-- --:--:-- --:--:--   276{"status":"Suppressed","id":5812,"suppressed_state":true}


# ______Suppress Archival Object______
# ____PYTHON EXAMPLE____
    # suppress_archobj = client.post("/repositories/:repo_id:/archival_objects/:archobj_id:/suppressed",
    #                                params={"suppressed": True})
# Replace :repo_id: with the ArchivesSpace repository ID, :archobj_id: with the ArchivesSpace ID of the archival object,
# and change the "suppressed" value to True to suppress the archival object or False to unsuppress the archival object

    # print(suppress_archobj.json())
# Output: {'status': 'Suppressed', 'id': 717782, 'suppressed_state': True}

# ____cURL EXAMPLE____
    # $ curl -X POST -H "X-ArchivesSpace-Session: $SESSION" "http://localhost:8089/repositories/:repo_id:/archival_objects/:archobj_id:/suppressed?suppressed=true"
# Replace http://localhost:8089 with your ArchivesSpace API URL, :repo_id: with the ArchivesSpace repository ID,
# :archobj_id: with the ArchivesSpace ID of the archival object, and change the "suppressed" value to true to suppress
# the archival object or false to unsuppress the archival object

# Output: {"status":"Suppressed","id":717782,"suppressed_state":true}

#   % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
#                                  Dload  Upload   Total   Spent    Left  Speed
# 100    60  100    60    0     0    631      0 --:--:-- --:--:-- --:--:--   638{"status":"Suppressed","id":717782,"suppressed_state":true}


# ______Suppress Digital Object______
# ____PYTHON EXAMPLE____
    # suppress_digobj = client.post("/repositories/:repo_id:/digital_objects/:digobj_id:/suppressed",
    #                               params={"suppressed": True})
# Replace :repo_id: with the ArchivesSpace repository ID, :digobj_id: with the ArchivesSpace ID of the digital object,
# and change the "suppressed" value to True to suppress the digital object or False to unsuppress the digital object

    # print(suppress_digobj.json())
# Output: {'status': 'Suppressed', 'id': 14098, 'suppressed_state': True}

# ____cURL EXAMPLE____
    # $ curl -X POST -H "X-ArchivesSpace-Session: $SESSION" "http://localhost:8089/repositories/:repo_id:/digital_objects/:digobj_id:/suppressed?suppressed=false"
# Replace http://localhost:8089 with your ArchivesSpace API URL, :repo_id: with the ArchivesSpace repository ID,
# :digobj_id: with the ArchivesSpace ID of the digital object, and change the "suppressed" value to true to suppress
# the digital object or false to unsuppress the digital object

# Output: {"status":"Suppressed","id":14098,"suppressed_state":true}

#   % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
#                                  Dload  Upload   Total   Spent    Left  Speed
# 100    60  100    60    0     0    847      0 --:--:-- --:--:-- --:--:--   857{"status":"Suppressed","id":14098,"suppressed_state":false}


# ______Suppress Digital Object Component______
# ____PYTHON EXAMPLE____
    # suppress_digobjcomp = client.post("/repositories/:repo_id:/digital_object_components/:digobjcomp_id:/suppressed",
    #                                   params={"suppressed": True})
# Replace :repo_id: with the ArchivesSpace repository ID, :digobjcomp_id: with the ArchivesSpace ID of the digital
# object component, and change the "suppressed" value to True to suppress the digital object component or False to
# unsuppress the digital object component

    # print(suppress_digobjcomp.json())
# Output: {'status': 'Suppressed', 'id': 3, 'suppressed_state': True}

# ____cURL EXAMPLE____
    # $ curl -X POST -H "X-ArchivesSpace-Session: $SESSION" "http://localhost:8089/repositories/:repo_id:/digital_object_components/:digobjcomp_id:/suppressed?suppressed=true"
# Replace http://localhost:8089 with your ArchivesSpace API URL, :repo_id: with the ArchivesSpace repository ID,
# :digobjcomp_id: with the ArchivesSpace ID of the digital object component, and change the "suppressed" value to True
# to suppress the digital object component or False to unsuppress the digital object component

# Output: {"status":"Suppressed","id":3,"suppressed_state":true}

#   % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
#                                  Dload  Upload   Total   Spent    Left  Speed
# 100    55  100    55    0     0    480      0 --:--:-- --:--:-- --:--:--   486{"status":"Suppressed","id":3,"suppressed_state":true}
