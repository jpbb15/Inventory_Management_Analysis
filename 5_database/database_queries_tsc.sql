USE inventorymanagement;

SELECT 
    c.country,
    SUM(ii.quantity * p.unitprice) AS total_revenue
FROM 
    InvoiceItems ii
JOIN 
    Invoices i ON ii.invoiceno = i.invoiceno
JOIN 
    Products p ON ii.stockcode = p.stockcode
JOIN 
    Customers c ON i.customerid = c.customerid
GROUP BY 
    c.country
ORDER BY 
    total_revenue DESC;
