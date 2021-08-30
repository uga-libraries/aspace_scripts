# This script checks archival objects for specific resources in ArchivesSpace and if they have an 'unknown_container' as
# the value of their indicator, then it deletes that object.
from secrets import *
from asnake.aspace import ASpace
from asnake.client import ASnakeClient


aspace = ASpace(baseurl=as_api, username=as_un, password=as_pw)
client = ASnakeClient(baseurl=as_api, username=as_un, password=as_pw)
client.authorize()
resource_ids = ["/repositories/4/resources/4103", "/repositories/4/resources/4064", "/repositories/4/resources/2798",
                "/repositories/4/resources/1001", "/repositories/4/resources/4048", "/repositories/2/resources/633",
                "/repositories/2/resources/723", "/repositories/2/resources/748", "/repositories/2/resources/414"]
# "/repositories/5/resources/5071" - UA collection - Steve to check with Kat

for resource_id in resource_ids:
    unknown_count = 0
    uri_breakup = resource_id.split("/")
    res_id = uri_breakup[4]
    repo_id = uri_breakup[2]
    try:
        rl_repo = aspace.repositories(repo_id)
        resource_record = rl_repo.resources(res_id).tree
        resource_tree = resource_record.walk
        print(rl_repo.resources(res_id).json()["title"])
        for node in resource_tree:
            ao_json = client.get(node.uri).json()
            for instance in ao_json["instances"]:
                if "sub_container" in instance.keys():
                    indicators = []
                    types = []
                    for key, value in instance["sub_container"].items():
                        if "indicator_" in key:
                            if "unknown container" == value:
                                child_type = "type_" + str(key[-1])
                                indicators.append(key)
                                types.append(child_type)
                                unknown_count += 1
                    for indicator in indicators:
                        try:
                            del instance["sub_container"][indicator]
                        except Exception as e:
                            print("There was an error when deleting the unknown indicator: {}".format(e))
                            print(instance)
                    for child_type in types:
                        try:
                            del instance["sub_container"][child_type]
                        except Exception as e:
                            print("There was an error when deleting the unknown child/grandchild type: {}".format(e))
                            print(instance)
                    if indicators and types:
                        update_ao = client.post(node.uri, json=ao_json).json()
                        print(update_ao)
                else:
                    indicators = []
                    types = []
                    for key, value in instance.items():
                        if "indicator_" in key:
                            if "unknown container" == value:
                                child_type = "type_" + str(key[-1])
                                indicators.append(key)
                                types.append(child_type)
                                unknown_count += 1
                    for indicator in indicators:
                        try:
                            del instance[indicator]
                        except Exception as e:
                            print("There was an error when deleting the unknown indicator: {}".format(e))
                            print(instance)
                    for child_type in types:
                        try:
                            del instance[child_type]
                        except Exception as e:
                            print("There was an error when deleting the unknown child/grandchild type: {}".format(e))
                            print(instance)
                    if indicators and types:
                        update_ao = client.post(node.uri, json=ao_json).json()
                        print(update_ao)
        print("Total unknown containers = {}".format(str(unknown_count)))
        print("\n")
        print("-" * 100)
    except Exception as e:
        print("There was an error retrieving {}: {}".format(resource_id, e))
        try:
            print(client.get(resource_id).json())
        except:
            print("Could not retrieve resource")
        print("\n")
        print("-" * 100)
