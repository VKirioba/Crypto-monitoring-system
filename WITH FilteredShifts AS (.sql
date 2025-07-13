WITH FilteredShifts AS (
    SELECT 
        w.shop_id, 
        SUM(TIMESTAMPDIFF(HOUR, w.start_time, w.end_time)) AS total_hours
    FROM WorkShift w
    WHERE w.start_time < '2025-02-24'
      AND w.end_time > DATE_SUB('2025-02-24', INTERVAL 28 DAY)
    GROUP BY w.shop_id
    HAVING total_hours > 0
),
FilteredSales AS (
    SELECT 
        w.shop_id, 
        SUM(p.price * sa.quantity_sold) AS total_sales
    FROM WorkShift w
    JOIN Sale sa ON w.shift_id = sa.shift_id
    JOIN Product p ON sa.product_id = p.product_id
    WHERE sa.sale_time >= DATE_SUB('2025-02-24', INTERVAL 28 DAY)
      AND sa.sale_time <= '2025-02-24'
    GROUP BY w.shop_id
),
Productivity AS (
    SELECT 
        s.shop_name, 
        COALESCE(fs.total_sales, 0) / fsh.total_hours AS productivity
    FROM FilteredShifts fsh
    JOIN Shop s ON fsh.shop_id = s.shop_id
    LEFT JOIN FilteredSales fs ON fsh.shop_id = fs.shop_id
)
SELECT 
    shop_name, 
    productivity, 
    'Highest' AS productivity_rank
FROM Productivity
ORDER BY productivity DESC
LIMIT 1

UNION ALL

SELECT 
    shop_name, 
    productivity, 
    'Lowest' AS productivity_rank
FROM Productivity
ORDER BY productivity ASC
LIMIT 1;