import requests
import os
import csv
from secrets import *
from lxml import etree

with open("invalid_links.csv", mode="w", newline='') as invalid_links:
    file_write = csv.writer(invalid_links, delimiter=",")
    file_write.writerow(["Collection Number", "Note", "Error Code", "URL"])
    invalid_links.close()

for file in os.listdir(source_path):
    print(file)
    tree = etree.parse(source_path + "/" + file)
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
                        with open("invalid_links.csv", mode="a", newline='') as invalid_links:
                            file_write = csv.writer(invalid_links, delimiter=",")
                            file_write.writerow([str(file), str(element.getparent().getparent().tag),
                                                 "Couldn't parse href", str(value)])
                            invalid_links.close()
                        pass
                    else:
                        try:
                            print(value)
                            test_request = requests.get(value)
                            if test_request.status_code != 200:
                                print(test_request.status_code)
                                with open("invalid_links.csv", mode="a", newline='') as invalid_links:
                                    file_write = csv.writer(invalid_links, delimiter=",")
                                    file_write.writerow([str(file), str(element.getparent().getparent().tag),
                                                         str(test_request.status_code), str(value)])
                                    invalid_links.close()
                            elif "russelldoc" in value or "hmfa" in value:
                                with open("invalid_links.csv", mode="a", newline='') as invalid_links:
                                    file_write = csv.writer(invalid_links, delimiter=",")
                                    file_write.writerow([str(file), str(element.getparent().getparent().tag),
                                                         "Old website URL - consider replacing", str(value)])
                                    invalid_links.close()
                        except Exception as e:
                            print(file, e)
                            with open("invalid_links.csv", mode="a", newline='') as invalid_links:
                                file_write = csv.writer(invalid_links, delimiter=",")
                                file_write.writerow([str(file), str(element.getparent().getparent().tag), str(e),
                                                     str(value)])
                                invalid_links.close()
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
                            with open("invalid_links.csv", mode="a", newline='') as invalid_links:
                                file_write = csv.writer(invalid_links, delimiter=",")
                                file_write.writerow([str(file), "Digital Object: {}".format(attributes["title"]),
                                                     str(test_request.status_code), str(value)])
                                invalid_links.close()
                    except Exception as e:
                        print(file, e)
                        with open("invalid_links.csv", mode="a", newline='') as invalid_links:
                            file_write = csv.writer(invalid_links, delimiter=",")
                            file_write.writerow([str(file), "Digital Object: {}".format(attributes["title"]), str(e),
                                                 str(value)])
                            invalid_links.close()
    print("-" * 200)
    # stuck at RBRL321AC.xml
