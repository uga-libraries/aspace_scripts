# This script removes all -'s from Russell resource IDs

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

    print("Combined_ID|Old_ID|New_ID|Status")
    repo_id = "2"
    total_changes = 0
    resources = client.get("repositories/{}/resources".format(repo_id), params={"all_ids": True}).json()
    for resource_id in resources:
        output_message = ""
        resource_data = client.get("repositories/{}/resources/{}".format(repo_id, resource_id)).json()
        no_slashes = ""
        combined_aspace_id = ""
        for field, value in resource_data.items():
            id_match = id_field_regex.match(field)
            if id_match:
                if "-" in value:
                    no_slashes = value.replace("-", "")
                    combined_aspace_id += no_slashes + "-"
                    resource_data[field] = no_slashes
                    output_message += combined_aspace_id[:-1] + "|" + value + "|" + no_slashes + "|"
                    total_changes += 1
                else:
                    combined_aspace_id += value + "-"
        if no_slashes:
            update_resource = client.post("repositories/{}/resources/{}".format(repo_id, resource_id),
                                          json = resource_data).json()
            output_message += str(update_resource)
        if output_message:
            print(output_message)
    print(f'Total Updates: {total_changes}')


asp_client = ASnakeClient(baseurl=as_api_stag, username=as_un, password=as_pw)
asp_client.authorize()
update_ids(asp_client)