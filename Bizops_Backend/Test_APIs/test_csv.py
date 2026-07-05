import pandas as pd
import os

# Check if file exists
file_path = r"C:\BIZOP\BIZOP\bizops-hackathon\Bizops_Backend\datasets\Updated_BizOps_datasets_with_count.csv"
print(f"Checking file: {file_path}")
print(f"File exists: {os.path.exists(file_path)}")

try:
    # Read the CSV file
    print("Attempting to read CSV...")
    df = pd.read_csv(file_path)
    print(f"CSV loaded successfully! Shape: {df.shape}")
    
    # Get column names
    print("\nColumn names:")
    print(df.columns.tolist())
    
    # Or with indices
    print("\nColumns with indices:")
    for i, col in enumerate(df.columns):
        print(f"{i}: {col}")
    
    # Show the head (first 5 rows) of the dataset
    print("\n" + "="*50)
    print("HEAD OF THE DATASET (First 5 rows):")
    print("="*50)
    print(df.head())
    
    # Optional: You can also show more rows by specifying a number
    # print("\nFirst 10 rows:")
    # print(df.head(10))
    
    # Optional: Show a preview with more details
    print("\n" + "="*50)
    print("DATASET PREVIEW:")
    print("="*50)
    print(f"Total rows: {len(df)}")
    print(f"Total columns: {len(df.columns)}")
    print("\nFirst few rows with column details:")
    for col in df.columns[:5]:  # Show first 5 columns
        print(f"\n{col}:")
        print(df[col].head())
        
except Exception as e:
    print(f"Error: {e}")