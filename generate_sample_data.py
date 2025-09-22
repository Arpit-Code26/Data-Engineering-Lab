import psycopg2
import datetime
import random

# PostgreSQL credentials
DB_HOST = "localhost"
DB_NAME = "weather_db"
DB_USER = "postgres"
DB_PASSWORD = "arpit"  # Replace with your password

CITY = "Pune"

def generate_sample_data():
    base_date = datetime.datetime.now() - datetime.timedelta(days=30)
    sample_data = []

    for day in range(30):
        date = base_date + datetime.timedelta(days=day)
        # Generate realistic sample weather values
        temperature = round(random.uniform(25, 35), 1)  # °C
        humidity = random.randint(40, 80)               # %
        pressure = random.randint(990, 1025)            # hPa
        wind_speed = round(random.uniform(1.0, 5.0), 1) # m/s
        description = random.choice([
            "clear sky", "few clouds", "scattered clouds",
            "broken clouds", "shower rain", "rain", "thunderstorm",
            "snow", "mist"
        ])

        sample_data.append({
            "city": CITY,
            "date_time": date,
            "temperature": temperature,
            "humidity": humidity,
            "pressure": pressure,
            "weather_description": description,
            "wind_speed": wind_speed
        })

    return sample_data

def insert_sample_data(sample_data):
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conn.cursor()
        insert_query = """
            INSERT INTO weather_data
            (city, date_time, temperature, humidity, pressure, weather_description, wind_speed)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        for entry in sample_data:
            cursor.execute(insert_query, (
                entry['city'], entry['date_time'], entry['temperature'],
                entry['humidity'], entry['pressure'], entry['weather_description'],
                entry['wind_speed']
            ))
        conn.commit()
        cursor.close()
        conn.close()
        print("Sample data inserted successfully.")
    except Exception as e:
        print("Error inserting sample data:", e)

if __name__ == "__main__":
    data = generate_sample_data()
    insert_sample_data(data)
