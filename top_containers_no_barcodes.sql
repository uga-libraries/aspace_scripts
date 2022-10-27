/* This grabs all top containers that have no barcodes and are associated with published archival objects and
 resources
*/

SELECT DISTINCT
    repo.name AS Repository,
    ao.title AS Linked_Archival_Object_Title,
    ao.ref_id AS Linked_Archival_Object_REFID,
    top_container.indicator, ev.value, location.title AS Location
FROM
    top_container
JOIN
    top_container_link_rlshp AS top_rlsh
        ON top_rlsh.top_container_id = top_container.id
JOIN
    sub_container
        ON top_rlsh.sub_container_id = sub_container.id
JOIN
    instance
        ON instance.id = sub_container.instance_id
JOIN
    archival_object AS ao
        ON ao.id = instance.archival_object_id
JOIN
    repository AS repo
        ON repo.id = ao.repo_id
JOIN
    resource
        ON resource.id = ao.root_record_id
JOIN
    enumeration_value AS ev
        ON ev.id = top_container.type_id
LEFT JOIN
	top_container_housed_at_rlshp AS contloc
		ON top_container.id = contloc.top_container_id
LEFT JOIN
	location
		ON location.id = contloc.location_id
WHERE
    top_container.barcode is NULL
    AND ao.publish is true
    AND resource.publish is true