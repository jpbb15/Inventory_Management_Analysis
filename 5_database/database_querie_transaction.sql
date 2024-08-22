USE inventory_management;

LOAD DATA LOCAL INFILE 'C:/Users/USER/Documents/GitHub/project_final/5_database/Data_CSV/transactions.csv'
INTO TABLE transactions
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(transaction_id, invoicedate, customerid, product_id, quantity, total_purchase);

