CREATE DATABASE inventory_management;
USE inventory_management;

CREATE TABLE Customers (
    customerid INT PRIMARY KEY,
    country VARCHAR(255)
);

CREATE TABLE Products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    description VARCHAR(255),
    unitprice DECIMAL(10, 2)
);

CREATE TABLE Transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    invoicedate DATETIME,
    customerid INT,
    product_id INT,
    quantity INT,
    total_purchase DECIMAL(10, 2),
    FOREIGN KEY (customerid) REFERENCES Customers(customerid),
    FOREIGN KEY (product_id) REFERENCES Products(product_id)
);
