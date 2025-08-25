import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, classification_report
import joblib

# --- 1. Load the Dataset ---
try:
    df = pd.read_csv("water_potability.csv")
    print("✅ Full dataset loaded successfully.")
except FileNotFoundError:
    print("❌ Error: 'water_potability.csv' not found.")
    exit()

# --- 2. NEW: Create a Simplified DataFrame ---
# We are only keeping the columns for the sensors you have, plus the target
simple_df = df[['ph', 'Solids', 'Potability']].copy()
print("✅ Created a simplified dataset with only 'ph' and 'Solids'.")

# --- 3. Prepare the Simplified Data ---
X = simple_df.drop('Potability', axis=1)
y = simple_df['Potability']

# Handle missing values for 'ph' and 'Solids'
imputer = SimpleImputer(strategy='mean')
X_imputed = imputer.fit_transform(X)
X = pd.DataFrame(X_imputed, columns=X.columns)

# --- 4. Split the Simplified Data ---
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# --- 5. Train the NEW, Simpler Model ---
simple_model = RandomForestClassifier(n_estimators=100, random_state=42)
print("⏳ Training the new, simpler model...")
simple_model.fit(X_train, y_train)
print("✅ Simpler model training complete.")

# --- 6. Evaluate the Simpler Model ---
y_pred = simple_model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print("\n--- New Simple Model Evaluation ---")
print(f"Accuracy on Test Data: {accuracy:.4f} (Note: May be lower than the 9-feature model)")
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# --- 7. Save the NEW Model and Imputer ---
# We use new filenames to avoid overwriting your old model
joblib.dump(simple_model, 'simple_model.joblib')
joblib.dump(imputer, 'simple_imputer.joblib')
print("\n✅ New model and imputer saved as 'simple_model.joblib' and 'simple_imputer.joblib'")