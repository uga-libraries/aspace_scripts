# A test script with different functions testing how to start up a series of background import jobs and monitor their
# progress
from asnake.client import ASnakeClient
from pathlib import Path
import os
import json
import time

as_username = "cschmidt"  # input("Enter your ArchivesSpace username: ")
as_password = "coreyaspace"  # input("Enter your ArchivesSpace password: ")
as_repo = input("Enter ArchivesSpace repository #: ")
# resource_prefix = input("Enter your resource identifier prefix: ")
as_api = "http://aspace-staging-uga.galib.uga.edu:8089"
client = ASnakeClient(baseurl=as_api, username=as_username, password=as_password)
client.authorize()

# job_ids = []
# eads_path = str(Path.joinpath(Path.cwd(), "clean_eads"))
# for root, directories, files in os.walk(eads_path):
#     for filename in files:
#         if filename[0:len(resource_prefix)] == resource_prefix:
#             filepath = str(Path.joinpath(Path.cwd(), "clean_eads", filename))
#             import_file = ('files[]', open(filepath, 'rb'),)
#             import_job = json.dumps(
#                 {"job_type": "import_job", "job": {"jsonmodel_type": "import_job", "filenames": [filename],
#                                                    "import_type": "ead_xml"}})
#             import_records = client.post('repositories/{}/jobs_with_files'.format(as_repo), files=[import_file],
#                                          params={"job": import_job})
#             response = json.loads(import_records.text)
#             print(response)
#             job_ids.append(response["id"])


def check_imports(sleep_counter, job_id, queued=False):
# LOG JOBS
    time.sleep(sleep_counter)
    check_job = client.get('repositories/{}/jobs/{}'.format(as_repo, job_id))
    job_response = json.loads(check_job.text)
    if queued is True:
        print(job_response)
    if job_response["status"] == "failed":
        check_status = client.get('repositories/{}/jobs/{}/log'.format(as_repo, job_id))
        with open('ead_import_log-{}.txt'.format(resource_prefix), 'w') as log:
            log.write(check_status.text + "\n")
            log.close()
    elif job_response["status"] == "queued":
        sleep_counter += 10
        check_imports(sleep_counter, job_id, queued=True)
    else:
        return "Success: {} with job # {}".format(job_response["filenames"], job_id)


def get_all_resources(as_repo):
    resources = client.get('repositories/{}/resources'.format(as_repo), params={"all_ids": True})
    print(resources.text)


# get_all_resources(as_repo)

def publish_do_fvs():
    repos = client.get("repositories").json()
    for repo in repos:
        repo_id = repo["uri"].split("/")[2]
        response_dos = client.get('repositories/{}/digital_objects'.format(repo_id), params={"all_ids": True})
        all_dos = list(response_dos.json())
        for do_id in all_dos[0:10]:
            response_do = client.get('repositories/{}/digital_objects/{}'.format(repo_id, do_id))
            do = dict(response_do.json())
            print(do)
            # do["file_versions"][0]["is_representative"] = True
            # update_do = client.post('repositories/{}/digital_objects/{}/publish'.format(repo_id, do_id))
            # print(update_do.text)


# publish_do_fvs()

# jobs_queued = []
# for job in job_ids:
#     check_imports(0, job)

# UPDATE A RECORD
# get_resource = client.get('/repositories/5/resources/1814')
# resource = json.loads(get_resource.text)
# resource["restrictions"] = True
# update_resource = client.post('/repositories/5/resources/1814', json=resource)
# print(update_resource, update_resource.text)


# CANCEL ALL JOBS
# jobs = client.get('repositories/5/jobs', params={'all_ids': 'true'})
# print(jobs.text)
# response = json.loads(jobs.text)
# for job in response:
#     cancel_job = client.post('repositories/5/jobs/{}/cancel'.format(str(job)))
#     print(cancel_job.text)
