import pandas as pd
from sqlalchemy import create_engine
import random
import time

print("Fact loading script started...")

# --- 1. SET UP DATABASE CONNECTION ---
# !! IMPORTANT: Replace 'YOUR_PASSWORD' with your actual PostgreSQL password
db_url = "postgresql://postgres:arpit@localhost:5432/retail_project_db"

try:
    engine = create_engine(db_url)
    print("Database connection established.")
except Exception as e:
    print(f"Error connecting to database: {e}")
    exit()

# --- 2. ETL (Transform): FETCH LOOKUP MAPS ---
# We read our dimension tables from the database to create
# "lookup maps". This allows us to replace business keys
# (like 'STORE-001') with surrogate keys (like 1).

print("Fetching lookup maps from dimension tables...")
try:
    # Store Map: {'STORE-001': 1, 'STORE-002': 2, ...}
    df_store_lookup = pd.read_sql('SELECT store_id, store_code FROM dim_store', engine)
    store_map = df_store_lookup.set_index('store_code')['store_id'].to_dict()
    
    # Product Map: {'SKU-0001': 1, 'SKU-0002': 2, ...}
    df_prod_lookup = pd.read_sql('SELECT product_id, sku FROM dim_product', engine)
    product_map = df_prod_lookup.set_index('sku')['product_id'].to_dict()

    # Date Map: {Timestamp('2023-01-01'): 1, ...}
    df_date_lookup = pd.read_sql('SELECT date_id, full_date FROM dim_date', engine)
    # Convert full_date to simple date objects for mapping
    df_date_lookup['full_date'] = pd.to_datetime(df_date_lookup['full_date']).dt.date
    date_map = df_date_lookup.set_index('full_date')['date_id'].to_dict()

    print("Lookup maps created successfully.")
except Exception as e:
    print(f"Error fetching lookup maps: {e}")
    exit()
    
# --- 3. ETL (Extract): SIMULATE RAW SALES DATA ---
print("Simulating raw sales transactions...")

# Get lists of valid keys to use in simulation
store_codes = list(store_map.keys())
skus = list(product_map.keys())
dates = list(date_map.keys())

raw_sales_data = []
num_transactions = 20000  # Generate 20,000 sales

for _ in range(num_transactions):
    # Pick random business keys
    store_code = random.choice(store_codes)
    sku = random.choice(skus)
    date = random.choice(dates)
    
    quantity = random.randint(1, 5)
    cost = round(random.uniform(5.0, 500.0), 2)
    # Add a random markup for the sales price (1.2x to 1.5x)
    price = round(cost * random.uniform(1.2, 1.5), 2)
    
    # Note: all keys are lowercase
    raw_sales_data.append({
        "store_code": store_code,
        "sku": sku,
        "date": date,
        "quantity_sold": quantity,
        "cost_of_goods_sold": cost * quantity,
        "sales_amount": price * quantity
    })
    
df_raw_sales = pd.DataFrame(raw_sales_data)
print(f"Simulated {num_transactions} raw sales.")

# --- 4. ETL (Transform): APPLY LOOKUPS & CALCULATE ---
print("Transforming raw sales data...")

# This is the core "Transform" step
# We use .map() to replace business keys with surrogate keys
df_raw_sales['store_id'] = df_raw_sales['store_code'].map(store_map)
df_raw_sales['product_id'] = df_raw_sales['sku'].map(product_map)
df_raw_sales['date_id'] = df_raw_sales['date'].map(date_map)

# Calculate Profit
df_raw_sales['profit'] = df_raw_sales['sales_amount'] - df_raw_sales['cost_of_goods_sold']

# Select only the columns needed for the fact_sales table
df_fact_sales = df_raw_sales[[
    "quantity_sold",
    "sales_amount",
    "cost_of_goods_sold",
    "profit",
    "store_id",
    "product_id",
    "date_id"
]]

# Handle any potential nulls if a map failed (good practice)
df_fact_sales = df_fact_sales.dropna()

print("Transformation complete.")

# --- 5. ETL (Load): LOAD TO FACT TABLE ---
try:
    start_time = time.time()
    print("Loading data into fact_sales...")
    
    # Use if_exists='append' so we can add more data later
    df_fact_sales.to_sql('fact_sales', engine, if_exists='append', index=False)
    
    end_time = time.time()
    print(f"FactSales table loaded successfully in {end_time - start_time:.2f} seconds.")

except Exception as e:
    print(f"Error loading fact data to database: {e}")

print("Script finished.")