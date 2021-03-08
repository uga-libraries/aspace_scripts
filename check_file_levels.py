from asnake.client import ASnakeClient
from secrets import *
import datetime
import json
import logging
import csv


def check_aos():
    ao_instances = {}
    repos = client.get("repositories").json()
    for repo in repos:
        print("Repository: {}".format(repo["name"]))
        get_aos = client.get(repo["uri"] + "/archival_objects?all_ids=true").json()
        print(f"Total number of Archival Objects to check: {len(get_aos)}")
        logging.info(f"Total Archival Objects for {repo['name']}: {len(get_aos)}")
        for ao_id in get_aos:
            get_ao = client.get(repo["uri"] + f"/archival_objects/{ao_id}")
            ao = json.loads(get_ao.text)
            if "level" in ao:
                if "file" == ao["level"] or "item" == ao["level"]:
                    if "parent" in ao:
                        check_parent = client.get(ao["parent"]["ref"]).json()
                        resource = client.get(ao["resource"]["ref"]).json()
                        try:
                            if check_parent["level"] == "file" or check_parent["level"] == "item":
                                if check_parent["instances"]:
                                    if check_parent["instances"][0]["sub_container"]:
                                        indicator_field = [field for field in check_parent["instances"][0]["sub_container"].keys() if "indicator_" in field]
                                        if not indicator_field:
                                            if check_parent["ref_id"] not in ao_instances:
                                                print(check_parent["title"], check_parent["ref_id"])
                                                if not check_parent["dates"]:
                                                    ao_instances[check_parent["ref_id"]] = [check_parent["title"],
                                                                                            "N/A", check_parent["uri"],
                                                                                            resource["title"],
                                                                                            resource["id_0"],
                                                                                            repo["name"]]
                                                else:
                                                    ao_instances[check_parent["ref_id"]] = [check_parent["title"],
                                                                                            check_parent["dates"][0]["expression"],
                                                                                            check_parent["uri"],
                                                                                            resource["title"],
                                                                                            resource["id_0"],
                                                                                            repo["name"]]
                                else:
                                    if check_parent["ref_id"] not in ao_instances:
                                        print(check_parent["title"])
                                        if not check_parent["dates"]:
                                            ao_instances[check_parent["ref_id"]] = [check_parent["title"], "N/A",
                                                                                    check_parent["uri"],
                                                                                    resource["title"],
                                                                                    resource["id_0"], repo["name"]]
                                        else:
                                            ao_instances[check_parent["ref_id"]] = [check_parent["title"],
                                                                                    check_parent["dates"][0]["expression"],
                                                                                    check_parent["uri"],
                                                                                    resource["title"], resource["id_0"],
                                                                                    repo["name"]]
                        except Exception as e:
                            logging.error(f"ERROR checking parent_ao: {e}. AO: {check_parent['title']}, "
                                          f"{check_parent['uri']}, {resource['title']}, {resource['id_0']}, "
                                          f"{repo['name']}")
        print("-" * 100)
    return ao_instances


def write_csv(date, mode, ao_refid, ao_title, ao_date, ao_uri, coll_title, coll_id, repo):
    with open(f"{date}as_ao_errors.csv", mode=mode, newline='', encoding='utf-8') as ao_log:
        file_write = csv.writer(ao_log, delimiter=",")
        file_write.writerow([ao_refid, ao_title, ao_date, ao_uri, coll_title, coll_id, repo])
        ao_log.close()


run = True
while run is True:
    date_filename = str(datetime.date.today())
    logging.basicConfig(filename=f"{date_filename}AS_AO_check.log")
    as_username = input("ArchivesSpace username: ")
    as_password = input("ArchivesSpace password: ")
    print(" " * 100)
    try:
        client = ASnakeClient(baseurl=as_api, username=as_username, password=as_password)
        client.authorize()
        print("Checking Archival Objects in ASpace...")
        write_csv(date_filename, "w", "AO_REFID", "AO_TITLE", "AO_DATE", "AO_URI", "COLLECTION_TITLE", "COLLECTION_ID",
                  "REPOSITORY")
        ao_instances = check_aos()
        for key, value in ao_instances.items():
            write_csv(date_filename, "a", key, value[0], value[1], value[2], value[3], value[4], value[5])
        run = False
    except Exception as e:
        print(f"Please try again. ERROR: {e}")
        logging.error(e)
