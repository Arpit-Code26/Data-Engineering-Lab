
# Automated Weather Data Ingestion and Storage in PostgreSQL

## Description
This project automatically fetches current weather data for a specified city using a public weather API and stores the data in a PostgreSQL database. It provides a basis for future weather data analysis.

## Requirements
- Python 3.x environment
- PostgreSQL database installed and configured
- Necessary Python libraries installed

## Setup Instructions
- Create the PostgreSQL database and required tables.
- Configure the database connection parameters.
- Obtain an API key from the weather service provider.
- Set up the environment to run the Python ingestion script.

## Usage
Run the script to fetch and store weather data regularly. The data is saved in a structured format for easy querying and analysis.

## Notes
- Ensure the database service is running before executing the script.
- Use secure handling of API keys and database credentials.
- Schedule periodic execution using task schedulers as needed.

