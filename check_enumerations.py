from asnake.client import ASnakeClient
from secrets import *

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

enumerations = client.get("/config/enumerations").json()
for enum in enumerations:
    print(enum["name"], enum["uri"])


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
