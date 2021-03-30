from asnake.client import ASnakeClient
from secrets import *
import datetime
import json
import logging
import csv
import os


def check_aos():
    ao_instances = {}
    parent_exceptions = {}
    repos = client.get("repositories").json()
    for repo in repos:
        print("Repository: {}".format(repo["name"]))
        get_aos = client.get(repo["uri"] + "/archival_objects?all_ids=true").json()
        print(f"Total number of Archival Objects to check: {len(get_aos)}")
        logging.info(f"Total Archival Objects for {repo['name']}: {len(get_aos)}")
        for ao_id in get_aos:
            get_ao = client.get(repo["uri"] + f"/archival_objects/{ao_id}")
            ao = json.loads(get_ao.text)
            resource = client.get(ao["resource"]["ref"]).json()
            try:
                if "parent" in ao:
                    if ao["instances"]:  # if there is a top container info linked
                        for instance in ao["instances"]:
                            if "sub_container" in instance:
                                childtype = [value for field, value in instance["sub_container"].items() if "type_" in field]
                                if "folder" in childtype:  # excluding AV objects - just want children labeled folders
                                    check_parent = client.get(ao["parent"]["ref"]).json()
                                    try:
                                        if check_parent["level"] == "file" or check_parent["level"] == "item":  # exclude all series, sub-series stuff
                                            if check_parent["instances"]:
                                                for parent_instance in check_parent["instances"]:
                                                    if "sub_container" in parent_instance:
                                                        indicator_field = [field for field in parent_instance["sub_container"].keys() if "indicator_" in field]
                                                        if not indicator_field:
                                                            if check_parent["ref_id"] not in ao_instances:
                                                                print(f"{check_parent['title']}, {check_parent['ref_id']}")
                                                                if not check_parent["dates"]:
                                                                    ao_instances[check_parent["ref_id"]] = [check_parent["title"],
                                                                                                            "N/A",
                                                                                                            check_parent["uri"],
                                                                                                            resource["title"],
                                                                                                            resource["id_0"],
                                                                                                            repo["name"]
                                                                                                            ]
                                                                else:
                                                                    ao_instances[check_parent["ref_id"]] = [check_parent["title"],
                                                                                                            check_parent["dates"][0]["expression"],
                                                                                                            check_parent["uri"],
                                                                                                            resource["title"],
                                                                                                            resource["id_0"],
                                                                                                            repo["name"]]
                                            else:
                                                if check_parent["ref_id"] not in ao_instances:
                                                    print(f"{check_parent['title']}, {check_parent['ref_id']}")
                                                    if not check_parent["dates"] and not check_parent["title"]:
                                                        ao_instances[check_parent["ref_id"]] = ["N/A",
                                                                                                "N/A",
                                                                                                check_parent["uri"],
                                                                                                resource["title"],
                                                                                                resource["id_0"],
                                                                                                repo["name"]]
                                                    elif not check_parent["dates"] and check_parent["title"]:
                                                        ao_instances[check_parent["ref_id"]] = [check_parent["title"],
                                                                                                "N/A",
                                                                                                check_parent["uri"],
                                                                                                resource["title"],
                                                                                                resource["id_0"],
                                                                                                repo["name"]]
                                                    elif check_parent["dates"] and not check_parent["title"]:
                                                        ao_instances[check_parent["ref_id"]] = ["N/A",
                                                                                                check_parent["dates"][0]["expression"],
                                                                                                check_parent["uri"],
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
                                    except Exception as e:
                                        parent_exceptions[f"{check_parent['ref_id']}"] = [f"{e}",
                                                                                          f"{check_parent['uri']}",
                                                                                          f"{resource['title']}",
                                                                                          f"{resource['id_0']}",
                                                                                          f"{repo['name']}"]
            except Exception as ao_error:
                try:
                    print(f"ERROR checking archival object: {ao_error}. AO: {ao['ref_id']}, {ao['uri']}")
                    logging.error(f"ERROR checking parent_ao: {ao_error}. AO: {ao['ref_id']}, "
                                  f"{ao['uri']}, {resource['title']}, {resource['id_0']}, "
                                  f"{repo['name']}")
                except Exception as e:
                    print(f"ERROR logging exception: {e}. Archival Object Error: {ao_error}. Archival Object: {ao}")
                    logging.error(f"ERROR catching exception: {e}, Archival Object Error: {ao_error}, "
                                  f"Archival Object: {ao}")
        print("-" * 100)
    return ao_instances, parent_exceptions


def write_csv(date, mode, ao_refid, ao_title, ao_date, ao_uri, coll_title, coll_id, repo):
    with open(f"reports/{date}as_ao_errors.csv", mode=mode, newline='', encoding='utf-8') as ao_log:
        file_write = csv.writer(ao_log, delimiter=",")
        file_write.writerow([ao_refid, ao_title, ao_date, ao_uri, coll_title, coll_id, repo])
        ao_log.close()


def create_reports_folder():
    if "reports" not in os.listdir(os.getcwd()):
        folder = "reports"
        source_path = os.path.join(os.getcwd(), folder)
        os.mkdir(source_path)


def create_log_folder():
    if "logfiles" not in os.listdir(os.getcwd()):
        folder = "logfiles"
        source_path = os.path.join(os.getcwd(), folder)
        os.mkdir(source_path)


if __name__ == "__main__":
    run = True
    while run is True:
        create_reports_folder()
        create_log_folder()
        date_filename = str(datetime.date.today())
        logging.basicConfig(filename=f"logfiles/{date_filename}AS_AO_check.log")
        as_username = input("ArchivesSpace username: ")
        as_password = input("ArchivesSpace password: ")
        print(" " * 100)
        try:
            client = ASnakeClient(baseurl=as_api, username=as_username, password=as_password)
            client.authorize()
            print("Checking Archival Objects in ASpace...")
            write_csv(date_filename, "w", "AO_REFID", "AO_TITLE", "AO_DATE", "AO_URI", "COLLECTION_TITLE",
                      "COLLECTION_ID", "REPOSITORY")
            ao_instances, parent_errors = check_aos()
            for key, value in ao_instances.items():
                write_csv(date_filename, "a", key, value[0], value[1], value[2], value[3], value[4], value[5])
            for parent, error in parent_errors.items():
                logging.error(f"ERROR checking parent_ao: {error[0]}. AO: {parent}, "
                              f"{error[1]}, {error[2]}, {error[3]}, {error[4]}")
            run = False
        except Exception as e:
            print(f"Please try again. ERROR: {e}")
            logging.error(e)
