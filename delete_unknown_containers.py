from secrets import *
from asnake.client import ASnakeClient

client = ASnakeClient(baseurl=as_api, username=as_un, password=as_pw)
client.authorize()
resource_ids = ["/repositories/4/resources/4103", "/repositories/4/resources/4064", "/repositories/4/resources/2798",
                "/repositories/4/resources/1001", "/repositories/4/resources/4048", "/repositories/2/resources/633",
                "/repositories/2/resources/723", "/repositories/2/resources/748", "/repositories/2/resources/414",
                "/repositories/5/resources/5071]"]


def check_children(children):
    if children:
        for child in children:
            if "children" in child.keys():
                archival_object = client.get(child["record_uri"]).json()
                if "instances" in archival_object.keys():
                    for instance in archival_object["instances"]:
                        check_instances(instance)
                print(archival_object)
                check_children(child["children"])
            else:
                archival_object = client.get(child["record_uri"]).json()
                print(archival_object)
    else:
        print("nothing!")
        pass


def check_instances(instance):
    if "sub_container" in instance.keys():
        print(instance["sub_container"])
        check_instances(instance["sub_container"])
    else:
        pass


# for resource_id in resource_ids:
resource_info = client.get(resource_ids[0]).json()
res_tree = client.get(resource_info["tree"]["ref"]).json()
if "children" in res_tree.keys():
    print(res_tree["children"])
    check_children(res_tree["children"])
else:
    print(res_tree)
    print("-"*100)
