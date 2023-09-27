# Overview
A collection of Python/SQL scripts for data cleanup, management, and others related to UGA's ArchivesSpace 
implementation.

# Getting Started

## Dependencies
Not every script requires every package as listed in the requirements.txt file. If you need to use a script, check the 
import statements at the top to see which specific packages are needed.

- [ArchivesSnake](https://github.com/archivesspace-labs/ArchivesSnake) - Library used for interacting with the 
ArchivesSpace API
- [lxml](https://lxml.de/) - Used to parse XML files for evaluating any XML syntax errors and parsing data from 
downloaded XML files
- [mysql](https://dev.mysql.com/doc/connector-python/en/) - Used to import mysql-connector
- [mysqlclient](https://github.com/PyMySQL/mysqlclient) - Used to connect to the ArchivesSpace MySQL database
- [mysql-connector-python](https://dev.mysql.com/doc/connector-python/en/) - Used to connect and detect any connection 
errors to the ArchivesSpace MySQL database
- [openpyxl](https://openpyxl.readthedocs.io/en/stable/) - Used to create and write an Excel spreadsheet to document
data audit report
- [PySimpleGUI](https://github.com/PySimpleGUI/PySimpleGUI) - The GUI packaged used to make GUIs
- [requests](https://docs.python-requests.org/en/latest/index.html) - Used to check URLs and get their status codes

## Installation

1. Download the repository via cloning to your local IDE or using GitHub's Code button and Download as ZIP
2. Run `pip install requirements.txt` or check the import statements for the script you want to run and install those 
packages
3. Create a secrets.py file with the following information:
   1. An ArchivesSpace admin username, password
   2. The URLs to your ArchivesSpace staging and production API instances
   3. Variables with their values set to user emails you want to send the report to
   4. The email server from which you send your email report
   5. Your ArchivesSpace's staging database credentials, including username, password, hostname, database name, and port
4. Run the script as `python3 ASpace_Data_Audit.py`

# Workflow
## api_test_project_template.py

Template for making scripts working with the ArchivesSpace API, particularly working with the ArchivesSnake
library: https://github.com/archivesspace-labs/ArchivesSnake

## as_functions.py

A test script with different functions testing how to start up a series of background import jobs and monitor their
progress

## aspace_migration.py

Runs a gamut of different cleanup functions against ArchivesSpace after UGA's migration from Archivists'
Toolkit

## check_aspace_aos.py

Checks all archival objects in ArchivesSpace and checks to see what objects are listed as collections, as well as
updating ms3789 to change its objects from 'collection' to 'file'

## check_child_counts.py

Checks how many children a parent object has in ArchivesSpace and if the number of children is equal to or greater than
1000, logs them in a .csv file

## check_enumerations.py

Checks a standard list of controlled vocabulary lists and updates ArchivesSpace by deleting or merging values

## check_file_levels.py

Checks for parent files (archival objects with children) that did not have Instances or top containers. It's confusing.

## check_urls.py

Exported all published resources from ASpace as an EAD.xml file, then took those files and looked for any URLs that were
present, checked their HTTP status and if it returned an error (anything but 200), then logged the error in a
spreadsheet. This was later adapted to make the Check URLs custom report plugin for ArchivesSpace.

## compare_agents_311.py

Quick and dirty method for comparing agents from our ArchivesSpace staging environment (v 3.1.1)
and compares then to our production environment (2.8.1). In run(), first uncomment the first 4 lines and run
get_agents() on prod and staging, then run edited_agents() to generate the EDTAGT_DATA.json with all the agents that
lost their dates of existence during the upgrade to staging (3.1.1). Make a copy of that file for backup, then run
update_does() AFTER UPGRADING prod to 3.1.1 to add the dates of existence back to those agents. See update_agent_does.py
for a more user-friendly script

## delete_unknown_containers.py

Checks archival objects for specific resources in ArchivesSpace and if they have an 'unknown_container' as the value of
their indicator, then it deletes that object

## export_all_resources.py

Exports all published resources for every repository in an ArchivesSpace instance and assigns a concatenated version of
the identifier as the filename

## find_er_accessions.sql
Finds electronic record accessions and their linked resources

## find_unknown_containers.py

Finds parent archival objects that have 'unknown container' in their identifier and logs it into a spreadsheet

## generate_subject-agent_list.py

Writes all subjects and agents to a spreadsheet with their title and URI. This script was made as the first step in a
project to clean up subjects and agents in ArchivesSpace. The final step is outlined in update_subjects_agents.py

## get_aos_ms30002e.py

This script gets all the archival objects for ms3000_2e


## get_uris.py

Retrieves digital object URIs from ArchivesSpace using a preformatted spreadsheet input with titles and dates of
archival objects to match to digital objects

## hargrett_cleanup_script.sql

Runs several cleanup operations on our data before migration from Archivists' Toolkit to ArchivesSpace. It updates
digital objects to change their repository based on their METS Identifier, delete component unique identifier (aka
subdivisionIdentifier) content in that field, replaces leftover xml namespaces from note contents, set resource level to
file when it is collection, and update specific digital objects to University Archives (repository 6)

## link_subjects_resources.py

Grab subjects from the ArchivesSpace database and their links to all resources and generates a spreadsheet with that
info

## ms3000_nofolder.py

Gets all archival objects in collections ms3000_1a, ms3000_1b, ms3000_2a, and ms3000_2b that don't have folders in their
container instances

## multiple_top_containers.sql

Grabs published archival objects with multiple top container instances attached to it

## pre_migration_cleanup.py

Attempts to run SQL updates on Archivists' Toolkit databases for cleanup before migrating to ArchivesSpace

## publish_do_fvs.py

Publishes all digital object file versions

## publish_dos.py

Publishes all digital objects

## resources_wout_creators.py

Checks all resources in an ArchivesSpace instance and makes an Excel spreadsheet with those without creators

## russell_av_containers.sql

Grabs all top containers with instance types that are either "moving_images" or "audio" for the Russell repository

## russell_cleanup_script.sql

This runs several cleanup operations on our data for the Russell repository before migration from Archivists' Toolkit to
ArchivesSpace. It updates FileVersions Use Statements to Audio-Streaming, changed Digital Object Show attribute to
onLoad instead of replace, replaces leftover xml namespaces from note contents, and sets instance and extent types for
some stubborn items.

## test_api_endpoints.py

Tests various API endpoints for ArchivesSpace

## test_archobj.py

Tests the various endpoints for the archival_object.rb controller file for ArchivesSpace

## test_exports.py

Tests the exports from the ArchivesSpace API

## test_resource_endpoints.py
Tests resource.rb endpoints for ArchivesSpace

## test_suppression_endpoints.py

Tests suppression.rb endpoints for ArchivesSpace

## top_containers_no_barcode.sql

Grabs all top containers that have no barcodes and are associated with published archival objects and resources

## unpublish_records.py

Unpublishes resources in ArchivesSpace when they have [CLOSED] in the resource id

## update_agentdates.py

Takes info from the Dates of Existence and puts them in the Dates field to display when exporting

## update_agent_does.py

Provides a command line user interface for comparing agents from our ArchivesSpace staging environment (v 3.1.1) and
compares then to our production environment (2.8.1). First, run the command compare agents. It generates 2 JSON files:
AGENTS_CACHE.json stores all agents in both environments that have dates of existence; and EDTAGT_DATA.json stores all
the agents who lost their dates of existence when upgrading from 2.8.1 to 3.1.1. Using the update does command, the
script goes through all the agents in EDTAGT_DATA.json and adds dates of existence back to the now updated production
environment (3.1.1).

## update_containers.py

Updates ArchivesSpace containers from a spreadsheet

## update_ms30002f.py

Transfers a series of archival objects from ms3000_2e to ms3000_2f at the top level

## update_subjects_agents.py

Deletes and merges subjects from a spreadsheet

(source: https://github.com/uga-libraries/general-aip)

# Author

- Corey Schmidt - Project Management Librarian/Archivist at the University of Georgia Libraries

# Acknowledgements

- ArchivesSpace community
- Kevin Cottrell - GALILEO/Library Infrastructure Systems Architect at the University of Georgia Libraries
- PySimpleGUI
