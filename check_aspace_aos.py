# This script checks all archival objects in ArchivesSpace and checks to see what objects are listed as collections, as
# well as updating ms3789 to change its objects from 'collection' to 'file'
from asnake.client import ASnakeClient
from secrets import *
import json
import logging
import csv

logging.basicConfig(filename="AS_AO_check.log", level=logging.INFO)


def check_aos():
    repos = client.get("repositories").json()
    counter_total = 0
    with open("as_ao_errors.csv", mode="w") as ao_log:
        ao_log = csv.writer(ao_log)
        ao_log.writerow(["AO_TITLE", "AO_DATE", "AO_URI", "AT_ID", "COLLECTION_TITLE", "COLLECTION_ID"])
    for repo in repos:
        print("Repository: {}".format(repo["name"]))
        counter_repo = 0
        get_aos = client.get(repo["uri"] + "/archival_objects?all_ids=true").json()
        print(len(get_aos))
        logging.info("Total Archival Objects for {}: {}".format(repo["name"], len(get_aos)))
        for ao_id in get_aos:
            get_ao = client.get(repo["uri"] + "/archival_objects/{}".format(ao_id))
            ao = json.loads(get_ao.text)
            if ao["level"] == "collection":
                resource = client.get(ao["resource"]["ref"]).json()
                print(resource)
                counter_repo += 1
                counter_total += 1
                print("Item level collections count: {}".format(counter_repo))
                print(ao)
                with open("as_ao_errors.csv", mode="w") as ao_log:
                    ao_log = csv.writer(ao_log)
                    if "title" not in ao:
                        ao_log.writerow(["N/A", ao["dates"][0]["expression"], ao["uri"],
                                         ao["external_ids"][0]["external_id"], resource["title"], resource["id_0"]])
                        logging.info("Repository: {}. Title: {}. Date: {}. URI: {}. Collection: {}".format(repo["name"],
                                                                                                           "N/A",
                                                                                                           ao["dates"][0]["expression"],
                                                                                                           ao["uri"],
                                                                                                           ao["external_ids"][0]["external_id"],
                                                                                                           resource["title"]))
                    else:
                        if not ao["title"] and ao["dates"]:
                            print("1st")
                            ao_log.writerow(["N/A", ao["dates"][0]["expression"], ao["uri"],
                                             ao["external_ids"][0]["external_id"], resource["title"], resource["id_0"]])
                            logging.info("Repository: {}. Title: {}. Date: {}. URI: {}. Collection: {}".format(repo["name"],
                                                                                                               "N/A",
                                                                                                               ao["dates"][0]["expression"],
                                                                                                               ao["uri"],
                                                                                                               ao["external_ids"][0]["external_id"],
                                                                                                               resource["title"]))
                        elif ao["title"] and not ao["dates"]:
                            print("2nd")
                            ao_log.writerow([ao["title"], "N/A", ao["uri"], ao["external_ids"][0]["external_id"],
                                             resource["title"], resource["id_0"]])
                            logging.info("Repository: {}. Title: {}. Date: {}. URI: {}. Collection: {}".format(repo["name"],
                                                                                                               ao["title"],
                                                                                                               "N/A",
                                                                                                               ao["uri"],
                                                                                                               ao["external_ids"][0]["external_id"],
                                                                                                               resource["title"]))
                        else:
                            print("3rd")
                            ao_log.writerow([ao["title"], ao["dates"][0]["expression"], ao["uri"],
                                             ao["external_ids"][0]["external_id"], resource["title"], resource["id_0"]])
                            logging.info("Repository: {}. Title: {}. Date: {}. URI: {}. Collection: {}".format(repo["name"],
                                                                                                               ao["title"],
                                                                                                               ao["dates"][0]["expression"],
                                                                                                               ao["uri"],
                                                                                                               ao["external_ids"][0]["external_id"],
                                                                                                               resource["title"]))
        print("-" * 100)
    print("Total Item level collections: {}".format(counter_total))
    print("-"*100)


def update_ms3789():
    arch_objs = []
    counter = 0
    resource = client.get("/repositories/4/resources/4312/tree").json()
    for arch_obj in resource["children"]:
        if arch_obj["level"] == "collection":
            counter += 1
            arch_objs.append(arch_obj)
    for arch_obj in arch_objs:
        get_ao = client.get(arch_obj["record_uri"])
        ao = json.loads(get_ao.text)
        if ao["level"] == "collection":
            ao["level"] = "file"
            update_aos = client.post(arch_obj["record_uri"], json=ao).json()
            print(update_aos)


as_username = input("ArchivesSpace username: ")
as_password = input("ArchivesSpace password: ")
print(" " * 100)

client = ASnakeClient(baseurl=as_api, username=as_username, password=as_password)
client.authorize()
run = True
while run is True:
    run_check_aos = input("Run check_aos? Y/N")
    run_update_ms3789 = input("Update ms3789? Y/N")
    if run_check_aos == "Y" and run_update_ms3789 == "N":
        print("Checking Archival Objects in ASpace...")
        check_aos()
        run = False
    elif run_check_aos == "N" and run_update_ms3789 == "Y":
        print("Updating ms3789...")
        update_ms3789()
        run = False
    elif run_check_aos == "Y" and run_update_ms3789 == "Y":
        print("Checking Archival Objects in ASpace...")
        check_aos()
        print("Updating ms3789...", end='', flush=True)
        update_ms3789()
        print("Done")
        run = False
    elif run_check_aos == "N" and run_update_ms3789 == "N":
        run = False
    else:
        print("Bad input. Please try again")
