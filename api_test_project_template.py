# This script is a template for making scripts working with the ArchivesSpace API, particularly working with the
# ArchivesSnake library: https://github.com/archivesspace-labs/ArchivesSnake
from secrets import *
from asnake.aspace import ASpace
from asnake.client import ASnakeClient

aspace = ASpace(baseurl=as_api, username=as_un, password=as_pw)
client = ASnakeClient(baseurl=as_api, username=as_un, password=as_pw)
client.authorize()
