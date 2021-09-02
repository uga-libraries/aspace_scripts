/*This grabs published archival objects with multiple top container instances attached to it*/

SELECT
    repository.name AS Repository,
    instance.archival_object_id,
    ao.ref_id, ao.title,
    COUNT(*)
FROM
    instance
JOIN
    archival_object AS ao
        ON ao.id = instance.archival_object_id
JOIN
    repository
        ON repository.id = ao.repo_id
WHERE
    ao.publish is True
    AND instance.instance_type_id != 349
GROUP BY
    instance.archival_object_id
HAVING
    count(archival_object_id) > 1