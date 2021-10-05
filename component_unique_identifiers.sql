/* This grabs all the archival objects that have a component unique identifier field */

SELECT
	repo.name AS Repository, 
	resource.identifier AS Resource_ID, 
	ao.ref_id AS Ref_ID, 
	ao.title AS Archival_Object_Title, 
	ao.component_id AS Component_Unique_Identifier
FROM 
	archival_object AS ao
JOIN
	repository AS repo 
		ON repo.id = ao.repo_id
JOIN
	resource
		ON resource.id = ao.root_record_id
WHERE 
	component_id is not Null
AND
	resource.publish is True
AND
	ao.publish is True