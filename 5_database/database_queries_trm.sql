USE inventorymanagement;

-- Total Revenue by Month

SELECT 
    MONTH(i.invoicedate) AS month, 
    SUM(ii.quantity * p.unitprice) AS total_revenue
FROM 	
    InvoiceItems ii
JOIN 
    Invoices i ON ii.invoiceno = i.invoiceno
JOIN 
    Products p ON ii.stockcode = p.stockcode
GROUP BY 
    month
ORDER BY 
    month ASC;