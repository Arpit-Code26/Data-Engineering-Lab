# Weather Data Engineering Capstone

This project builds a pipeline to fetch live weather data from OpenWeatherMap API, store it in PostgreSQL, visualize 30 days of weather trends in Pune, and forecast next-day temperature using a basic ML model.

## Project Files

- `insert_weather.py` — live weather data fetch and insert
- `generate_sample_data.py` — create synthetic historical data
- `visualize_weather.py` — plot 30 days weather trends
- `ml_forecast.py` — linear regression forecasting model

## How to Run

1. Set up PostgreSQL with database `weather_db` and table `weather_data`.  
2. Run `insert_weather.py` to fetch live data (or `generate_sample_data.py` for demo data).  
3. Run `visualize_weather.py` to view weather charts.  
4. Run `ml_forecast.py` to train and predict temperature.

## Screenshots

Screenshots demonstrating outputs are included .

