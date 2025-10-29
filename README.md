# 🏬 Multi-Store Retail BI Data Model: A Data Engineering Project

## 📘 1. About This Project

This project showcases the creation of a **centralized data warehouse** for a fictional multi-store retailer using standard data engineering practices.  
The goal was to build a robust system capable of **consolidating scattered retail data (sales, stores, products)** into a **single source of truth**, optimized for **Business Intelligence (BI)** and analytics.

By bringing data together from simulated sources into **PostgreSQL** and organizing it with a **Star Schema**, this project enables fast, reliable analysis of performance across different stores, products, and time periods.

An **automated ETL pipeline (built with Python)** handles data extraction, cleaning, transformation (including key lookups), and loading.  
The final output is visualized through an interactive **Power BI dashboard**.

> **Field:** Data Engineering & Retail Business Intelligence (BI)

---

## 🧰 2. The Toolkit We Used

| Purpose | Tool |
|----------|------|
| **Code** | Python (with Pandas for data handling, Faker for data generation, SQLAlchemy for DB connections) |
| **Database** | PostgreSQL |
| **Visualization** | Power BI Desktop |
| **Workspace** | Visual Studio Code (with PostgreSQL extension) |

---

## 🌟 3. How the Data Fits Together (Star Schema Model)

The heart of the warehouse is the **Star Schema** – designed to be simple and fast for analytical queries.

### 🧮 Fact Table: `fact_sales`
Holds the main metrics:
- `quantity_sold`
- `sales_amount`
- `cost_of_goods_sold`
- `profit`

### 🧭 Dimension Tables:
- **`dim_store`** → Store details (store name, region)  
- **`dim_product`** → Product details (product name, category)  
- **`dim_date`** → Time details (year, month, day)

All tables follow **lowercase_snake_case** naming to avoid PostgreSQL case-sensitivity issues.  
`SERIAL` keys are used for primary and foreign keys to link everything efficiently.

📊 **Schema Overview:**

    dim_store          dim_product          dim_date
        │                   │                   │
        └──────────┬────────┴────────┬───────────┘
                   │   fact_sales   │
                   └────────────────┘

---

## ⚙️ 4. Getting the Data In (The ETL Pipeline)

The ETL (Extract, Transform, Load) process is automated using **two Python scripts**:

### 1️⃣ `1_load_dimensions.py`
- Creates realistic fake data for **stores**, **products**, and **dates**.
- Loads the clean “context” data into PostgreSQL.
- Database auto-generates numeric IDs.

### 2️⃣ `2_load_facts.py`
- Fetches unique IDs from the dimension tables (e.g., `store_id` for `'STORE-001'`).
- Generates raw sales data with store/product codes.
- **Transforms** codes into numeric IDs and calculates **profit**.
- Loads everything into `fact_sales`.

> ⚠️ **Run Order Matters:**  
> Always run `1_load_dimensions.py` **before** `2_load_facts.py`.  
> Facts depend on dimension tables being preloaded!

---

## ✅ 5. Did It Work? (Validation)

Before connecting Power BI, data validation was performed via **SQL joins and aggregations** in PostgreSQL.  
Example: Summarizing total profit by region proved that:
- Joins worked correctly  
- Foreign key relationships were intact  
- ETL pipeline was functioning as expected  

Confidence boost: 💪 **100%!**

---

## 📊 6. The Payoff: The Interactive Dashboard

The final result is an **interactive Power BI dashboard** connected directly to the PostgreSQL warehouse.

### Highlights:
- 🗺️ **Sales by Region:** Map visual showing store performance  
- 📈 **Profit Over Time:** Line chart of profit trends  
- 📊 **Top Products:** Bar chart ranking bestsellers  



## 🧠 7. What we Learned (Challenges & Wins)

### 💡 Key Takeaways:
- **Database Rules (Foreign Keys):** Learned why load order matters and how to safely reset tables using  
  ```sql
  TRUNCATE TABLE table_name CASCADE;
