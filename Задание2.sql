SELECT
    korpus_id,
    section,
    AVG(square) AS average_square,
    SUM(price * square) / SUM(square) AS weighted_average_price
FROM
    buildings
GROUP BY
    korpus_id, section;


SELECT
    room_type,
    COUNT(*) AS count_of_apartments
FROM
    buildings
WHERE
    korpus_id = ‘K0003901'
GROUP BY
    room_type;


SELECT DISTINCT
    b.korpus_id,
    s.sales_object_id
FROM
    buildings AS b
LEFT JOIN
    sales_objects AS s
ON
    b.korpus_id = s.korpus_id;

