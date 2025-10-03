# Data Lifecycle Pipeline for Retail Transactions

## 1. Project Objective
This project demonstrates a complete, end-to-end data lifecycle pipeline for a retail scenario.  
The goal is to simulate the journey of data from its creation to its visualization, covering all key stages of data engineering.

---

## 2. Technologies Used
- **Language:** Python  
- **Database:** PostgreSQL  
- **Key Python Libraries:**
  - `pandas` for data manipulation  
  - `faker` for synthetic data generation  
  - `sqlalchemy` and `psycopg2` for database connection  
  - `matplotlib` for data visualization  

---

## 3. The Data Lifecycle Stages

### Stage 1: Capture
Synthetic retail transaction data was generated using a Python script (`data_generation.py`).  
Each transaction includes:
- `transaction_id`  
- `product_id`  
- `customer_id`  
- `quantity`  
- `price`  
- `timestamp`  

---

### Stage 2: Store
The generated data was loaded into a **PostgreSQL** database named `retail_db`,  
inside a table called `transactions`.  

📸 See screenshot: **`pgadmin_transactions.png`**

---

### Stage 3: Process
The data was processed in Python (`data_processing.py`) by creating a new derived column:  
- `total_amount = quantity * price`

---

### Stage 4: Analyze
SQL queries were executed on the database (`queries.sql`) to aggregate the data.  
Specifically, the **total sales amount for each product** was calculated to find out which products generate the most revenue.

---

### Stage 5: Visualize
The analyzed data was visualized using **matplotlib** (`visualization.py`) to create a bar chart  
showing the **total sales for each product ID**.  

📸 See screenshot: **`sales_visualization.png`**
