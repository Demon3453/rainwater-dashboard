import pandas as pd

# Path to the input CSV
input_path = "../data/water_potability.csv"  # Adjust if your structure is different
# Path for the cleaned output
output_path = "../water_potability_cleaned.csv"

# Load data
df = pd.read_csv(input_path)

# Check for missing values
print("Missing values:\n", df.isnull().sum())

# Fill missing values with mean of each column
df.fillna(df.mean(), inplace=True)

# Save cleaned data
df.to_csv(output_path, index=False)
print(f"Cleaned data saved to {output_path}")
