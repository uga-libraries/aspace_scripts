/* This grabs all top containers with instance types that are either "moving_images" or "audio" for the Russell
repository */

SELECT
    repo.name AS Repository,
    JSON_EXTRACT(resource.identifier,'$[0]') AS Resource_ID,
    ao.title AS Linked_Archival_Object_Title, 
    ao.ref_id AS Linked_Archival_Object_REFID, 
    top_container.indicator,
    ev.value
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
        ON ev.id = instance.instance_type_id
WHERE
    instance.instance_type_id = 354
    OR instance.instance_type_id = 346
    AND repo.id = 2