import pandas as pd
import joblib

# --- 1. Load the Trained Model and Imputer ---
try:
    model = joblib.load('water_potability_model.joblib')
    imputer = joblib.load('imputer.joblib')
    print("✅ Model and imputer loaded successfully.")
except FileNotFoundError:
    print("❌ Error: Model or imputer files not found. Please run the training script first.")
    exit()

# --- 2. Enter Your Rainwater Sample Data Here ---
# IMPORTANT: Replace the placeholder values below with your actual water test results.
rainwater_sample = {
    'ph': [7.0],                # Example: pH level (0-14)
    'Hardness': [195.0],          # Example: Hardness (mg/L)
    'Solids': [21000.0],        # Example: Total dissolved solids (ppm)
    'Chloramines': [7.2],       # Example: Chloramines (ppm)
    'Sulfate': [330.0],         # Example: Sulfate (mg/L)
    'Conductivity': [425.0],    # Example: Conductivity (μS/cm)
    'Organic_carbon': [14.5], # Example: Organic Carbon (ppm)
    'Trihalomethanes': [66.0],# Example: Trihalomethanes (μg/L)
    'Turbidity': [4.0]          # Example: Turbidity (NTU)
}
print("\n--- Analyzing Your Sample ---")
input_df = pd.DataFrame(rainwater_sample)
print(input_df)

# --- 3. Prepare the Data and Make a Prediction ---
# Use the loaded imputer to prepare the data, just like in training
input_imputed = imputer.transform(input_df)

# Predict potability and the probability
prediction = model.predict(input_imputed)
prediction_proba = model.predict_proba(input_imputed)

# --- 4. Display the Result ---
print("\n--- Prediction Result ---")
if prediction[0] == 1:
    print("✅ The water is predicted to be POTABLE (Safe to drink).")
else:
    print("❌ The water is predicted to be NOT POTABLE (Not safe to drink).")

print(f"\nConfidence Score:")
print(f"   Probability of NOT POTABLE: {prediction_proba[0][0]:.2%}")
print(f"   Probability of POTABLE:     {prediction_proba[0][1]:.2%}")