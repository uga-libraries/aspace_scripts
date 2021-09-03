# This script publishes all digital objects
from asnake.client import ASnakeClient
from secrets import *

as_username = input("ArchivesSpace username: ")
as_password = input("ArchivesSpace password: ")

client = ASnakeClient(baseurl=as_api, username=as_username, password=as_password)
client.authorize()

repos = client.get("repositories").json()
print("Publishing Digital Objects...", end='', flush=True)
for repo in repos:
    digital_object = {}
    dig_objs_per_repo = []
    repo_digital_objects = client.get(repo["uri"] + "/digital_objects?all_ids=true").json()
    for dig_obj_id in repo_digital_objects:
        object_request = repo["uri"] + "/digital_objects/" + str(dig_obj_id) + "/publish"
        try:
            client.post(object_request)
        except Exception as e:
            print("Error found when requesting id: " + str(e) + "\n" + object_request)
    #     digital_object[dig_obj_id] = client.get(repo["uri"] + "/digital_objects/" + str(dig_obj_id)).json()
    #     dig_objs_per_repo.append(digital_object)
    # repo_dig_objects[repo['name']] = dig_objs_per_repo
print("Done")
# print(json_data)
