import requests
import pandas as pd
from sqlalchemy import create_engine
from datetime import date

# Configurations
API_KEY = "8adda756db2fa1af4ae49ad2cc00a42a"  # Replace with your OpenWeatherMap API key
CITY = "Dehradun"  # Specify the city name

# PostgreSQL connection string
# Format: postgresql+psycopg2://username:password@host:port/database
PG_CONN_STRING = "postgresql+psycopg2://postgres:arpit@localhost:5432/sales_weather2_db" 
# Replace username and password accordingly

def fetch_weather(api_key, city):
    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={api_key}&units=metric"
    )
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    return {
        'weather_date': date.today(),
        'city': city,
        'temp_c': data['main']['temp'],
        'humidity': data['main']['humidity'],
        'description': data['weather'][0]['description'],
    }

def store_weather_to_db(weather_data, conn_string):
    engine = create_engine(conn_string)
    df = pd.DataFrame([weather_data])
    # Save into PostgreSQL "weather" table
    df.to_sql('weather', engine, if_exists='append', index=False)
    print(f"Weather data for {weather_data['city']} stored successfully in PostgreSQL.")

def main():
    weather = fetch_weather(API_KEY, CITY)
    store_weather_to_db(weather, PG_CONN_STRING)

if __name__ == "__main__":
    main()
