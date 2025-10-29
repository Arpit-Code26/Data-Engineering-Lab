import pandas as pd
from faker import Faker
from sqlalchemy import create_engine
import random
import time

print("Script started...")

# --- 1. SET UP DATABASE CONNECTION ---
# !! IMPORTANT: Replace 'YOUR_PASSWORD' with your actual PostgreSQL password
# Format: "postgresql://username:password@hostname:port/database_name"
db_url = "postgresql://postgres:arpit@localhost:5432/retail_project_db"

try:
    engine = create_engine(db_url)
    print("Database connection established.")
except Exception as e:
    print(f"Error connecting to database: {e}")
    exit()

fake = Faker()

# --- 2. GENERATE DIM_STORE ---
print("Generating dim_store data...")
stores_data = []
regions = ["North", "South", "East", "West"]
for i in range(1, 11): # 10 Stores
    city = fake.city()
    # FIX: All dictionary keys are now lowercase
    stores_data.append({
        "store_code": f"STORE-{i:03d}",
        "store_name": f"{city} Central Store",
        "city": city,
        "region": random.choice(regions)
    })
df_stores = pd.DataFrame(stores_data)

# --- 3. GENERATE DIM_PRODUCT ---
print("Generating dim_product data...")
products_data = []
categories = ["Electronics", "Clothing", "Home Goods", "Groceries", "Toys"]
brands = ["BrandA", "BrandB", "BrandC", "BrandD"]
for i in range(1, 101): # 100 Products
    # FIX: All dictionary keys are now lowercase
    products_data.append({
        "sku": f"SKU-{i:04d}",
        "product_name": fake.catch_phrase(), # This is the fix for the faker attribute
        "category": random.choice(categories),
        "brand": random.choice(brands)
    })
df_products = pd.DataFrame(products_data)

# --- 4. GENERATE DIM_DATE ---
print("Generating dim_date data...")
start_date = pd.to_datetime('now').date() - pd.DateOffset(days=730)
end_date = pd.to_datetime('now').date()

df_dates = pd.DataFrame({"full_date": pd.date_range(start_date, end_date)})
df_dates["full_date"] = df_dates["full_date"].dt.date

# FIX: All new column names are now lowercase
df_dates["year"] = df_dates["full_date"].apply(lambda x: x.year)
df_dates["month"] = df_dates["full_date"].apply(lambda x: x.month)
df_dates["day"] = df_dates["full_date"].apply(lambda x: x.day)
df_dates["quarter"] = df_dates["full_date"].apply(lambda x: pd.to_datetime(x).quarter)
df_dates["day_of_week"] = df_dates["full_date"].apply(lambda x: pd.to_datetime(x).day_name())

# --- 5. LOAD DATA TO POSTGRESQL ---
try:
    start_time = time.time()
    print("Loading dim_store...")
    # FIX: Table name is 'dim_store' and we use 'append'
    df_stores.to_sql('dim_store', engine, if_exists='append', index=False)
    
    print("Loading dim_product...")
    # FIX: Table name is 'dim_product' and we use 'append'
    df_products.to_sql('dim_product', engine, if_exists='append', index=False)
    
    print("Loading dim_date...")
    # FIX: Table name is 'dim_date' and we use 'append'
    df_dates.to_sql('dim_date', engine, if_exists='append', index=False)
    
    end_time = time.time()
    print(f"All dimension tables loaded successfully in {end_time - start_time:.2f} seconds.")

except Exception as e:
    print(f"Error loading data to database: {e}")

print("Script finished.")