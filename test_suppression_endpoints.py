# Tests suppression.rb endpoints for ArchivesSpace

import requests

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

req_auth = requests.post(as_api_stag + '/users/' + as_un + '/login?password=' + as_pw).json()
session = req_auth['session']
headers = {'X-ArchivesSpace-Session': session, 'Content-Type': 'application/json'}

client = ASnakeClient(baseurl=as_api_stag, username=as_un, password=as_pw)
client.authorize()

# Suppress Archival Object


# Suppress Resource
suppress_resource = client.post("/repositories/:repo_id:/resources/:resource_id:/suppressed",
                                params={"suppressed": True})
# Replace :repo_id: with the ArchivesSpace repository ID, :resource_id: with the ArchivesSpace ID of the resource, and
# change the "suppressed" value to True to suppress the resource and False to unsuppress a resource

print(suppress_resource.json())
# Output: {'status': 'Suppressed', 'id': 5812, 'suppressed_state': True}

# $ curl -X POST -H "X-ArchivesSpace-Session: $SESSION" "http://:your_api_url:/repositories/:repo_id:/resources/:resource_id:/suppressed?suppressed=true"
#   % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
#                                  Dload  Upload   Total   Spent    Left  Speed
# 100    58  100    58    0     0    276      0 --:--:-- --:--:-- --:--:--   276{"status":"Suppressed","id"::resource_id:,"suppressed_state":true}




