USE inventorymanagement;

-- Most Popular Products (Overall)

SELECT 
    p.stockcode, 
    p.description, 
    SUM(ii.quantity) AS total_quantity_sold
FROM 
    InvoiceItems ii
JOIN 
    Products p ON ii.stockcode = p.stockcode
GROUP BY 
    p.stockcode, p.description
ORDER BY 
    total_quantity_sold DESC
LIMIT 10;



