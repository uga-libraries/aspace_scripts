from secrets import *
from asnake.client import ASnakeClient


def correct_dates_type(agent, agent_type, client):
    count = 0
    agent_data = client.get(f"agents/{agent_type}/{agent}").json()
    if "dates_of_existence" in agent_data:
        if not agent_data["dates_of_existence"]:
            count += 1
    return count


def get_agents(client):
    count = 0
    agent_types = ["people", "families", "corporate_entities"]
    for agent_type in agent_types:
        # print("Agent Title;Agent Dates;Agent Type;ASpace URI")
        # print(agent_type + "\n")
        agents = client.get(f"agents/{agent_type}", params={"all_ids": True}).json()
        for agent in agents:
            count += correct_dates_type(agent, agent_type, client)
        # print("\n" + "-"*100)
    return count


def run():
    staging_client = ASnakeClient(baseurl=as_api_stag, username=as_un, password=as_pw)
    staging_client.authorize()
    staging_count = get_agents(staging_client)
    prod_client = ASnakeClient(baseurl=as_api, username=as_un, password=as_pw)
    prod_client.authorize()
    prod_count = get_agents(prod_client)
    print(f'Staging count: {staging_count}\nProd count: {prod_count}')


run()
