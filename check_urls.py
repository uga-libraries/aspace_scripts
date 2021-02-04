import requests
import os
import csv
import re
from pathlib import Path
from secrets import *
from asnake.client import ASnakeClient
from lxml import etree

id_field_regex = re.compile(r"(^id_+\d)")
id_combined_regex = re.compile(r'[\W_]+', re.UNICODE)
web_url_regex = re.compile(r"""(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))""")


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
        for resource_id in resources:
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
        tree = etree.parse(source_path + "/" + file)
        root = tree.getroot()
        for element in root.getiterator():
            element.tag = etree.QName(element).localname
        for element in root.findall(".//*"):
            if element.tag == "extref":
                attributes = dict(element.attrib)
                print(element.getparent().getparent().tag)
                for key, value in attributes.items():
                    if key == "{http://www.w3.org/1999/xlink}href":
                        if "www.anb.org" in value or "www.oxforddnb.com" in value or "doi.org" in value or \
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
                for key, value in attributes.items():
                    if key == "{http://www.w3.org/1999/xlink}href":
                        print("Digital Object: ", attributes["{http://www.w3.org/1999/xlink}title"])
                        print(value)
                        try:
                            test_request = requests.get(value)
                            if test_request.status_code != 200:
                                print(test_request.status_code)
                                write_csv("a", str(file),
                                          "Digital Object: {}".format(attributes["{http://www.w3.org/1999/xlink}title"]),
                                          str(test_request.status_code), str(value))
                        except Exception as e:
                            print(file, e)
                            write_csv("a", str(file),
                                      "Digital Object: {}".format(attributes["{http://www.w3.org/1999/xlink}title"]),
                                      str(e), str(value))
            else:
                element_words = str(element.text).split(" ")
                filtered_words = list(filter(None, element_words))
                for word in filtered_words:
                    clean_word = word.strip(",.;:`~()<>")
                    match = web_url_regex.match(clean_word)
                    if match:
                        print(element.getparent().tag)
                        print(clean_word)
                        if "www.anb.org" in clean_word or "www.oxforddnb.com" in clean_word or "doi.org" in clean_word \
                                or \
                                "http://www.ledger-enquirer.com/2012/07/05/2110319_judge-aaron-cohn-dies-at-95.html?rh=1" \
                                == clean_word:
                            print("Couldn't parse href for: ", file)
                            write_csv("a", str(file), str(element.getparent().getparent().tag), "Couldn't parse href",
                                      str(clean_word))
                            pass
                        else:
                            try:
                                test_request = requests.get(clean_word)
                                if test_request.status_code != 200:
                                    print(test_request.status_code)
                                    write_csv("a", str(file), element.getparent().tag, str(test_request.status_code),
                                              str(clean_word))
                            except Exception as e:
                                print(file, e)
                                write_csv("a", str(file), element.getparent().tag, str(e), str(clean_word))
        print("-" * 200)


source_eads_path = setup_defaults()
# export_eads(as_api, as_un, as_pw, source_eads_path)
write_csv("w", "Collection Number", "Note", "Error Code", "URL")
check_urls(source_eads_path)  # "F:/Schmidtty/Documents/UGA_remote/as_xtf_prgm/as_xtf_prgm/source_eads"
