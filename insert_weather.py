import requests
import datetime
import time
import psycopg2

# PostgreSQL credentials
DB_HOST = "localhost"
DB_NAME = "weather_db"
DB_USER = "postgres"
DB_PASSWORD = "arpit"  # Replace with your password

# OpenWeatherMap API details
API_KEY = "8adda756db2fa1af4ae49ad2cc00a42a"  # Replace with your key

# Pune coordinates
LAT = 18.5204
LON = 73.8567

URL = "https://api.openweathermap.org/data/3.0/onecall/timemachine"

def fetch_weather_for_day(timestamp):
    params = {
        "lat": LAT,
        "lon": LON,
        "dt": timestamp,
        "appid": API_KEY,
        "units": "metric"
    }
    response = requests.get(URL, params=params)
    data = response.json()
    if response.status_code == 200:
        # return the hourly data (list)
        return data.get('data', []) or data.get('hourly', [])
    else:
        print(f"Failed to fetch data for timestamp {timestamp}: {data.get('message')}")
        return None

def insert_weather(weather):
    try:
        conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
        cursor = conn.cursor()
        insert_query = """
            INSERT INTO weather_data 
            (city, date_time, temperature, humidity, pressure, weather_description, wind_speed)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT DO NOTHING;
        """
        cursor.execute(insert_query, (
            weather['city'], weather['date_time'], weather['temperature'], weather['humidity'],
            weather['pressure'], weather['weather_description'], weather['wind_speed']
        ))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print("DB insert error:", e)

def main():
    print("Starting historical data fetch and insert...")
    today = datetime.datetime.utcnow()
    city = "Pune"
    # Fetch data for last 30 days
    for days_ago in range(1, 31):
        dt = today - datetime.timedelta(days=days_ago)
        timestamp = int(dt.replace(hour=12, minute=0, second=0, microsecond=0).timestamp())  # noon utc to get day's data
        print(f"Fetching data for: {dt.strftime('%Y-%m-%d')}")

        hourly_data = fetch_weather_for_day(timestamp)
        if hourly_data is None:
            continue

        # Insert hourly data points (can choose to average or pick specific hour)
        for hour_entry in hourly_data:
            weather = {
                "city": city,
                "date_time": datetime.datetime.utcfromtimestamp(hour_entry['dt']),
                "temperature": hour_entry.get('temp'),
                "humidity": hour_entry.get('humidity'),
                "pressure": hour_entry.get('pressure'),
                "weather_description": hour_entry.get('weather', [{}])[0].get('description', ''),
                "wind_speed": hour_entry.get('wind_speed')
            }
            insert_weather(weather)

        # To avoid hitting API rate limits
        time.sleep(1)

    print("Historical data fetching completed.")

if __name__ == "__main__":
    main()
