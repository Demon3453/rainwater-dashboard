import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, classification_report
import joblib

# --- 1. Load the Dataset ---
# Corrected the filename to match what's in your folder
try:
    df = pd.read_csv("water_potability.csv")
    print("✅ Dataset loaded successfully.")
except FileNotFoundError:
    print("❌ Error: 'water_potability.csv' not found. Please check the filename and location.")
    exit()

# --- 2. Prepare the Data ---
# Separate features (X) and the target variable (y)
X = df.drop('Potability', axis=1)
y = df['Potability']

# Handle missing values using an imputer
imputer = SimpleImputer(strategy='mean')
X_imputed = imputer.fit_transform(X)

# Convert the imputed data back into a pandas DataFrame
X = pd.DataFrame(X_imputed, columns=X.columns)
print("✅ Data preprocessing and imputation complete.")

# --- 3. Split Data into Training and Testing Sets ---
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print(f"✅ Data split into {len(X_train)} training samples and {len(X_test)} testing samples.")

# --- 4. Train the Machine Learning Model ---
model = RandomForestClassifier(n_estimators=100, random_state=42)

print("⏳ Training the RandomForest model...")
model.fit(X_train, y_train)
print("✅ Model training complete.")

# --- 5. Evaluate the Model ---
y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print("\n--- Model Evaluation ---")
print(f"Accuracy on Test Data: {accuracy:.4f}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# --- 6. Save the Model and Imputer ---
joblib.dump(model, 'water_potability_model.joblib')
joblib.dump(imputer, 'imputer.joblib')
print("\n✅ Model and imputer have been saved successfully!")
