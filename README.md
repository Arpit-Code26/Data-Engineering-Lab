
# Data Modeling for Analytics (DDMA)

This project demonstrates a retail transactional database with customers, products, and sales tables. It supports basic data integrity and enables key business analytics like monthly revenue and average order value (AOV).

## Features

- Designed schema with foreign key constraints for referential integrity
- Includes generated columns and data type checks
- Populates tables with sample realistic data for testing
- Provides sample analytics queries for monthly revenue and AOV
- Joins sales with customers and products for detailed transaction views

## Database Schema

- `customers`: Stores customer info (name, contact, address)
- `products`: Stores product catalog info (name, price, stock)
- `sales`: Stores transactional sales data with foreign keys to customers and products

## How to Use

1. Run the provided SQL script to create the database, tables, and insert sample data.
2. Execute the sample queries to verify data counts and perform analytics.
3. Customize schema or queries as needed for your application.

## Sample Queries

- Count total customers, products, sales
- Calculate monthly revenue grouped by sale month
- Calculate average order value (AOV) by month
- View recent sales joined with customer and product details

***

