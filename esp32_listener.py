import joblib
import pandas as pd
import serial
import time

# --- 1. Load the Model and Imputer ---
try:
    model = joblib.load('water_potability_model.joblib')
    imputer = joblib.load('imputer.joblib')
    print("✅ Model and imputer loaded. Waiting for data from ESP32...")
except FileNotFoundError:
    print("❌ Error: Model or imputer files not found. Run the training script first.")
    exit()

# --- 2. Setup Serial Connection ---
# Find your ESP32's port name (e.g., 'COM3' on Windows, '/dev/ttyUSB0' on Linux)
# You can find this in the Arduino IDE or your system's device manager.
SERIAL_PORT = 'COM3' 
BAUD_RATE = 115200

try:
    esp32 = serial.Serial(port=SERIAL_PORT, baudrate=BAUD_RATE, timeout=1)
    print(f"✅ Connected to ESP32 on port {SERIAL_PORT}.")
except serial.SerialException:
    print(f"❌ Error: Could not connect to ESP32. Check port name and connection.")
    exit()

# Column names must be in the exact order the ESP32 sends them
COLUMN_NAMES = [
    'ph', 'Hardness', 'Solids', 'Chloramines', 'Sulfate',
    'Conductivity', 'Organic_carbon', 'Trihalomethanes', 'Turbidity'
]

# --- 3. Listen for Data and Predict Continuously ---
while True:
    if esp32.in_waiting > 0:
        # Read the incoming line of data from the ESP32
        data_string = esp32.readline().decode('utf-8').strip()
        print(f"\nReceived data string: {data_string}")

        try:
            # Parse the string into a list of 9 numbers
            data_values = [float(x) for x in data_string.split(',')]
            
            if len(data_values) != 9:
                 print(f"⚠️ Warning: Received {len(data_values)} values, but expected 9.")
                 continue # Skip this reading and wait for the next one

            # Create a pandas DataFrame for the model
            input_df = pd.DataFrame([data_values], columns=COLUMN_NAMES)
            
            # Use the imputer and make a prediction
            input_imputed = imputer.transform(input_df)
            prediction = model.predict(input_imputed)

            # Print the final result
            if prediction[0] == 1:
                print("Prediction Result: ✅ POTABLE")
            else:
                print("Prediction Result: ❌ NOT POTABLE")

        except (ValueError, IndexError) as e:
            print(f"⚠️ Warning: Could not parse data. Ensure it's 9 comma-separated numbers. Error: {e}")
            
    time.sleep(2) # Wait a couple of seconds before checking for new data