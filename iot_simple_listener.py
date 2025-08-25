import pandas as pd
import joblib
import paho.mqtt.client as mqtt
import sqlite3
import datetime

# --- 1. CONFIGURATION ---
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_TOPIC = "makeathon/rainwater/yahyaa/data"
DB_FILE = "water_data.db" # Database file
COLUMN_NAMES = ['ph', 'Solids']

# --- 2. LOAD THE SIMPLE MODEL & IMPUTER ---
try:
    model = joblib.load('simple_model.joblib')
    imputer = joblib.load('simple_imputer.joblib')
except FileNotFoundError:
    print("❌ Error: Model files not found. Run train_simple_model.py first.")
    exit()

# --- 3. DATABASE FUNCTIONS (NEW) ---
def setup_database():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS readings (
            timestamp TEXT, ph REAL, Solids REAL, prediction TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_reading(data_values, prediction_text):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data_to_insert = [timestamp] + data_values + [prediction_text]
    cursor.execute("INSERT INTO readings VALUES (?,?,?,?)", data_to_insert)
    conn.commit()
    conn.close()
    print(f"✅ Data saved to database: {DB_FILE}")

# --- 4. MQTT CALLBACK FUNCTION ---
def on_message(client, userdata, msg):
    data_string = msg.payload.decode('utf-8')
    print(f"\nReceived data: {data_string}")

    try:
        data_values = [float(x) for x in data_string.split(',')]
        if len(data_values) != 2:
            print(f"⚠️ Warning: Received {len(data_values)} values, expected 2.")
            return

        input_df = pd.DataFrame([data_values], columns=COLUMN_NAMES)
        input_imputed = imputer.transform(input_df)
        prediction = model.predict(input_imputed)[0]
        prediction_text = "Potable" if prediction == 1 else "Not Potable"

        print(f"Prediction Result: {prediction_text.upper()}")
        # NEW: Save the reading to the database
        insert_reading(data_values, prediction_text)

    except Exception as e:
        print(f"⚠️ Error processing message: {e}")

# --- 5. MAIN SCRIPT ---
setup_database() # Ensure DB is ready
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_message = on_message
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.subscribe(MQTT_TOPIC)
print("✅ Listener connected and saving data to DB. Listening...")
client.loop_forever()