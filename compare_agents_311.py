# This script is a quick and dirty method for compareing agents from our ArchivesSpace staging environment (v 3.1.1)
# and compares then to our production enviornment (2.8.1). In run(), first uncomment the first 4 lines and run
# get_agents() on prod and staging, then run edited_agents() to generate the EDTAGT_DATA.json with all the agents that
# lost their dates of existence during the upgrade to staging (3.1.1). Make a copy of that file for backup, then run
# update_does() AFTER UPGRADING prod to 3.1.1 to add the dates of existence back to those agents. See
# update_agent_does.py for a more user-friendly script

import json

from secrets import *
from asnake.client import ASnakeClient

prod_client = ASnakeClient(baseurl=as_api, username=as_un, password=as_pw)
prod_client.authorize()

staging_client = ASnakeClient(baseurl=as_api_stag, username=as_un, password=as_pw)
staging_client.authorize()

try:
    agent_data_cache = open("AGENT_DATA.json", "r")
    read_cache = agent_data_cache.read()
    AGENT_CACHE = json.loads(read_cache)
    agent_data_cache.close()
except Exception as e:
    AGENT_CACHE = {}
    print(e)


try:
    edited_agents_cache = open("data/EDTAGT_DATA.json", "r")
    read_ed_cache = edited_agents_cache.read()
    EDAGT_CACHE = json.loads(read_ed_cache)
    edited_agents_cache.close()
except Exception as e:
    EDAGT_CACHE = {}
    print(e)


def correct_dates_type(agent, agent_type, client):
    count = 0
    agent_data = client.get(f"agents/{agent_type}/{agent}").json()
    if "dates_of_existence" in agent_data:
        doe_data = agent_data["dates_of_existence"]
        if doe_data:
            count += 1
            return count, agent_data
        else:
            return count, None
    else:
        return count, None


def get_agents(client, instance):
    count = 0
    agent_types = ["people", "families", "corporate_entities"]
    for agent_type in agent_types:
        agents = client.get(f"agents/{agent_type}", params={"all_ids": True}).json()
        for agent in agents:
            ag_count, agent_wdoe = correct_dates_type(agent, agent_type, client)
            if agent_wdoe is not None:
                unique_id = agent_wdoe["uri"] + f'-{instance}'
                AGENT_CACHE[unique_id] = agent_wdoe
                with open("AGENT_DATA.json", "w") as agent_file:
                    agent_data = json.dumps(AGENT_CACHE)
                    agent_file.write(agent_data)
                    agent_file.close()
            count += ag_count
    return count


def edited_agents():
    for agent, agent_data in AGENT_CACHE.items():
        original_uri = agent.split("-")[0]
        staging_uri = original_uri + "-staging"
        prod_uri = original_uri + "-prod"
        if staging_uri not in AGENT_CACHE:
            if original_uri not in EDAGT_CACHE:
                EDAGT_CACHE[original_uri] = AGENT_CACHE[prod_uri]
                with open("data/EDTAGT_DATA.json", "w") as edtagt:
                    edit_agent = json.dumps(EDAGT_CACHE)
                    edtagt.write(edit_agent)
                    edtagt.close()
    print(len(EDAGT_CACHE))


def update_does():
    for agent, agent_data in EDAGT_CACHE.items():
        date_type = agent_data["dates_of_existence"][0]["date_type"]
        if date_type == "range":
            if "begin" in agent_data["dates_of_existence"][0] and "end" in agent_data["dates_of_existence"][0]:
                begin_date = agent_data["dates_of_existence"][0]["begin"]
                end_date = agent_data["dates_of_existence"][0]["end"]
                if "expression" in agent_data["dates_of_existence"][0]:
                    expression_date = agent_data["dates_of_existence"][0]["expression"]
                else:
                    expression_date = ""
                staging_data = staging_client.get(agent).json()
                dates_of_existence = {"lock_version": 0,
                                      "jsonmodel_type": "structured_date_label",
                                      "date_type_structured": date_type,
                                      "date_label": "existence",
                                      "structured_date_range":
                                          {"lock_version": 0,
                                           "begin_date_standardized": begin_date,
                                           "end_date_standardized": end_date,
                                           "begin_date_standardized_type": "standard",
                                           "end_date_standardized_type": "standard",
                                           "begin_date_expression": expression_date,
                                           "jsonmodel_type": "structured_date_range"}}
                staging_data["dates_of_existence"] = [dates_of_existence]
                update_agent = staging_client.post(agent, json=staging_data).json()
            elif "expression" in agent_data["dates_of_existence"][0]:
                expression_date = agent_data["dates_of_existence"][0]["expression"]
                staging_data = staging_client.get(agent).json()
                dates_of_existence = {"lock_version": 0,
                                      "jsonmodel_type": "structured_date_label",
                                      "date_type_structured": date_type,
                                      "date_label": "existence",
                                      "structured_date_range":
                                          {"date_expression": expression_date,
                                           "lock_version": 0,
                                           "date_standardized_type": "standard",
                                           "jsonmodel_type": "structured_date_range"}}
                staging_data["dates_of_existence"] = [dates_of_existence]
                update_agent = staging_client.post(f"{agent}", json=staging_data).json()
        if date_type == "single":
            staging_data = staging_client.get(agent).json()
            try:
                single_date = agent_data["dates_of_existence"][0]["expression"]
            except Exception as e:
                single_date = None
                print(f'Expression in single date not found {e}\n{agent_data["dates_of_existence"][0]}')
            if not single_date:
                try:
                    single_date = agent_data["dates_of_existence"][0]["begin"]
                    print(f'Using Begin date for single date: {single_date}')
                except Exception as e:
                    single_date = None
                    print(f'Begin in single date not found {e}\n{agent_data["dates_of_existence"][0]["begin"]}')
            if single_date:
                dates_of_existence = {"lock_version": 0,
                                      "date_type_structured": date_type,
                                      "date_label": "existence",
                                      "jsonmodel_type": "structured_date_label",
                                      "structured_date_single":
                                          {"date_expression": single_date,
                                           "lock_version": 0,
                                           "date_role": "begin",
                                           "date_standardized_type": "standard",
                                           "jsonmodel_type": "structured_date_single"}}
                staging_data["dates_of_existence"] = [dates_of_existence]
                update_agent = staging_client.post(f"{agent}", json=staging_data).json()
        if "error" in update_agent:
            print(f'ERROR: {update_agent}\nDate Type: {date_type}\n   {staging_data}')
        else:
            print(f'SUCCESS: {update_agent}')


def run():
    # prod_count = get_agents(prod_client, "prod")
    # staging_count = get_agents(staging_client, "staging")
    # print(f'Staging count: {staging_count}\nProd count: {prod_count}')
    # edited_agents()
    update_does()


run()
