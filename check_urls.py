import requests
import os
import csv
import re
from pathlib import Path
from secrets import *
from asnake.client import ASnakeClient
from lxml import etree

id_field_regex = re.compile(r"(^id_+\d)")
id_combined_regex = re.compile('[\W_]+', re.UNICODE)


def setup_defaults():
    try:
        current_directory = os.getcwd()
        for root, directories, files in os.walk(current_directory):
            if "source_eads" in directories:
                return str(Path(os.getcwd(), "source_eads"))
            else:
                raise Exception
    except Exception as source_ead_error:
        print(str(source_ead_error) + "\nNo source_eads folder found, creating new one...", end='', flush=True)
        current_directory = os.getcwd()
        folder = "source_eads"
        source_path = os.path.join(current_directory, folder)
        os.mkdir(source_path)
        print("{} folder created\n".format(folder))
        return str(source_path)


def export_eads(as_api, as_un, as_pw, source_path):
    client = ASnakeClient(baseurl=as_api, username=as_un, password=as_pw)
    client.authorize()
    repos = client.get("repositories").json()
    for repo in repos:
        print(repo["name"] + "\n")
        repo_id = repo["uri"].split("/")[2]
        resources = client.get("repositories/{}/resources".format(repo_id), params={"all_ids": True}).json()
        for resource_id in resources[:4]:
            resource = client.get("repositories/{}/resources/{}".format(repo_id, resource_id))
            combined_id = ""
            for field, value in resource.json().items():
                id_match = id_field_regex.match(field)
                if id_match:
                    combined_id += value + "-"
            combined_id = combined_id[:-1]
            combined_aspace_id_clean = id_combined_regex.sub('', combined_id)
            if resource.json()["publish"] is True:
                if resource.status_code == 200:
                    export_ead = client.get("repositories/{}/resource_descriptions/{}.xml".format(repo_id, resource_id),
                                            params={"include_unpublished": False, "include_daos": True,
                                                    "numbered_cs": True, "print_pdf": False, "ead3": False})
                    filepath = str(Path(source_path, combined_aspace_id_clean))
                    filepath = filepath + ".xml"
                    with open(filepath, "wb") as local_file:
                        local_file.write(export_ead.content)
                        local_file.close()
                        print("Exported: {}".format(combined_id))
                else:
                    print("\nThe following errors were found when exporting {}:\n{}: {}\n".format(combined_id, resource,
                                                                                                  resource.text))
        print("-"*100)


def write_csv(mode, coll_num, note, err_code, url):
    with open("invalid_links.csv", mode=mode, newline='') as invalid_links:
        file_write = csv.writer(invalid_links, delimiter=",")
        file_write.writerow([coll_num, note, err_code, url])
        invalid_links.close()


def check_urls(source_path):
    for file in os.listdir(source_path):
        print(file)
        tree = etree.parse(str(Path(source_path, file)))
        root = tree.getroot()
        for element in root.findall(".//*"):
            if element.tag == "extref":
                attributes = dict(element.attrib)
                print(element.getparent().getparent().tag)
                for key, value in attributes.items():
                    if key == "href":
                        if "www.anb.org" in value or "www.oxforddnb.com" in value or \
                                "http://www.ledger-enquirer.com/2012/07/05/2110319_judge-aaron-cohn-dies-at-95.html?rh=1" \
                                == value:
                            print("Couldn't parse href for: ", file)
                            write_csv("a", str(file), str(element.getparent().getparent().tag), "Couldn't parse href",
                                      str(value))
                            pass
                        else:
                            try:
                                print(value)
                                test_request = requests.get(value)
                                if test_request.status_code != 200:
                                    print(test_request.status_code)
                                    write_csv("a", str(file), str(element.getparent().getparent().tag),
                                              str(test_request.status_code), str(value))
                                elif "russelldoc" in value or "hmfa" in value:
                                    write_csv("a", str(file), str(element.getparent().getparent().tag),
                                              "Old website URL - consider replacing", str(value))
                            except Exception as e:
                                print(file, e)
                                write_csv("a", str(file), str(element.getparent().getparent().tag), str(e), str(value))
            if element.tag == "dao":
                attributes = dict(element.attrib)
                print("Digital Object: ", attributes["title"])
                for key, value in attributes.items():
                    if key == "href":
                        print(value)
                        try:
                            test_request = requests.get(value)
                            if test_request.status_code != 200:
                                print(test_request.status_code)
                                write_csv("a", str(file), "Digital Object: {}".format(attributes["title"]),
                                          str(test_request.status_code), str(value))
                        except Exception as e:
                            print(file, e)
                            write_csv("a", str(file), "Digital Object: {}".format(attributes["title"]), str(e),
                                      str(value))
        print("-" * 200)


source_eads_path = setup_defaults()
export_eads(as_api, as_un, as_pw, source_eads_path)
write_csv("w", "Collection Number", "Note", "Error Code", "URL")
check_urls(source_eads_path)
