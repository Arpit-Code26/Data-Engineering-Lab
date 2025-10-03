import pandas as pd
import random
from faker import Faker
from sqlalchemy import create_engine
import matplotlib.pyplot as plt

# --- 1. CAPTURE: Generate Synthetic Data ---
print("Step 1: Generating synthetic data...")
fake = Faker()
data = []
for i in range(100):
  data.append({
      "transaction_id": i + 1,
      "product_id": random.randint(1, 20),
      "customer_id": random.randint(1, 50),
      "quantity": random.randint(1, 5),
      "price": round(random.uniform(50, 500), 2),
      "timestamp": fake.date_time_this_year()
  })
df = pd.DataFrame(data)
print("Data generated successfully.")
print("-" * 30)


# --- 2. STORE: Load Data into PostgreSQL ---
print("Step 2: Storing data in PostgreSQL...")
try:
    # !!! IMPORTANT: Replace 'arpit' with your actual PostgreSQL password. !!!
    engine = create_engine("postgresql+psycopg2://postgres:arpit@localhost/retail_db")
    
    # 'if_exists="replace"' will delete the old table and create a new one.
    # This is useful for re-running the script during testing.
    df.to_sql("transactions", engine, if_exists="replace", index=False)
    print("Data stored successfully!")
except Exception as e:
    print(f"An error occurred: {e}")
    print("Could not connect to the database. Please check these things:")
    print("1. Is your PostgreSQL server running?")
    print("2. Is the password in the script correct?")
    exit() # Stop the script if it can't connect
print("-" * 30)


# --- 3. PROCESS: Transform Data ---
print("Step 3: Processing data (adding total_amount column)...")
df["total_amount"] = df["quantity"] * df["price"]
print("Processing complete.")
print("-" * 30)


# --- 4. ANALYZE: Query Data for Insights ---
print("Step 4: Analyzing data...")
query = "SELECT product_id, SUM(quantity * price) as total_sales FROM transactions GROUP BY product_id ORDER BY product_id"
sales_df = pd.read_sql(query, engine)
print("Analysis complete. Here are the total sales per product:")
print(sales_df)
print("-" * 30)


# --- 5. VISUALIZE: Create a Chart ---
print("Step 5: Visualizing results...")
plt.figure(figsize=(12, 6)) # Make the plot window a bit bigger
plt.bar(sales_df["product_id"], sales_df["total_sales"], color='skyblue')
plt.xlabel("Product ID")
plt.ylabel("Total Sales ($)")
plt.title("Total Sales per Product")
plt.xticks(sales_df["product_id"]) # Ensure all product IDs are shown on the x-axis
plt.grid(axis='y', linestyle='--', alpha=0.7)

# The script will pause here until you close the plot window.
print("Displaying plot. Close the plot window to end the script.")
plt.show()

print("\nPipeline execution finished successfully!")