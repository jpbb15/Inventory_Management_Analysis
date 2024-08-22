CREATE DATABASE InventoryManagement;
USE InventoryManagement;

CREATE TABLE Customers (
    customerid INT PRIMARY KEY,
    country VARCHAR(255)
);

CREATE TABLE Products (
    stockcode VARCHAR(255) PRIMARY KEY,
    description VARCHAR(255),
    unitprice DECIMAL(10, 2)
);

CREATE TABLE Invoices (
    invoiceno VARCHAR(255) PRIMARY KEY,
    invoicedate DATETIME,
    customerid INT,
    FOREIGN KEY (customerid) REFERENCES Customers(customerid)
);

CREATE TABLE InvoiceItems (
    id INT PRIMARY KEY AUTO_INCREMENT,
    invoiceno VARCHAR(255),
    stockcode VARCHAR(255),
    quantity INT,
    FOREIGN KEY (invoiceno) REFERENCES Invoices(invoiceno),
    FOREIGN KEY (stockcode) REFERENCES Products(stockcode)
);
