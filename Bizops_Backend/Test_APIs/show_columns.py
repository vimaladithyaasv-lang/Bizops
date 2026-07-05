import pandas as pd

# Read the CSV file
df = pd.read_csv(r"C:\BIZOP\BIZOP\bizops-hackathon\Bizops_Backend\datasets\Updated_BizOps_datasets_with_count.csv")

# Get column names
print("Column names:")
print(df.columns.tolist())

# Or with indices
print("\nColumns with indices:")
for i, col in enumerate(df.columns):
    print(f"{i}: {col}")