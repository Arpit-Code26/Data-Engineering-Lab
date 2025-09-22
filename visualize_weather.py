import psycopg2
import pandas as pd
import matplotlib.pyplot as plt

# PostgreSQL credentials
DB_HOST = "localhost"
DB_NAME = "weather_db"
DB_USER = "postgres"
DB_PASSWORD = "arpit"  # Replace with your password

CITY = "Pune"

def fetch_last_30_days():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        query = """
            SELECT date_time, temperature, humidity, pressure, wind_speed
            FROM weather_data
            WHERE city = %s AND date_time >= NOW() - INTERVAL '30 days'
            ORDER BY date_time;
        """
        df = pd.read_sql_query(query, conn, params=(CITY,))
        conn.close()
        return df
    except Exception as e:
        print("Error fetching data:", e)
        return None

def plot_temperature(df):
    plt.figure(figsize=(10,5))
    plt.plot(df['date_time'], df['temperature'], marker='o', linestyle='-')
    plt.title(f'Temperature Trend in {CITY} - Last 30 Days')
    plt.xlabel('Date')
    plt.ylabel('Temperature (°C)')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    df = fetch_last_30_days()
    if df is not None and not df.empty:
        plot_temperature(df)
    else:
        print("No data available for the last 30 days.")
