from asnake.client import ASnakeClient
from secrets import *
import datetime
import json
import logging
import csv


def check_aos(date):
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
                if "file" == ao["level"]:
                    if "parent" in ao:
                        check_parent = client.get(ao["parent"]["ref"]).json()
                        resource = client.get(ao["resource"]["ref"]).json()
                        if check_parent["level"] == "file":
                            if check_parent["instances"]:
                                if check_parent["instances"][0]["sub_container"]:
                                    if "indicactor_" not in check_parent["instances"][0]["sub_container"]:
                                        try:
                                            if not ao["dates"]:
                                                write_csv(date, "a", ao["title"], "N/A", ao["uri"],
                                                          resource["title"], resource["id_0"], repo["name"])
                                                logging.info(
                                                    "Repository: {}. Title: {}. Date: {}. URI: {}. Collection: {}".format(
                                                        repo["name"],
                                                        ao["title"],
                                                        "N/A",
                                                        ao["uri"],
                                                        resource["title"]))
                                            else:
                                                write_csv(date, "a", ao["title"], ao["dates"][0]["expression"],
                                                          ao["uri"],
                                                          resource["title"], resource["id_0"], repo["name"])
                                                logging.info(
                                                    "Repository: {}. Title: {}. Date: {}. URI: {}. Collection: {}".format(
                                                        repo["name"],
                                                        ao["title"],
                                                        ao["dates"][0]["expression"],
                                                        ao["uri"],
                                                        resource["title"]))
                                            print(ao["title"])
                                        except Exception as e:
                                            print(f"Error writing archival object to log: {e}; {ao}")
                                            logging.error(f"ERROR: {e}; {ao}")
                            else:
                                try:
                                    if not ao["dates"]:
                                        write_csv(date, "a", ao["title"], "N/A", ao["uri"],
                                                  resource["title"], resource["id_0"], repo["name"])
                                        logging.info(
                                            "Repository: {}. Title: {}. Date: {}. URI: {}. Collection: {}".format(
                                                repo["name"],
                                                ao["title"],
                                                "N/A",
                                                ao["uri"],
                                                resource["title"]))
                                    else:
                                        write_csv(date, "a", ao["title"], ao["dates"][0]["expression"], ao["uri"],
                                                  resource["title"], resource["id_0"], repo["name"])
                                        logging.info(
                                            "Repository: {}. Title: {}. Date: {}. URI: {}. Collection: {}".format(
                                                repo["name"],
                                                ao["title"],
                                                ao["dates"][0]["expression"],
                                                ao["uri"],
                                                resource["title"]))
                                    print(ao["title"])
                                except Exception as e:
                                    print(f"Error writing archival object to log: {e}; {ao}")
                                    logging.error(f"ERROR: {e}; {ao}")
        print("-" * 100)


def write_csv(date, mode, ao_title, ao_date, ao_uri, coll_title, coll_id, repo):
    with open(f"{date}as_ao_errors.csv", mode=mode, newline='', encoding='utf-8') as ao_log:
        file_write = csv.writer(ao_log, delimiter=",")
        file_write.writerow([ao_title, ao_date, ao_uri, coll_title, coll_id, repo])
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
        write_csv(date_filename, "w", "AO_TITLE", "AO_DATE", "AO_URI", "COLLECTION_TITLE", "COLLECTION_ID",
                  "REPOSITORY")
        check_aos(date_filename)
        run = False
    except Exception as e:
        print(f"Please try again. ERROR: {e}")
        logging.error(e)
