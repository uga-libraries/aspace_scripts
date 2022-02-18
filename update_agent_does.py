# This script provides a command line user interface for compareing agents from our ArchivesSpace staging environment
# (v 3.1.1) and compares then to our production enviornment (2.8.1). First, run the command compare agents. It
# generates 2 JSON files: AGENTS_CACHE.json stores all agents in both environments that have dates of existence; and
# EDTAGT_DATA.json stores all the agents who lost their dates of existence when upgrading from 2.8.1 to 3.1.1. Using
# the update does command, the script goes through all the agents in EDTAGT_DATA.json and adds dates of existence back
# to the now updated production environment (3.1.1).

import json
import requests

from asnake.client import ASnakeClient
from asnake.client.web_client import ASnakeAuthError


def connect_prod_client(as_api, as_un, as_pw):
    prod_client = ASnakeClient(baseurl=as_api, username=as_un, password=as_pw)
    try:
        requests.get(as_api)
    except Exception as api_error:
        print("Your API credentials were entered incorrectly.\n"
              "Please try again.\n\n" + api_error.__str__())
        return False
    else:
        try:
            prod_client.authorize()
        except ASnakeAuthError as e:
            error_message = ""
            if ":" in str(e):
                error_divided = str(e).split(":")
                for line in error_divided:
                    error_message += line + "\n"
            else:
                error_message = str(e)
            print(error_message)
            return False
        else:
            return prod_client


def connect_staging_client(as_api_stag, as_un, as_pw):
    staging_client = ASnakeClient(baseurl=as_api_stag, username=as_un, password=as_pw)
    try:
        requests.get(as_api_stag)
    except Exception as api_error:
        print("Your API credentials were entered incorrectly.\n"
              "Please try again.\n\n" + api_error.__str__())
        return False
    else:
        try:
            staging_client.authorize()
        except ASnakeAuthError as e:
            error_message = ""
            if ":" in str(e):
                error_divided = str(e).split(":")
                for line in error_divided:
                    error_message += line + "\n"
            else:
                error_message = str(e)
            print(error_message)
            return False
        else:
            return staging_client


def get_does_cache():
    try:
        agent_data_cache = open("AGENT_DATA.json", "r")
        read_cache = agent_data_cache.read()
        agent_cache = json.loads(read_cache)
        agent_data_cache.close()
    except Exception as e:
        agent_cache = {}
        print(e)
    return agent_cache


def get_diffagt_cache():
    try:
        edited_agents_cache = open("EDTAGT_DATA.json", "r")
        read_ed_cache = edited_agents_cache.read()
        edagt_cache = json.loads(read_ed_cache)
        edited_agents_cache.close()
    except Exception as e:
        edagt_cache = {}
        print(e)
    return edagt_cache


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


def get_agents(client, instance, agent_cache):
    count = 0
    agent_types = ["people", "families", "corporate_entities"]
    for agent_type in agent_types:
        agents = client.get(f"agents/{agent_type}", params={"all_ids": True}).json()
        for agent in agents:
            ag_count, agent_wdoe = correct_dates_type(agent, agent_type, client)
            if agent_wdoe is not None:
                unique_id = agent_wdoe["uri"] + f'-{instance}'
                agent_cache[unique_id] = agent_wdoe
                with open("AGENT_DATA.json", "w") as agent_file:
                    agent_data = json.dumps(agent_cache)
                    agent_file.write(agent_data)
                    agent_file.close()
            count += ag_count
    return count


def edited_agents(agent_cache, edagt_cache):
    for agent, agent_data in agent_cache.items():
        original_uri = agent.split("-")[0]
        staging_uri = original_uri + "-staging"
        prod_uri = original_uri + "-prod"
        if staging_uri not in agent_cache:
            if original_uri not in edagt_cache:
                edagt_cache[original_uri] = agent_cache[prod_uri]
                with open("EDTAGT_DATA.json", "w") as edtagt:
                    edit_agent = json.dumps(edagt_cache)
                    edtagt.write(edit_agent)
                    edtagt.close()
    print(len(edagt_cache))


def update_does(edagt_cache, prod_client):
    update_agent = None
    staging_data = None
    for agent, agent_data in edagt_cache.items():
        try:
            date_type = agent_data["dates_of_existence"][0]["date_type"]
        except Exception as e:
            print(f'ERROR: No Date Type found: {e}\nAgent data: {agent_data}\n')
        else:
            if date_type == "range":
                if "begin" in agent_data["dates_of_existence"][0] and "end" in agent_data["dates_of_existence"][0]:
                    begin_date = agent_data["dates_of_existence"][0]["begin"]
                    end_date = agent_data["dates_of_existence"][0]["end"]
                    if "expression" in agent_data["dates_of_existence"][0]:
                        expression_date = agent_data["dates_of_existence"][0]["expression"]
                    else:
                        expression_date = ""
                    staging_data = prod_client.get(agent).json()
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
                    update_agent = prod_client.post(agent, json=staging_data).json()
                elif "expression" in agent_data["dates_of_existence"][0]:
                    expression_date = agent_data["dates_of_existence"][0]["expression"]
                    staging_data = prod_client.get(agent).json()
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
                    update_agent = prod_client.post(f"{agent}", json=staging_data).json()
            elif date_type == "single":
                staging_data = prod_client.get(agent).json()
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
                    update_agent = prod_client.post(f"{agent}", json=staging_data).json()
            if "error" in update_agent or update_agent is None:
                print(f'ERROR: {update_agent}\nDate Type: {date_type}'
                      f'\n   Staging data response: {staging_data}'
                      f'\n   Cached Agent data: {agent_data}')
            else:
                print(f'SUCCESS: {update_agent}')


def run(arguments, prod_client, staging_client):
    total_agent_cache = get_does_cache()
    diff_agent_cache = get_diffagt_cache()
    if arguments == "compare agents":
        prod_count = get_agents(prod_client, "prod", total_agent_cache)
        staging_count = get_agents(staging_client, "staging", total_agent_cache)
        print(f'Staging count: {staging_count}\nProd count: {prod_count}')
        return "Success"
    elif arguments == "update does":
        edited_agents(total_agent_cache, diff_agent_cache)
        update_does(diff_agent_cache, prod_client)
        return "Success"
    else:
        return None


def connection_interface():
    credentials = False
    while credentials is False:
        print(f'Enter your ArchivesSpace credentials...')
        as_prod_api = input('ArchivesSpace Production API URL: ')
        as_staging_api = input('ArchivesSpace Staging API URL: ')
        as_username = input('ArchivesSpace username: ')
        as_password = input('ArchivesSpace password: ')
        prod_client = connect_prod_client(as_prod_api, as_username, as_password)
        stag_client = connect_staging_client(as_staging_api, as_username, as_password)
        if prod_client is not False and stag_client is not False:
            credentials = True
    return prod_client, stag_client


def user_interface():
    help_statement = (f'\nUpdate Agents Dates of Existence script\n\nDIRECTIONS\nFirst run the command '
                      f'"compare agents" with this script when staging is on 3.1.1 and production is on 2.8.1. Then '
                      f'run the command "update does" to add dates of existence back to agents.\n\nCOMMANDS\n\n'
                      f'compare agents = Compare agent records with dates of existence from prod (2.8.1) and staging '
                      f'(3.1.1)\n'
                      f'update does = Take the EDTAGT_DATA.json file generated when running compare agents with agents '
                      f'that lost their dates of existence and update them - must run compare agents first!\n'
                      f'help = List these options\n'
                      f'exit = Exit the script\n')
    user_arguments = ["run update", "compare agents", "update does", "help", "exit"]
    user_args = ""
    while user_args != "exit":
        prod_client, staging_client = connection_interface()
        print(help_statement)
        user_args = input(f'Enter a command: ')
        if user_args not in user_arguments:
            print(f'Command not recognized: {user_args}')
        elif user_args == "exit":
            print("Exiting the program...")
            break
        elif user_args == "help":
            print(help_statement)
        else:
            operation = run(user_args, prod_client, staging_client)
            if operation is None:
                print(f'Command not recognized: {user_args}')


user_interface()
