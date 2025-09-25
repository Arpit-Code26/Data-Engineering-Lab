import requests
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus
from datetime import date

API_KEY = "8adda756db2fa1af4ae49ad2cc00a42a"  # Replace this
CITY = "London"  # Replace this with your city

USER = "root"
PASSWORD = "arpit"  # Replace this
HOST = "127.0.0.1"
PORT = 3306
DB = "DDMA"

conn_str = f"mysql+pymysql://{USER}:{quote_plus(PASSWORD)}@{HOST}:{PORT}/{DB}"

def fetch_weather():
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": CITY, "appid": API_KEY, "units": "metric"}
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    return {
        "weather_date": date.today(),
        "city": CITY,
        "temp_c": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "description": data["weather"][0]["description"],
    }

def store_weather(weather_data):
    engine = create_engine(conn_str)
    with engine.begin() as conn:
        sql = text("""
        INSERT INTO weather (weather_date, city, temp_c, humidity, description)
        VALUES (:weather_date, :city, :temp_c, :humidity, :description)
        ON DUPLICATE KEY UPDATE
            temp_c = VALUES(temp_c),
            humidity = VALUES(humidity),
            description = VALUES(description);
        """)
        conn.execute(sql, weather_data)
    print("Weather data inserted/updated successfully.")

if __name__ == "__main__":
    weather = fetch_weather()
    store_weather(weather)
