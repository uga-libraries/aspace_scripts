# This script exports all published resources for every repository in an ArchivesSpace instance and assigns a
# concatenated version of the identifier as the filename.
import os
import re
from secrets import *
from asnake.client import ASnakeClient
from pathlib import Path

id_field_regex = re.compile(r"(^id_+\d)")
id_combined_regex = re.compile(r'[\W_]+', re.UNICODE)


def export_eads(client, source_path):
    repos = client.get("repositories").json()
    for repo in repos:
        print(repo["name"] + "\n")
        repo_id = repo["uri"].split("/")[2]
        repo_folder = str(Path(source_path, repo["name"]))
        if not os.path.isdir(str(Path(source_path, repo["name"]))):
            repo_folder = str(Path(source_path, repo["name"]))
            os.mkdir(repo_folder)
        resources = client.get("repositories/{}/resources".format(repo_id), params={"all_ids": True}).json()
        for resource_id in resources:
            resource = client.get("repositories/{}/resources/{}".format(repo_id, resource_id))
            combined_id = ""
            for field, value in resource.json().items():
                id_match = id_field_regex.match(field)
                if id_match:
                    combined_id += value + "-"
            combined_id = combined_id[:-1]
            combined_aspace_id_clean = id_combined_regex.sub('', combined_id)
            if resource.json()["publish"] is True:
                if resource.status_code == 200:
                    export_ead = client.get("repositories/{}/resource_descriptions/{}.xml".format(repo_id, resource_id),
                                            params={"include_unpublished": False, "include_daos": True,
                                                    "numbered_cs": True, "print_pdf": False, "ead3": False})
                    filepath = str(Path(repo_folder, combined_aspace_id_clean)) + ".xml"
                    with open(filepath, "wb") as local_file:
                        local_file.write(export_ead.content)
                        local_file.close()
                        print("Exported: {}".format(combined_id))
                else:
                    print("\nThe following errors were found when exporting {}:\n{}: {}\n".format(combined_id, resource,
                                                                                                  resource.text))
        print("-" * 100)


sourcepath = input("Enter folder path for exported EADs: ")
asp_client = ASnakeClient(baseurl=as_api, username=as_un, password=as_pw)
asp_client.authorize()
export_eads(asp_client, sourcepath)
