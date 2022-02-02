# Scripts

## api_test_project_template.py
This script is a template for making scripts working with the ArchivesSpace API, particularly working with the ArchivesSnake library: https://github.com/archivesspace-labs/ArchivesSnake

## as_functions.py
A test script with different functions testing how to start up a series of background import jobs and monitor their progress

## ASpace_Data_Audit.py
A series of SQL queries, API calls, and exports to generate a spreadsheet for data cleanup.

## aspace_migration.py
This script runs a gamut of different cleanup functions against ArchivesSpace after UGA's migration from Archivists' Toolkit

## check_aspace_aos.py
This script checks all archival objects in ArchivesSpace and checks to see what objects are listed as collections, as well as updating ms3789 to change its objects from 'collection' to 'file'

## check_child_counts.py
This script checks how many children a parent object has in ArchivesSpace and if the number of children is equal to or greater than 1000, logs them in a .csv file

## check_enumerations.py
This script checks a standard list of controlled vocabularly lists and updates ArchivesSpace by deleting or merging values

## check_file_levels.py
This script was checking for parent files (archival objects with children) that did not have Instances or top containers. It's confusing.

## check_urls.py
This script exported all published resources from ASpace as an EAD.xml file, then took those files and looked for any URLs that were present, checked their HTTP status and if it returned an error (anything but 200), then logged the error in a spreadsheet. This was later adapted to make the Check URLs custom report plugin for ArchivesSpace.

## delete_unknown_containers.py
This script checks archival objects for specific resources in ArchivesSpace and if they have an 'unknown_container' as the value of their indicator, then it deletes that object

## export_all_resources.py
This script exports all published resources for every repository in an ArchivesSpace instance and assigns a concatenated version of the identifier as the filename

## find_unknown_containers.py
This script finds parent archival objects that have 'unknown container' in their identifier and logs it into a spreadsheet

## generate_subject-agent_list.py
This script writes all subjects and agents to a spreadsheet with their title and URI. This script was made as the first step in a project to cleanup subjects and agents in ArchivesSpace. The final step is outlined in update_subjects_agents.py

## hargrett_cleanup_script.sql
This runs several cleanup operations on our data before migration from Archivists' Toolkit to ArchivesSpace. It updates digital objects to change their repository based on their METS Identifier, delete component unique identifier (aka subdivisionIdentifier) content in that field, replaces leftover xml namespaces from note contents, set resource level to file when it is collection, and update specific digital objects to University Archives (repository 6)

## link_subjects_resources.py
This script grabs subjects from the ArchivesSpace database and their links to all resources and generates a spreadsheet with that info

## multiple_top_containers.sql
This grabs published archival objects with multiple top container instances attached to it

## pre_migration_cleanup.py
This script attempts to run SQL updates on Archivists' Toolkit databases for cleanup before migrating to ArchivesSpace

## publish_do_fvs.py
This script publishes all digital object file versions

## publish_dos.py
This script publishes all digital objects

## resources_wout_creators.py
This script checks all resources in an ArchivesSpace instance and makes an excel spreadsheet with those without creators

## russell_av_containers.sql
This grabs all top containers with instance types that are either "moving_images" or "audio" for the Russell repository

## russell_cleanup_script.sql
This runs several cleanup operations on our data for the Russell repository before migration from Archivists' Toolkit to ArchivesSpace. It updates FileVersions Use Statements to Audio-Streaming, changed Digital Object Show attribute to onLoad instead of replace, replaces leftover xml namespaces from note contents, and sets instance and extent types for some stubborn items.

## test_exports.py
This script tests the exports from the ArchivesSpace API

## top_containers_no_barcode.sql
This grabs all top containers that have no barcodes and are associated with published archival objects and resources

## unpublish_records.py
This script unpublishes resources in ArchivesSpace when they have a [CLOSED] in the resource id

## update_agentdates.py
This script takes info from the Dates of Existence and puts them in the Dates field to display when exporting

## update_containers.py
This script updates ArchivesSpace containers from a spreadsheet

## update_ms30002f.py
This script transfers a series of archival objects from ms3000_2e to ms3000_2f at the top level

## update_subjects_agents.py
This scirpt deletes and merges subjects from a spreadsheet
