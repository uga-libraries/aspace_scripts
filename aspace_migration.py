from asnake.client import ASnakeClient
from secrets import *
from logging.handlers import TimedRotatingFileHandler
import re
import logging
import sys

id_field_regex = re.compile(r"(^id_+\d)")
FORMATTER = logging.Formatter("%(asctime)s — %(name)s — %(levelname)s — %(message)s")
LOG_FILE = "aspace_migration.log"

as_username = as_un
as_password = as_pw
client = ASnakeClient(baseurl=as_api, username=as_username, password=as_password)
client.authorize()

need_to_delete_extents = ["copies", "linear_foot"]
extent_types = ["gigabyte(s)", "linear_feet", "box(es)", "item(s)", "volume(s)", "moving_image(s)", "folder(s)",
                "sound_recording(s)", "interview(s)", "photograph(s)", "oversize_folders", "interview", "photographs",
                "item", "minutes", "unknown", "pages", "linear_foot", "copies"]
need_to_delete_containers = ["unknown_item"]
container_types = ["box", "folder", "oversized_box", "oversized_folder", "reel", "roll", "portfolio", "item", "volume",
                   "physdesc", "electronic_records", "carton", "drawer", "cassette", "rr", "cs"]
need_to_delete_instance = ["accession"]  # Russell: http://aspace-staging-uga.galib.uga.edu:8080/search?aq=%7B%22query%22%3A%7B%22op%22%3A%22OR%22%2C%22subqueries%22%3A%5B%7B%22field%22%3A%22instance_type_enum_s%22%2C%22value%22%3A%22accession%22%2C%22negated%22%3Afalse%2C%22literal%22%3Atrue%2C%22jsonmodel_type%22%3A%22field_query%22%7D%5D%2C%22jsonmodel_type%22%3A%22boolean_query%22%7D%2C%22jsonmodel_type%22%3A%22advanced_query%22%7D
instance_types = ["artifacts", "audio", "books", "digital_object", "graphic_materials", "maps", "microform",
                  "mixed_materials", "moving_images", "electronic_records"]
do_types = ["cartographic", "mixed_materials", "moving_image", "software_multimedia", "sound_recording", "still_image",
            "text"]
need_to_delete_accession = ["letter"]  # Russell: http://aspace-staging-uga.galib.uga.edu:8080/search?aq=%7B%22query%22%3A%7B%22op%22%3A%22OR%22%2C%22subqueries%22%3A%5B%7B%22field%22%3A%22resource_type_enum_s%22%2C%22value%22%3A%22letter%22%2C%22negated%22%3Afalse%2C%22literal%22%3Atrue%2C%22jsonmodel_type%22%3A%22field_query%22%7D%5D%2C%22jsonmodel_type%22%3A%22boolean_query%22%7D%2C%22jsonmodel_type%22%3A%22advanced_query%22%7D
accession_res_types = ["collection", "papers", "records"]
need_to_delete_subject = ["gmgpc"]  # Hargrett: http://aspace-staging-uga.galib.uga.edu:8080/search?aq=%7B%22query%22%3A%7B%22op%22%3A%22OR%22%2C%22subqueries%22%3A%5B%7B%22field%22%3A%22source_enum_s%22%2C%22value%22%3A%22gmgpc%22%2C%22negated%22%3Afalse%2C%22literal%22%3Atrue%2C%22jsonmodel_type%22%3A%22field_query%22%7D%5D%2C%22jsonmodel_type%22%3A%22boolean_query%22%7D%2C%22jsonmodel_type%22%3A%22advanced_query%22%7D
subject_sources = ["aat", "lcsh", "local", "lcnaf"]
need_to_delete_name = ["library_of_congress_subject_headings"]
name_sources = ["local", "naf", "ingest"]
fa_status_terms = ["completed", "unprocessed", "in_process", "problem"]


def get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    return console_handler


def get_file_handler():
    file_handler = TimedRotatingFileHandler(LOG_FILE, when='midnight')
    file_handler.setFormatter(FORMATTER)
    return file_handler


def get_logger(logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)  # better to have too much log than not enough
    logger.addHandler(get_console_handler())
    logger.addHandler(get_file_handler())
    logger.propagate = False
    return logger


def update_extents(logger):
    merge_extents = merge_enums("/config/enumerations/14", "item", "item(s)")
    if 'error' in merge_extents:
        logger.error("Extent Types: Merging error: {}".format(merge_extents))
    else:
        print("Extent Types: Merging: {}".format(merge_extents))
    new_extents = client.get("/config/enumerations/14").json()
    new_extents["values"] = []
    new_extents["enumeration_values"] = []
    aspace_extent_type = client.get("/config/enumerations/14").json()
    for extent in aspace_extent_type["enumeration_values"]:
        if extent["value"] in extent_types:
            new_extents["enumeration_values"].append(extent)
            new_extents["values"].append(extent["value"])
    update = client.post("/config/enumerations/14", json=new_extents)
    if 'error' in update.json():
        logger.error("Extent Types: Updating error: {}".format(update.json()))
    else:
        print("Extent Types: Updating: {}".format(update.json()))


def update_containers(logger):
    merge_containers = merge_enums("/config/enumerations/16", "unknown_item", "item")
    if 'error' in merge_containers:
        logger.error("Container Types: Merging error: {}".format(merge_containers))
    else:
        print("Container Types: Merging: {}".format(merge_containers))
    new_container = client.get("/config/enumerations/16").json()
    new_container["values"] = []
    new_container["enumeration_values"] = []
    aspace_container_type = client.get("/config/enumerations/16").json()
    for container in aspace_container_type["enumeration_values"]:
        if container["value"] in container_types:
            new_container["enumeration_values"].append(container)
            new_container["values"].append(container["value"])
    update = client.post("/config/enumerations/16", json=new_container)
    if 'error' in update.json():
        logger.error("Container Types: Updating error: {}".format(update.json()))
    else:
        print("Container types: Updating: {}".format(update.json()))


def update_instances(logger):
    merge_instance_values = [{"mixed_materials": ["box_oversize", "box", "folder", "item", "page", "text",
                                                  "oversize_box", "bankers_box", "folder_oversize", "volume"]},
                             {"microform": ["reel", "cartridge"]},
                             {"artifacts": ["artifact"]},
                             {"moving_images": ["moving_image"]}]
    for merge in merge_instance_values:
        for to_value, from_values in merge.items():
            for from_value in from_values:
                merge_instance_types = merge_enums("/config/enumerations/22", from_value, to_value)
                if 'error' in merge_instance_types:
                    logger.error("Instance types: Merging error: {}".format(merge_instance_types))
                else:
                    print("Instance Types: Merging: {}".format(merge_instance_types))
    new_instances = client.get("/config/enumerations/22").json()
    new_instances["values"] = []
    new_instances["enumeration_values"] = []
    aspace_instance_type = client.get("/config/enumerations/22").json()
    for instance in aspace_instance_type["enumeration_values"]:
        if instance["value"] in instance_types:
            new_instances["enumeration_values"].append(instance)
            new_instances["values"].append(instance["value"])
    update = client.post("/config/enumerations/22", json=new_instances)
    if 'error' in update.json():
        logger.error("Instance types: Updating error: {}".format(update.json()))
    else:
        print("Instance Types: Updating: {}".format(update.json()))


def update_acc_res_types(logger):
    new_acc_res_types = client.get("/config/enumerations/7").json()
    new_acc_res_types["values"] = []
    new_acc_res_types["enumeration_values"] = []
    aspace_acc_res_type = client.get("/config/enumerations/7").json()
    for acc_res_type in aspace_acc_res_type["enumeration_values"]:
        if acc_res_type["value"] in accession_res_types:
            new_acc_res_types["enumeration_values"].append(acc_res_type)
            new_acc_res_types["values"].append(acc_res_type["value"])
    update = client.post("/config/enumerations/7", json=new_acc_res_types)
    if 'error' in update.json():
        logger.error("Accession Resource Type: Updating error: {}".format(update.json()))
    else:
        print("Accession Resource Types: Updating: {}".format(update.json()))


def update_digital_objects(logger):
    new_digital_object_types = client.get("/config/enumerations/12").json()
    new_digital_object_types["values"] = []
    new_digital_object_types["enumeration_values"] = []
    aspace_digital_object_types = client.get("/config/enumerations/12").json()
    for dig_obj_type in aspace_digital_object_types["enumeration_values"]:
        if dig_obj_type["value"] in do_types:
            new_digital_object_types["enumeration_values"].append(dig_obj_type)
            new_digital_object_types["values"].append(dig_obj_type["value"])
    update = client.post("/config/enumerations/7", json=new_digital_object_types)
    if 'error' in update.json():
        logger.error("Digital Object Types: Updating error: {}".format(update.json()))
    else:
        print("Digital Object Types: Updating: {}".format(update.json()))


def update_subject_sources(logger):
    merge_ss = merge_enums("/config/enumerations/23", "ingest", "local")
    if 'error' in merge_ss:
        logger.error("Subject Sources: Merging error: {}".format(merge_ss))
    else:
        print("Subject Sources Types: Merging: {}".format(merge_ss))
    new_subject_sources = client.get("/config/enumerations/23").json()
    new_subject_sources["values"] = []
    new_subject_sources["enumeration_values"] = []
    aspace_subject_sources = client.get("/config/enumerations/23").json()
    for subject_source in aspace_subject_sources["enumeration_values"]:
        if subject_source["value"] in subject_sources:
            new_subject_sources["enumeration_values"].append(subject_source)
            new_subject_sources["values"].append(subject_source["value"])
    update = client.post("/config/enumerations/23", json=new_subject_sources)
    if 'error' in update.json():
        logger.error("Subject Sources Types: Updating error: {}".format(update.json()))
    else:
        print("Subject Sources: Updating: {}".format(update.json()))


def update_name_sources(logger):
    merge_ns1 = merge_enums("/config/enumerations/4", "library_of_congress_subject_headings", "naf")
    merge_ns2 = merge_enums("/config/enumerations/4", "mediadonor", "local")
    merge_ns3 = merge_enums("/config/enumerations/4", "digital_library_of_georgia_name_database", "local")
    if 'error' in merge_ns1:
        logger.error("Name Sources: Merging error: {}".format(merge_ns1))
    else:
        print("Name Sources: Merging: {}".format(merge_ns1))
    if 'error' in merge_ns2:
        logger.error("Name Sources: Merging error: {}".format(merge_ns2))
    else:
        print("Name Sources: Merging: {}".format(merge_ns2))
    if 'error' in merge_ns3:
        logger.error("Name Sources: Merging error: {}".format(merge_ns3))
    else:
        print("Name Sources: Merging: {}".format(merge_ns3))
    new_name_sources = client.get("/config/enumerations/4").json()
    new_name_sources["values"] = []
    new_name_sources["enumeration_values"] = []
    aspace_name_sources = client.get("/config/enumerations/4").json()
    for name_source in aspace_name_sources["enumeration_values"]:
        if name_source["value"] in name_sources:
            new_name_sources["enumeration_values"].append(name_source)
            new_name_sources["values"].append(name_source["value"])
    update = client.post("/config/enumerations/4", json=new_name_sources)
    if 'error' in update.json():
        logger.error("Name Sources: Updating error: {}".format(update.json()))
    else:
        print("Name Sources: Updating: {}".format(update.json()))


def update_fa_status_terms(logger):
    new_fa_status_terms = client.get("/config/enumerations/21").json()
    new_fa_status_terms["values"] = []
    new_fa_status_terms["enumeration_values"] = []
    aspace_fa_status_terms = client.get("/config/enumerations/21").json()
    for fa_status_term in aspace_fa_status_terms["enumeration_values"]:
        if fa_status_term["value"] in fa_status_terms:
            new_fa_status_terms["enumeration_values"].append(fa_status_term)
            new_fa_status_terms["values"].append(fa_status_term["value"])
    update = client.post("/config/enumerations/21", json=new_fa_status_terms)
    if 'error' in update.json():
        logger.error("Finding Aid Status Terms: Updating error: {}".format(update.json()))
    else:
        print("Finding Aid Status Terms: Updating: {}".format(update.json()))


def merge_enums(enum_uri, from_val, to_val):
    merge_json = {"enum_uri": enum_uri, "from": from_val, "to": to_val}
    merge_instance = client.post("/config/enumerations/migration", json=merge_json)
    return merge_instance.json()


def unpublish_records(logger):
    repos = client.get("repositories").json()
    print("Unpublishing Closed Records")
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
                print("Unpublishing {}".format(combined_id))
                all_uris = client.get("repositories/{}/resources/{}/ordered_records".format(repo_id,
                                                                                            resource_id)).json()
                for uri in all_uris["uris"]:
                    resource_ao = client.get(uri["ref"]).json()
                    resource_ao["publish"] = False
                    update_resource_ao = client.post(uri["ref"], json=resource_ao)
                    if "error" in update_resource_ao.json():
                        logger.error("Unpublishing Resource/AO: {}\nError: {}".format(uri["ref"],
                                                                                      update_resource_ao.json()))
        print("-"*100)


def publish_do_fvs(logger):
    repos = client.get("repositories").json()
    print("Publishing Digital Object File Versions")
    for repo in repos:
        print(repo["name"])
        repo_id = repo["uri"].split("/")[2]
        response_dos = client.get('repositories/{}/digital_objects'.format(repo_id), params={"all_ids": True})
        all_dos = list(response_dos.json())
        for do_id in all_dos:
            update_do = client.post('repositories/{}/digital_objects/{}/publish'.format(repo_id, do_id))
            if 'error' in update_do:
                logger.error("Digital Object File Version: Publishing error: {}".format(update_do))
            else:
                print("Digital Object File Version: Publishing: {}".format(update_do.text))
        print("-"*100)


def delete_users(logger):
    print("Deleting tgraham and mcalists from ArchivesSpace")
    users = client.get("users", params={"all_ids": True}).json()
    for user in users:
        user_info = client.get("users/{}".format(str(user))).json()
        if user_info["username"] == "tgraham" or user_info["username"] == "mcalists":
            print(user_info)
            user_uri = user_info["uri"]
            delete_user = client.delete(user_uri).json()
            if 'error' in delete_user:
                logger.error("Deleting user failed: {}, User: {}".format(delete_user, user_info["username"]))
            else:
                print("Deleting user completed: {}, User: {}".format(delete_user, user_info["username"]))
    print("-" * 100)


def delete_repository(logger):
    print("Deleting UGA repository from ArchivesSpace")
    repos = client.get("repositories").json()
    for repo in repos:
        if repo["name"] == "UGA Libraries":
            print(repo)
            delete_repo = client.delete(repo["uri"]).json()
            if 'error' in delete_repo:
                logger.error("Deleting repository failed: {}, Repo: {}".format(delete_repo, repo["name"]))
            else:
                print("Deleting repository completed: {}, Repo: {}".format(delete_repo, repo["name"]))
    print("-" * 100)


def update_rbrl462(logger):
    print("Deleting 'af' Archival Object from RBRL/462")
    repos = client.get("repositories").json()
    for repo in repos:
        if repo["name"] == "Richard B. Russell Library for Political Research and Studies":
            resources = client.get(repo["uri"] + "/resources", params={"all_ids": True}).json()
            for resource in resources:
                resource_info = client.get(repo["uri"] + "/resources/{}".format(str(resource))).json()
                if resource_info["id_0"] == "RBRL/462":
                    res_tree = client.get(resource_info["tree"]["ref"]).json()
                    # res_tree = client.get("/repositories/2/resources/1124/tree").json()
                    for series in res_tree["children"]:
                        if series["title"] == "Series 4: Research Files, 2005-2019":
                            for subseries in series["children"]:
                                if subseries["title"] == "Subseries B. Journal/Archive Analysis , 1975-2019":
                                    for arch_obj in subseries["children"]:
                                        if arch_obj["title"] == "af\n":
                                            delete_arch_obj = client.delete(arch_obj["record_uri"]).json()
                                            if 'error' in delete_arch_obj:
                                                logger.error(
                                                    "Deleting repository failed: {}, Repo: {}".format(delete_arch_obj,
                                                                                                      arch_obj["title"])
                                                            )
                                            else:
                                                print("Deleting 'af' in RBRL/462 completed: {}, "
                                                      "URI: {}".format(delete_arch_obj, arch_obj["record_uri"]))
    print("-" * 100)


def update_ms1(logger):
    print("Moving Archival Objects in ms1")
    ledgers_series = ""
    position_num = 1
    repos = client.get("repositories").json()
    for repo in repos:
        if repo["name"] == "Hargrett Library":
            resources = client.get(repo["uri"] + "/resources", params={"all_ids": True}).json()
            for resource in resources:
                resource_info = client.get(repo["uri"] + "/resources/{}".format(str(resource))).json()
                if resource_info["id_0"] == "ms1":
                    res_tree = client.get(resource_info["tree"]["ref"]).json()
                    print(res_tree)
                    for series in res_tree["children"]:
                        if series["title"] == "11. Ledgers":
                            ledgers_series = series["record_uri"]
                        elif series["level"] == "file":
                            if "Ledger" in series["title"]:
                                print(series["title"])
                                move_ao = client.post(ledgers_series + "/accept_children",
                                                      params={"children": [series["record_uri"]],
                                                              "position": position_num}).json()
                                position_num += 1
                                if 'error' in move_ao:
                                    logger.error("Moving Archival Objects in ms1 error: {}, "
                                                 "Archival Object: {}".format(move_ao, series["title"]))
                                else:
                                    print("Moving {} to {} - Status: {}".format(series["title"], ledgers_series,
                                                                                move_ao))
                    print("-" * 100)
                    break


def update_ms3265(logger):
    print("Moving Archival Objects in ms3265")
    misc_series = ""
    position_num = 1
    repos = client.get("repositories").json()
    for repo in repos:
        if repo["name"] == "Hargrett Library":
            resources = client.get(repo["uri"] + "/resources", params={"all_ids": True}).json()
            for resource in resources:
                resource_info = client.get(repo["uri"] + "/resources/{}".format(str(resource))).json()
                if resource_info["id_0"] == "ms3265":
                    res_tree = client.get(resource_info["tree"]["ref"]).json()
                    # res_tree = client.get("/repositories/4/resources/3941/tree").json()
                    for series in res_tree["children"]:
                        if series["title"] == "3. Financials":
                            series["level"] = "series"
                            series["resource"] = {"ref": res_tree["record_uri"]}
                            series["lock_version"] = 0
                            update_financials = client.post(series["record_uri"], json=series).json()
                            if 'error' in update_financials:
                                logger.error("Updating {}, Error: {}, Archival Object: {}".format(series["title"],
                                                                                                  update_financials,
                                                                                                  series["title"]))
                            else:
                                print("Updating Series: {}, Message: {}".format(series["title"], update_financials))
                        elif series["title"] == "5. Miscellaneous":
                            misc_series = series["record_uri"]
                        elif series["level"] == "file":
                            move_ao = client.post(misc_series + "/accept_children",
                                                  params={"children": [series["record_uri"]],
                                                          "position": position_num}).json()
                            position_num += 1
                            if 'error' in move_ao:
                                logger.error("Moving Archival Objects in ms1 error: {}, "
                                             "Archival Object: {}".format(move_ao, series["title"]))
                            else:
                                print("Moving {} to {} - Status: {}".format(series["title"], misc_series, move_ao))
                    print("-" * 100)
                    break


def clean_aspace():
    logger = get_logger("__name__")
    update_extents(logger)
    update_containers(logger)
    update_instances(logger)
    update_acc_res_types(logger)
    update_digital_objects(logger)
    update_subject_sources(logger)
    update_name_sources(logger)
    update_fa_status_terms(logger)
    unpublish_records(logger)
    publish_do_fvs(logger)
    delete_users(logger)
    delete_repository(logger)
    update_rbrl462(logger)
    update_ms1(logger)
    update_ms3265(logger)


clean_aspace()
