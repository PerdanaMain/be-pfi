WITH RECURSIVE equipment_hierarchy AS (
    -- Base case: get root level equipment (parent_id is null or top level)
    SELECT
        id,
        name,
        location_tag,
        parent_id,
        1 as level,
        ARRAY [name] as path
    FROM
        ms_equipment_master
    WHERE
        parent_id IS NULL -- atau kondisi untuk root level
    UNION
    ALL -- Recursive case: get children
    SELECT
        e.id,
        e.name,
        e.location_tag,
        e.parent_id,
        eh.level + 1,
        eh.path || e.name
    FROM
        ms_equipment_master e
        INNER JOIN equipment_hierarchy eh ON e.parent_id = eh.id
),
rp_oh_schedule AS (
    SELECT
        *
    FROM
        rp_oh_schedule
    WHERE
        year = '2025'
)
SELECT
    eh.id as equipment_id,
    eh.name as equipmentName,
    eh.location_tag as equipmentTag,
    eh.parent_id as parentId,
    eh.level as equipment_level,
    eh.path as equipment_path,
    pf_parts.id,
    pf_parts.equipment_id,
    pf_parts.part_name as sensorName,
    pf_parts.type_id,
    pf_parts.location_tag as sensorTag,
    pf_details.upper_threshold as tripThreshold,
    pf_details.lower_threshold as alarmThreshold,
    pf_details.time_failure as PFInterval,
    pf_details.predict_status as status,
    dl_ms_type.unit as unit,
    dl_features_data.value as currentValue,
    dl_features_data.date_time as currentValueDate,
    rp_oh_schedule.start as wostart,
    rp_oh_schedule.finish as wofinish,
    rp_oh_schedule.year as woyear
FROM
    equipment_hierarchy eh
    LEFT JOIN pf_parts ON pf_parts.equipment_id = eh.id
    LEFT JOIN pf_details ON pf_details.part_id = pf_parts.id
    LEFT JOIN dl_ms_type ON dl_ms_type.id = pf_parts.type_id
    LEFT JOIN (
        SELECT
            DISTINCT ON (part_id) part_id,
            value,
            date_time
        FROM
            dl_features_data
        ORDER BY
            part_id,
            date_time DESC
    ) dl_features_data ON dl_features_data.part_id = pf_parts.id
    CROSS JOIN rp_oh_schedule
ORDER BY
    eh.path,
    eh.level,
    equipmentName ASC;