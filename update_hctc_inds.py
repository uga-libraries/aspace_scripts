# Updates all HCTC container indicators to match the ####.###.###abcdetc. format for those beginning with four numbers,
# aka year

import re
from secrets import *
from asnake.client import ASnakeClient

match_year = re.compile(r"^[0-9]{4}", re.UNICODE)

client = ASnakeClient(baseurl=as_api_stag, username=as_un, password=as_pw)
client.authorize()

def generate_new_ind(old_ind):
    """
    Take the indicator string and split into sections on the ., evaulate between numbers and letters, then recombine
    into one new ind, stripping ending . and any spaces.
    Args:
        old_ind (str): the indicator as given in ArchivesSpace top container or child container (not grandchild)

    Returns:
        new_ind(str): the updated indicator, with format ####.###.###<optional_letters>

    """
    if match_year.match(old_ind):
        ind_sections = old_ind.split('.')
        new_ind = f"{ind_sections[0]}."
        section_count = 1
        for subsection in ind_sections[1:]:  # Skip first section, which is the year and should always be 4 numbers
            if section_count > 2:  # For an ind like this: 1900.0.32.a
                new_ind += subsection + "."
            elif "-" in subsection:  # To properly reformat inds like the following: 1950.188.19ab-20 or 1950.188.21-22
                subsection_parts = subsection.split("-")
                new_subsection_ind = ""
                for subsubsection in subsection_parts:
                    subsubsection_ind = parse_ind_sections(subsubsection)
                    subsubsection_ind += "-"
                    new_subsection_ind += subsubsection_ind
                new_ind += new_subsection_ind[:-1] + "."
            else:
                new_sub_ind = parse_ind_sections(subsection)
                new_ind += new_sub_ind + "."
            section_count += 1
        new_ind = new_ind[:-1]
        return new_ind.strip()  # Some indicators contain trailing spaces, the darned detail devils!
    else:
        return None


def parse_ind_sections(subsection):
    """
    Parse a subsection of the indicator and format into ###abcdetc.
    Args:
        subsection (str): subsection of the indicator to parse into ###abcs

    Returns:
        new_sub_ind (str): the reformatted string, structured ###abcdetc.
    """
    new_sub_ind = ""
    number_list = []
    letter_list = []
    for character in subsection:
        try:
            int(character)
            number_list.append(character)
        except ValueError:
            letter_list.append(character)
    for number in number_list:
        new_sub_ind += number
    new_sub_ind = new_sub_ind.zfill(3)
    for letter in letter_list:
        new_sub_ind += letter
    return new_sub_ind


def run_update(update=True):
    """
    Takes all archival objects in the HCTC repository (8) and checks them for any instances. If instances are found,
    iterate down to search for sub_containers (child instances) and reformat their indicators to ####.###.###abcdetc., 
    and find all associated top containers and reformat their indicators to ####.###.###abcdetc. if their indicators 
    start with 4 numbers (year).
    Args:
        update (bool): if True, post the updated indicators to ASpace. If false, don't post!
    """
    all_aoids = client.get('/repositories/8/archival_objects', params={'all_ids': True}).json()
    for ao_id in all_aoids:
        ao_data = client.get(f'/repositories/8/archival_objects/{str(ao_id)}').json()
        if 'instances' in ao_data:
            for instance in ao_data['instances']:
                if 'sub_container' in instance.keys():
                    if 'indicator_2' in instance['sub_container']:
                        new_childc_ind = generate_new_ind(instance['sub_container']['indicator_2'])
                        if new_childc_ind is not None:
                            print(new_childc_ind, "Child_Container")
                            instance['sub_container']['indicator_2'] = new_childc_ind
                            if update is True:
                                # print(ao_data)
                                client.post(f'/repositories/8/archival_objects/{str(ao_id)}', json=ao_data)
                    tc_data = client.get(instance['sub_container']['top_container']['ref']).json()
                    if 'indicator' in tc_data:
                        new_topc_ind = generate_new_ind(tc_data['indicator'])
                        if new_topc_ind is not None:
                            print(new_topc_ind, "Top_Container")
                            tc_data['indicator'] = new_topc_ind
                            if update is True:
                                # print(tc_data)
                                client.post(instance['sub_container']['top_container']['ref'], json=tc_data)


if __name__ == "__main__":
    run_update(update=False)

