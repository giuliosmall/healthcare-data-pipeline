-- Drop existing data marts if they exist
DROP TABLE IF EXISTS united_healthcare_data;
DROP TABLE IF EXISTS humana_data;

-- criteria for UnitedHealthcare
SELECT
    COUNT(*)
FROM
    encounters AS e
LEFT JOIN
    payers pa
    ON e.payer = pa.id
WHERE
    pa.name = 'UnitedHealthcare'
    AND e.payer_coverage = 0;

-- data mart for UnitedHealthcare
CREATE TABLE united_healthcare_data AS
    SELECT DISTINCT
        e.id,
        e.code,
        e.patient,
        e.base_encounter_cost,
        e.payer,
        e.description
    FROM
        encounters AS e
    LEFT JOIN
        payers AS pa
        ON e.payer = pa.id
    WHERE
        pa.name = 'UnitedHealthcare'
        AND e.payer_coverage = 0
    ORDER BY
        e.id ASC;

-- criteria for Humana
SELECT
    COUNT(*)
FROM
    encounters AS e
LEFT JOIN
    payers AS pa
    ON e.payer = pa.id
WHERE
    pa.name = 'Humana'
    AND e.payer_coverage = 0;

-- data mart for Humana
CREATE TABLE humana_data AS
    SELECT DISTINCT
        e.id,
        e.code,
        e.patient,
        e.base_encounter_cost,
        e.payer,
        e.description
    FROM
        encounters AS e
    LEFT JOIN
        payers AS pa
        ON e.payer = pa.id
    WHERE
        pa.name = 'Humana'
        AND e.payer_coverage = 0
    ORDER BY
        e.id ASC;

-- rank payers by costs paid
CREATE TABLE payer_ranking AS
    SELECT
        pa.name,
        SUM(e.base_encounter_cost) AS total_cost
    FROM
        encounters AS e
    LEFT JOIN
        payers AS pa
        ON e.payer = pa.id
    GROUP BY
        pa.name
    ORDER BY
        total_cost DESC;

-- get top 5 highest costing patients
CREATE TABLE top_5_patients AS
    SELECT
        e.patient,
        SUM(e.base_encounter_cost) AS total_cost
    FROM
        encounters AS e
    GROUP BY
        e.patient
    ORDER BY
        total_cost DESC
    LIMIT 5;

-- get top 5 most expensive procedures on a daily basis by median
CREATE TABLE top_5_procedures_daily AS
    SELECT
        DATE_TRUNC('day', e.start::TIMESTAMP) AS procedure_day,
        e.code,
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY e.base_encounter_cost) AS median_cost
    FROM
        encounters AS e
    GROUP BY
        procedure_day,
        e.code
    ORDER BY
        procedure_day DESC,
        median_cost DESC
    LIMIT 5;