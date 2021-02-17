import csv
from secrets import *
from asnake.client import ASnakeClient


def write_csv(mode, uri, title, date, box_num, child_type, child_indicator):
    with open("ua06_unknowns.csv", mode=mode, newline='') as invalid_links:
        file_write = csv.writer(invalid_links, delimiter=",")
        file_write.writerow([uri, title, date, box_num, child_type, child_indicator])
        invalid_links.close()


def check_children(children, cont_count):
    count = cont_count
    if children:
        for child in children:
            archival_object = client.get(child["record_uri"]).json()
            if "instances" in archival_object.keys():
                instance_count = 0
                for instance in archival_object["instances"]:
                    unknowns = check_instances(instance, archival_object, instance_count)
                    instance_count += 1
                    if unknowns > 0:
                        count += unknowns
            if "children" in child.keys():
                count = check_children(child["children"], count)
    return count


def check_instances(instance, archival_object, cont_count=0):
    if "sub_container" in instance.keys():
        for key, value in instance["sub_container"].items():
            if "indicator_" in key:
                if "unknown container" == value:
                    print(archival_object)
                    top_container = client.get(instance["sub_container"]["top_container"]["ref"]).json()
                    write_csv("a", archival_object["uri"], archival_object["title"],
                              archival_object["dates"][0]["expression"], "Box {}".format(top_container["indicator"]),
                              instance["sub_container"]["type_2"], value)
                    cont_count += 1
        return cont_count


client = ASnakeClient(baseurl=as_api, username=as_un, password=as_pw)
client.authorize()
ua97_090_uri = "/repositories/5/resources/5071"

write_csv("w", "URI", "Title", "Date", "Box Number", "Child Type", "Child Indicator")
resource_info = client.get(ua97_090_uri).json()
res_tree = client.get(resource_info["tree"]["ref"]).json()
if "children" in res_tree.keys():
    print(resource_info["title"])
    unknowns = check_children(res_tree["children"], 0)
    print("Total unknown containers = {}".format(str(unknowns)))
    print("\n")
    print("-" * 100)
