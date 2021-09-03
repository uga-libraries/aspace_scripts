# This script publishes all digital object file versions
from asnake.client import ASnakeClient
from secrets import *

as_username = input("Enter your ArchivesSpace username: ")  # input("Enter your ArchivesSpace username: ")
as_password = input("Enter your ArchivesSpace password: ")  # input("Enter your ArchivesSpace password: ")
client = ASnakeClient(baseurl=as_api, username=as_username, password=as_password)
client.authorize()


def publish_do_fvs():
    repos = client.get("repositories").json()
    for repo in repos:
        print(repo["name"])
        repo_id = repo["uri"].split("/")[2]
        response_dos = client.get('repositories/{}/digital_objects'.format(repo_id), params={"all_ids": True})
        all_dos = list(response_dos.json())
        for do_id in all_dos:
            update_do = client.post('repositories/{}/digital_objects/{}/publish'.format(repo_id, do_id))
            print(update_do.text)


publish_do_fvs()
