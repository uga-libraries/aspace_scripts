# import re
from secrets import *
from asnake.client import ASnakeClient


# date_regex = re.compile(r"((?:(?:between) )*\d{4}(?:(?:-| and )\d{4})).*")

client = ASnakeClient(baseurl=as_api_stag, username=as_un, password=as_pw)
client.authorize()
count = 0


def correct_dates(agents, agent_type):
    for agent in agents:
        expression = ""
        agent_data = client.get(f"agents/{agent_type}/{agent}").json()
        if "dates_of_existence" not in agent_data:
            print(agent_data, f"agents/{agent_type}/{agent}")
        else:
            for date in agent_data["dates_of_existence"]:
                if "begin" in date and "end" in date:
                    expression += date["begin"] + "-" + date["end"]
                    date["date_type"] = "range"
                elif "begin" not in date and "end" in date:
                    expression += "-" + date["end"]
                    date["date_type"] = "single"
                elif "begin" in date and "end" not in date:
                    expression += date["begin"] + "-"
                    date["date_type"] = "single"
                elif "expression" in date:
                    expression = date["expression"]
            if expression:
                for name in agent_data["names"]:
                    if name["is_display_name"] is True:
                        if "dates" not in name or not name["dates"]:  # if dates already exists or if it doesn't have any values
                            name["dates"] = expression
                            try:
                                update_agent = client.post(f"agents/{agent_type}/{agent}", json=agent_data).json()
                                if "error" in update_agent:
                                    raise Exception
                                else:
                                    print(f"{agent_data['title']};{name['dates']};"
                                          f"{agent_data['dates_of_existence'][0]['date_type']};"
                                          f"{agent_data['uri']}")
                                    global count
                                    count += 1
                            except Exception as e:
                                print(f"ERROR;{agent_data['title']};"
                                      f"URI: {agent_data['uri']}\nError: {e}")
                        else:
                            print(f"{agent_data['title']};{name['dates']};"
                                  f"{agent_data['dates_of_existence'][0]['date_type']};"
                                  f"{agent_data['uri']}")


agent_types = ["people", "families", "corporate_entities"]
for agent_type in agent_types:
    print("Agent Title;Agent Dates;Agent Type;ASpace URI")
    print(agent_type + "\n")
    agents = client.get(f"agents/{agent_type}", params={"all_ids": True}).json()
    correct_dates(agents, agent_type)
    print("\n" + "-"*100)
print(f"Updated a total of {str(count)} agents")
