/* Finds electronic record accessions and their linked resources */

SELECT
	repo.name as Repository,
	acc.title as ER_Accession_Title, 
    acc.identifier as ER_Accession_ID, 
    acc.accession_date as ER_Accession_Date, 
    concat(extent.number, ' ', ev.value) as ER_Accession_Extent, 
    resource.identifier as Related_Resource # concat(JSON_EXTRACT(resource.identifier,'$[0]'), nullif()) AS Resource_ID 
FROM 
	accession as acc
JOIN 
	extent 
		ON extent.accession_id = acc.id
JOIN 
	enumeration_value as ev 
		ON ev.id = extent.extent_type_id
JOIN 
	spawned_rlshp as sr 
		ON sr.accession_id = acc.id
JOIN 
	resource 
		ON resource.id = sr.resource_id
JOIN
	repository as repo
		ON repo.id = resource.repo_id
WHERE 
	LOCATE('ER', acc.identifier)