from asnake.client import ASnakeClient
import re
import logging
from secrets import *

id_field_regex = re.compile(r"(^id_+\d)")
logging.basicConfig(filename="unpublish.log", level=logging.INFO)
as_username = input("Enter your ArchivesSpace username: ")
as_password = input("Enter your ArchivesSpace password: ")
client = ASnakeClient(baseurl=as_api, username=as_username, password=as_password)
client.authorize()


def unpublish_records():
    repos = client.get("repositories").json()
    for repo in repos:
        print(repo["name"])
        repo_id = repo["uri"].split("/")[2]
        resources = client.get("repositories/{}/resources".format(repo_id), params={"all_ids": True}).json()
        for resource_id in resources:
            resource = client.get("repositories/{}/resources/{}".format(repo_id, resource_id)).json()
            combined_id = ""
            for field, value in resource.items():
                id_match = id_field_regex.match(field)
                if id_match:
                    combined_id += value + "-"
            combined_id = combined_id[:-1]
            if "[CLOSED]" in combined_id:
                logging.info("Unpublishing {} from {}".format(combined_id, repo["name"]))
                print(combined_id)
                all_uris = client.get("repositories/{}/resources/{}/ordered_records".format(repo_id,
                                                                                            resource_id)).json()
                for uri in all_uris["uris"]:
                    resource_ao = client.get(uri["ref"]).json()
                    resource_ao["publish"] = False
                    update_resource_ao = client.post(uri["ref"], json=resource_ao)
                    if "error" in update_resource_ao.json():
                        logging.error("Error unpublishing Resource/AO: {}\nError: {}".format(uri["ref"],
                                                                                             update_resource_ao.json()))
                        print("Error unpublishing Resource/AO: {}\nError: {}".format(uri["ref"],
                                                                                     update_resource_ao.json()))


unpublish_records()
