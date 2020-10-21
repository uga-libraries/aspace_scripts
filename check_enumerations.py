from asnake.client import ASnakeClient
import logging
from secrets import *

logging.basicConfig(filename="AS_enums.log", level=logging.INFO)

as_username = input("Enter your ArchivesSpace username: ")  # input("Enter your ArchivesSpace username: ")
as_password = input("Enter your ArchivesSpace password: ")  # input("Enter your ArchivesSpace password: ")
client = ASnakeClient(baseurl=as_api, username=as_username, password=as_password)
client.authorize()

need_to_delete_extents = ["copies", "linear_foot"]

extent_types = ["gigabyte(s)", "linear_feet", "box(es)", "item(s)", "volume(s)", "moving_image(s)", "folder(s)",
                "sound_recording(s)", "interview(s)", "photograph(s)", "oversize_folders", "interview", "photographs",
                "item", "minutes", "unknown", "pages", "linear_foot", "copies"]

container_types = ["box", "folder", "oversized_box", "oversized_folder", "reel", "roll", "portfolio", "item", "volume",
                   "physdesc", "electronic_records", "carton", "drawer", "cassette", "rr", "cs"]

instance_types = ["artifacts", "audio", "books", "digital_object", "graphic_materials", "maps", "microform",
                  "mixed_materials", "moving_images", "electronic_records"]

do_types = ["cartographic", "mixed_materials", "moving_image", "software_multimedia", "sound_recording", "still_image",
            "text"]

accession_res_types = ["collection", "papers", "records"]

subject_sources = ["aat", "lcsh", "local", "lcnaf"]

name_sources = ["local", "naf", "ingest"]

fa_status_terms = ["completed", "unprocessed", "in_process", "problem"]


# enumerations = client.get("/config/enumerations").json()
# for enum in enumerations:
#     print(enum["name"], enum["uri"])


def update_extents():
    new_extents = client.get("/config/enumerations/14").json()
    new_extents["values"] = []
    new_extents["enumeration_values"] = []
    aspace_extent_type = client.get("/config/enumerations/14").json()
    for extent in aspace_extent_type["enumeration_values"]:
        if extent["value"] in extent_types:
            print("{}".format(extent["value"]))
            new_extents["enumeration_values"].append(extent)
            new_extents["values"].append(extent["value"])
    update = client.post("/config/enumerations/14", json=new_extents)
    print(update.json())
    if 'error' in update.json():
        logging.info("Extents Error: {}".format(str(update.json())))
    merge_extents = merge_enums("/config/enumerations/14", "item", "item(s)")
    print(merge_extents)
    logging.info("Merging Extents results: {}".format(merge_extents))


def update_containers():
    new_container = client.get("/config/enumerations/16").json()
    new_container["values"] = []
    new_container["enumeration_values"] = []
    aspace_container_type = client.get("/config/enumerations/16").json()
    for container in aspace_container_type["enumeration_values"]:
        if container["value"] in container_types:
            print("{}".format(container["value"]))
            new_container["enumeration_values"].append(container)
            new_container["values"].append(container["value"])
    update = client.post("/config/enumerations/16", json=new_container)
    print(update.json())
    merge_containers = merge_enums("/config/enumerations/16", "unknown_item", "item")
    print(merge_containers)
    logging.info("Merging Container types: {}".format(merge_containers))


def update_instances():
    new_instances = client.get("/config/enumerations/22").json()
    new_instances["values"] = []
    new_instances["enumeration_values"] = []
    aspace_instance_type = client.get("/config/enumerations/22").json()
    for instance in aspace_instance_type["enumeration_values"]:
        if instance["value"] in instance_types:
            print("{}".format(instance["value"]))
            new_instances["enumeration_values"].append(instance)
            new_instances["values"].append(instance["value"])
    update = client.post("/config/enumerations/22", json=new_instances)
    print(update.json())
    merge_instance_values = [{"mixed_materials": ["box_oversize", "box", "folder", "item", "page", "text",
                                                  "oversize_box", "bankers_box", "folder_oversize", "volume"]},
                             {"microform": ["reel", "cartridge"]},
                             {"artifacts": ["artifact"]},
                             {"moving_images": ["moving_image"]}]
    for merge in merge_instance_values:
        for to_value, from_values in merge.items():
            for from_value in from_values:
                merge_instance_types = merge_enums("/config/enumerations/22", from_value, to_value)
                print(merge_instance_types)
                logging.info("Merging Instance types: {}".format(merge_instance_types))


def update_acc_res_types():
    new_acc_res_types = client.get("/config/enumerations/7").json()
    new_acc_res_types["values"] = []
    new_acc_res_types["enumeration_values"] = []
    aspace_acc_res_type = client.get("/config/enumerations/7").json()
    for acc_res_type in aspace_acc_res_type["enumeration_values"]:
        if acc_res_type["value"] in accession_res_types:
            print(acc_res_type["value"])
            new_acc_res_types["enumeration_values"].append(acc_res_type)
            new_acc_res_types["values"].append(acc_res_type["value"])
    update = client.post("/config/enumerations/7", json=new_acc_res_types)
    print(update.json())


def update_digital_objects():
    new_digital_object_types = client.get("/config/enumerations/12").json()
    new_digital_object_types["values"] = []
    new_digital_object_types["enumeration_values"] = []
    aspace_digital_object_types = client.get("/config/enumerations/12").json()
    for dig_obj_type in aspace_digital_object_types["enumeration_values"]:
        if dig_obj_type["value"] in do_types:
            print(dig_obj_type["value"])
            new_digital_object_types["enumeration_values"].append(dig_obj_type)
            new_digital_object_types["values"].append(dig_obj_type["value"])
    update = client.post("/config/enumerations/7", json=new_digital_object_types)
    print(update.json())


def update_subject_sources():
    new_subject_sources = client.get("/config/enumerations/23").json()
    new_subject_sources["values"] = []
    new_subject_sources["enumeration_values"] = []
    aspace_subject_sources = client.get("/config/enumerations/23").json()
    for subject_source in aspace_subject_sources["enumeration_values"]:
        if subject_source["value"] in subject_sources:
            print(subject_source["value"])
            new_subject_sources["enumeration_values"].append(subject_source)
            new_subject_sources["values"].append(subject_source["value"])
    update = client.post("/config/enumerations/23", json=new_subject_sources)
    print(update.json())
    merge_ss = merge_enums("/config/enumerations/23", "ingest", "local")
    print(merge_ss)
    logging.info(merge_ss)


def update_name_sources():
    new_name_sources = client.get("/config/enumerations/4").json()
    new_name_sources["values"] = []
    new_name_sources["enumeration_values"] = []
    aspace_name_sources = client.get("/config/enumerations/4").json()
    for name_source in aspace_name_sources["enumeration_values"]:
        if name_source["value"] in name_sources:
            print(name_source["value"])
            new_name_sources["enumeration_values"].append(name_source)
            new_name_sources["values"].append(name_source["value"])
    update = client.post("/config/enumerations/4", json=new_name_sources)
    print(update.json())
    merge_ns1 = merge_enums("/config/enumerations/4", "library_of_congress_subject_headings", "naf")
    merge_ns2 = merge_enums("/config/enumerations/4", "mediadonor", "local")
    merge_ns3 = merge_enums("/config/enumerations/4", "digital_library_of_georgia_name_database", "local")
    print(merge_ns1, merge_ns2, merge_ns3)
    logging.info("Merging Name Sources: {}, {}, {}".format(merge_ns1, merge_ns2, merge_ns3))


def update_fa_status_terms():
    new_fa_status_terms = client.get("/config/enumerations/21").json()
    new_fa_status_terms["values"] = []
    new_fa_status_terms["enumeration_values"] = []
    aspace_fa_status_terms = client.get("/config/enumerations/21").json()
    for fa_status_term in aspace_fa_status_terms["enumeration_values"]:
        if fa_status_term["value"] in fa_status_terms:
            print(fa_status_term["value"])
            new_fa_status_terms["enumeration_values"].append(fa_status_term)
            new_fa_status_terms["values"].append(fa_status_term["value"])
    update = client.post("/config/enumerations/21", json=new_fa_status_terms)
    print(update.json())


def merge_enums(enum_uri, from_val, to_val):
    merge_json = {"enum_uri": enum_uri, "from": from_val, "to": to_val}
    merge_instance = client.post("/config/enumerations/migration", json=merge_json)
    return merge_instance.json()


update_fa_status_terms()
