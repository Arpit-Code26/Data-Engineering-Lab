import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sqlalchemy import create_engine

DB_USER = "postgres"
DB_PASSWORD = "arpit"  # Replace with your password
DB_HOST = "localhost"
DB_NAME = "weather_db"
CITY = "Pune"

def fetch_data():
    try:
        connection_string = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
        engine = create_engine(connection_string)
        query = """
            SELECT date_time, temperature
            FROM weather_data
            WHERE city = %s AND date_time >= NOW() - INTERVAL '30 days'
            ORDER BY date_time;
        """
        df = pd.read_sql_query(query, engine, params=(CITY,))
        return df
    except Exception as e:
        print("Error fetching data:", e)
        return None

def train_and_predict(df):
    # Create a column for next day's temperature (shifted by -1)
    df['temp_next_day'] = df['temperature'].shift(-1)
    df = df.dropna()

    X = df[['temperature']]
    y = df['temp_next_day']

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Create and train linear regression model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Predict on test data
    y_pred = model.predict(X_test)

    mse = mean_squared_error(y_test, y_pred)
    print(f"Mean Squared Error: {mse:.3f}")

    # Predict next day's temperature based on last available temperature
    last_temp = np.array(df['temperature'].iloc[-1]).reshape(1, -1)
    import pandas as pd
    predicted_temp = model.predict(pd.DataFrame(last_temp, columns=['temperature']))

    print(f"Predicted temperature for next day: {predicted_temp[0]:.2f} °C")

if __name__ == "__main__":
    data = fetch_data()
    if data is not None and not data.empty:
        train_and_predict(data)
    else:
        print("Insufficient data for prediction.")
