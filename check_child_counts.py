import re
import json
import csv
from secrets import *
from asnake.aspace import ASpace
from asnake.client import ASnakeClient

id_field_regex = re.compile(r"(^id_+\d)")
id_combined_regex = re.compile(r'[\W_]+', re.UNICODE)

aspace = ASpace(baseurl=as_api, username=as_un, password=as_pw)
client = ASnakeClient(baseurl=as_api, username=as_un, password=as_pw)
client.authorize()


def check_child_counts(tree_info, child_counts, root_uri, aspace_coll_id, client, repository, top_level=False):
    if tree_info["child_count"] >= 1000 and tree_info["uri"] not in child_counts:
        child_counts[f"{tree_info['uri']}"] = (tree_info["title"], tree_info["child_count"], tree_info["level"],
                                               aspace_coll_id, repository)
        print(aspace_coll_id)
    if "precomputed_waypoints" in tree_info and tree_info["child_count"] != 0:
        if top_level is True:
            waypoint_key = ""
        else:
            waypoint_key = tree_info["uri"]
        for waypoint_num, waypoint_info in tree_info["precomputed_waypoints"][waypoint_key].items():
            for child in waypoint_info:
                if child["child_count"] >= 1000:
                    child_counts[f'{child["uri"]}'] = (child["title"], child["child_count"], child["level"],
                                                       aspace_coll_id)
                children = client.get(root_uri + "/tree/node", params={"node_uri": child["uri"],
                                                                       "published_only": True}).json()
                check_child_counts(children, child_counts, root_uri, aspace_coll_id, client, repository,
                                   top_level=False)
    return child_counts


child_counts = {}
repos = client.get("repositories").json()
for repo in repos:
    print(repo["name"] + "\n")
    repo_id = repo["uri"].split("/")[2]
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
                root_uri = f'/repositories/{repo_id}/resources/{resource_id}'
                tree_info = client.get(f'{root_uri}/tree/root').json()
                print(combined_id)
                child_counts = check_child_counts(tree_info, child_counts, root_uri, combined_id, client, repo["name"],
                                                  top_level=True)

new_dict = json.dumps(child_counts)
load_dict = json.loads(new_dict)
with open("data/check_child_count.csv", "w", encoding="utf8", newline='') as file:
    writer = csv.writer(file)
    for child, data in load_dict.items():
        fields = [str(child), str(data[0]), str(data[1]), str(data[2]), str(data[3], str(data[4]))]
        writer.writerow(fields)
    file.close()
