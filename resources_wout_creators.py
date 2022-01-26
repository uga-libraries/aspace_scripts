# This script exports all published resources for every repository in an ArchivesSpace instance and assigns a
# concatenated version of the identifier as the filename.
import re
from secrets import *
from asnake.client import ASnakeClient

id_field_regex = re.compile(r"(^id_+\d)")
id_combined_regex = re.compile(r'[\W_]+', re.UNICODE)


def check_creators(client):
    repos = client.get("repositories").json()
    for repo in repos:
        print(repo["name"] + "\n")
        repo_id = repo["uri"].split("/")[2]
        resources = client.get("repositories/{}/resources".format(repo_id), params={"all_ids": True}).json()
        for resource_id in resources:
            has_creator = False
            resource = client.get("repositories/{}/resources/{}".format(repo_id, resource_id))
            combined_id = ""
            for field, value in resource.json().items():
                id_match = id_field_regex.match(field)
                if id_match:
                    combined_id += value + "-"
            combined_id = combined_id[:-1]
            if resource.json()["publish"] is True:
                if resource.status_code == 200:
                    if "linked_agents" in resource.json():
                        linked_agents = resource.json()["linked_agents"]
                        for linked_agent in linked_agents:
                            if linked_agent["role"] == "creator":
                                has_creator = True
                        if has_creator is False:
                            print(f'{repo["name"]},{combined_id},Publish: {resource.json()["publish"]}')
                    else:
                        print(f'{repo["name"]},{combined_id},Publish: {resource.json()["publish"]}')
        print("-" * 100)


asp_client = ASnakeClient(baseurl=as_api, username=as_un, password=as_pw)
asp_client.authorize()
check_creators(asp_client)
