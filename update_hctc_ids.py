# Updates all HCTC container indicators to match the ####.###.### format

from secrets import *
from asnake.aspace import ASpace
from asnake.client import ASnakeClient

aspace = ASpace(baseurl=as_api_stag, username=as_un, password=as_pw)
client = ASnakeClient(baseurl=as_api_stag, username=as_un, password=as_pw)
client.authorize()

# all_tcids = client.get('/repositories/8/top_containers', params={'all_ids': True}).json()
# for tc_id in all_tcids[:10]:
#     tc_data = client.get(f'/repositories/8/top_containers/{str(tc_id)}').json()
#     print(tc_data)

all_aoids = client.get('/repositories/8/archival_objects', params={'all_ids': True}).json()
for ao_id in all_aoids:
    ao_data = client.get(f'/repositories/8/archival_objects/{str(ao_id)}').json()
    if 'instances' in ao_data:
        for instance in ao_data['instances']:
            if 'sub_container' in instance.keys():
                tc_data = client.get(instance['sub_container']['top_container']['ref']).json()
                # if 'indicator_2' in instance['sub_container']:
                #     print(instance['sub_container']['indicator_2'])
                if 'indicator' in tc_data:
                    print(tc_data['indicator'])
                # print(instance['sub_container'])
                # print(tc_data)
                # print('\n\n')
        # print(ao_data['instances'])



