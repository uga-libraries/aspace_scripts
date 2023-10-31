# This script removes all /'s from Russell resource IDs

import re
from secrets import *
from asnake.client import ASnakeClient

id_field_regex = re.compile(r"(^id_+\d)")
id_combined_regex = re.compile(r'[\W_]+', re.UNICODE)


def update_ids(client):
    """

    Args:
        client: ArchivesSnake client to connect to ArchivesSpace

    Returns:
        None
    """

    repo_id = "2"
    resources = client.get("repositories/{}/resources".format(repo_id), params={"all_ids": True}).json()
    for resource_id in resources:
        resource_data = client.get("repositories/{}/resources/{}".format(repo_id, resource_id)).json()
        no_slashes = ""
        combined_aspace_id = ""
        for field, value in resource_data.items():
            id_match = id_field_regex.match(field)
            if id_match:
                if "/" in value:
                    no_slashes = value.replace("/", "-")
                    combined_aspace_id += no_slashes + "-"
                    resource_data[field] = no_slashes
                else:
                    combined_aspace_id += value + "-"
        if no_slashes:
            print(combined_aspace_id[:-1])
            update_resource = client.post("repositories/{}/resources/{}".format(repo_id, resource_id),
                                          json = resource_data).json()
            print(update_resource)
            print("-" * 100)


asp_client = ASnakeClient(baseurl=as_api, username=as_un, password=as_pw)
asp_client.authorize()
update_ids(asp_client)