
# Weather-Sales Integration Project

## Overview
Integrate sales data with weather data in MySQL to analyze weather impact on sales using Python scripts in VS Code.

## Setup
- Use local MySQL to create and modify tables (`customers`, `products`, `sales`, `weather`).
- Add `weather_date` column and populate from `sale_date`.
- Insert manual sample weather data for testing historical dates.

## Development
- Use VS Code with Python extension.
- Install dependencies: `pip install requests sqlalchemy pymysql`
- Configure and run Python script to fetch current weather from OpenWeather API and upsert into MySQL.
- Use SQL queries to join and analyze sales with weather.

## Notes
- Manual data is for initial testing.
- API integration automates live weather updates.
- Extend script for multiple dates/cities if needed.


[9](https://bulldogjob.com/readme/how-to-write-a-good-readme-for-your-github-project)
[10](https://dev.to/kwing25/how-to-write-a-good-readme-for-your-project-1l10)
