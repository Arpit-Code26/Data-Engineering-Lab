
## Project Overview
This Python project implements a scheduled ETL pipeline to fetch weather data for multiple cities from a public API, validate and deduplicate the data, and store it in MongoDB. It also performs daily aggregations such as minimum, maximum, and average temperatures per city for analytical queries.

## Features
- Fetches current weather data for multiple cities.
- Validates data and prevents duplicates.
- Stores raw and aggregated weather data in MongoDB.
- Aggregates daily statistics using MongoDB pipelines.
- Scheduling to automate data ingestion at configured intervals.

## Technologies
- Python
- MongoDB
- OpenWeatherMap API
- `requests`, `pymongo`, `schedule` Python libraries

## Setup Instructions
1. Install MongoDB and start the database server.
2. Obtain an API key from OpenWeatherMap.
3. Install required Python packages:
   ```
   pip install requests pymongo schedule
   ```
4. Configure API key, city list, and MongoDB connection string in the Python script.
5. Run the script to start the scheduled ETL jobs.

## Usage
Run the Python script to begin scheduled data ingestion, validation, and storage. Monitor output in the terminal and query MongoDB collections `weather_raw` and `weather_summary` to analyze data.

