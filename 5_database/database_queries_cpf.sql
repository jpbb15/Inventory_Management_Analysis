USE inventorymanagement; 

-- Customer Purchase Frequency

SELECT 
    c.customerid, 
    COUNT(DISTINCT i.invoiceno) AS purchase_count
FROM 
    Invoices i
JOIN 
    Customers c ON i.customerid = c.customerid
GROUP BY 
    c.customerid
ORDER BY 
    purchase_count DESC
LIMIT 10;