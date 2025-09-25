import requests
from pymongo import MongoClient, ASCENDING
from datetime import datetime, timezone
import schedule
import time

# Configurations
API_KEY = "8adda756db2fa1af4ae49ad2cc00a42a"
CITIES = ["Dehradun", "Jaipur", "Patna", "Tokyo"]  # List of cities
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "weather_db"
COLLECTION_RAW = "weather_raw"
COLLECTION_SUMMARY = "weather_summary"

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
raw_collection = db[COLLECTION_RAW]
summary_collection = db[COLLECTION_SUMMARY]

# Create indexes for query efficiency
raw_collection.create_index([("city", ASCENDING), ("date", ASCENDING)], unique=True)
summary_collection.create_index("city", unique=True)

def fetch_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return {
        "date": datetime.now(timezone.utc),
        "city": city,
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "description": data["weather"][0]["description"]
    }

def validate_data(new_data):
    if not new_data.get("city") or not isinstance(new_data.get("temperature"), (int, float)):
        return False
    if new_data["temperature"] < -50 or new_data["temperature"] > 60:
        return False
    return True

def upsert_raw_data(data):
    query = {"city": data["city"], "date": {"$gte": datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)}}
    if raw_collection.find_one(query):
        print(f"Skipping duplicate data for {data['city']} today.")
        return
    raw_collection.insert_one(data)
    print(f"Inserted raw data for {data['city']}.")

def aggregate_daily_summary():
    pipeline = [
        {
            "$match": {
                "date": {
                    "$gte": datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
                }
            }
        },
        {
            "$group": {
                "_id": "$city",
                "min_temp": {"$min": "$temperature"},
                "max_temp": {"$max": "$temperature"},
                "avg_temp": {"$avg": "$temperature"},
                "count": {"$sum": 1}
            }
        }
    ]

    results = raw_collection.aggregate(pipeline)
    for res in results:
        city = res["_id"]
        summary_collection.update_one(
            {"city": city},
            {
                "$set": {
                    "date": datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0),
                    "min_temp": res["min_temp"],
                    "max_temp": res["max_temp"],
                    "avg_temp": round(res["avg_temp"], 2),
                    "record_count": res["count"]
                }
            },
            upsert=True
        )
        print(f"Updated daily summary for {city}")

def run_etl():
    for city in CITIES:
        try:
            weather = fetch_weather(city)
            if validate_data(weather):
                upsert_raw_data(weather)
            else:
                print(f"Invalid data for {city}, skipping.")
        except Exception as e:
            print(f"Error fetching weather for {city}: {e}")
    aggregate_daily_summary()

# Run ETL job immediately once on start
run_etl()


schedule.every(10).seconds.do(run_etl)


print("Starting scheduled ETL job...")
while True:
    schedule.run_pending()
    time.sleep(1)
