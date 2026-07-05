import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

# ------------------------------
# 1. Load data from CSV
# ------------------------------
csv_path =  r"C:\BIZOP\BIZOP\bizops-hackathon\Bizops_Backend\datasets\Updated_BizOps_datasets_with_count.csv" # Change this to your actual file path
if not os.path.exists(csv_path):
    raise FileNotFoundError(f"CSV file not found: {csv_path}")

data = pd.read_csv(csv_path)

# Print columns to debug (optional)
print("Available columns:", data.columns.tolist())

# Map the columns from your CSV to what the code expects
# Adjust these mappings based on your actual column names
column_mapping = {
    'Business Type__polygon': 'business_category',  # Use the polygon version
    'Standardized Area Name': 'area_name',
    'Count': 'Count_of_businesses',
    'Total Population (in thousands)': 'Population_of_area'  # Note the different naming
}

# Check if required columns exist (with original names)
required_original_cols = list(column_mapping.keys())
for col in required_original_cols:
    if col not in data.columns:
        raise ValueError(f"Required column '{col}' not found in CSV. Available columns: {data.columns.tolist()}")

# Rename columns for consistency
data.rename(columns=column_mapping, inplace=True)

# Verify that all renamed columns exist
for col in ['business_category', 'area_name', 'Count_of_businesses', 'Population_of_area']:
    if col not in data.columns:
        raise ValueError(f"Column '{col}' missing after renaming")

# ------------------------------
# 2. Handle missing values
# ------------------------------
data['Count_of_businesses'] = data['Count_of_businesses'].fillna(0)
data['Population_of_area'] = data['Population_of_area'].fillna(1)   # Avoid division by zero

# Fill missing categorical values
data['business_category'] = data['business_category'].fillna('Unknown')
data['area_name'] = data['area_name'].fillna('Unknown')

# ------------------------------
# 3. Feature engineering (only those that will be used as features)
# ------------------------------
data['supply_demand_ratio'] = data['Population_of_area'] / (data['Count_of_businesses'] + 1)
data['saturation_index'] = data['Count_of_businesses'] / (data['Population_of_area'] + 1e-5)

# ------------------------------
# 4. Create target opportunity score (used only for labeling)
# ------------------------------
# This score is NOT used as a model feature
data['opportunity_score'] = (
    (data['Population_of_area'] / (data['Count_of_businesses'] + 1)) +
    (0.1 / (data['Count_of_businesses'] + 1))
)

# Additional metric for rule-based overrides
data['business_density'] = data['Count_of_businesses'] / (data['Population_of_area'] + 1e-5)

# Adjust opportunity scores for dense areas
data['opportunity_score'] = np.where(
    (data['business_density'] > 0.0007) & (data['Count_of_businesses'] > 200),
    data['opportunity_score'] * 0.8,
    data['opportunity_score']
)

# Remove any rows with NaN in target after calculations
data = data.dropna(subset=['opportunity_score'])

# ------------------------------
# 5. Train / test split BEFORE creating thresholds
# ------------------------------
X_raw = data[['Count_of_businesses', 'Population_of_area',
              'supply_demand_ratio', 'saturation_index',
              'business_category', 'area_name']]
y_raw = data['opportunity_score']   # temporary, will be replaced

X_train_raw, X_test_raw, y_train_raw, y_test_raw = train_test_split(
    X_raw, y_raw, test_size=0.2, random_state=42, stratify=None   # no target yet
)

# Reset indices to avoid alignment issues
X_train_raw = X_train_raw.reset_index(drop=True)
X_test_raw = X_test_raw.reset_index(drop=True)
y_train_raw = y_train_raw.reset_index(drop=True)
y_test_raw = y_test_raw.reset_index(drop=True)

# ------------------------------
# 6. Define opportunity levels using ONLY training data quantiles
# ------------------------------
# Compute thresholds on training scores
threshold_low = y_train_raw.quantile(0.4)
threshold_mid = y_train_raw.quantile(0.7)

def assign_opportunity_level(row, score_col, density_col, count_col, pop_col):
    score = row[score_col]
    density = row[density_col]
    count = row[count_col]
    pop = row[pop_col]

    # Rule-based overrides
    if count > 200 and density > 0.0007:
        return 'low'
    elif count > 100 and pop > 500000:
        return 'mid'

    # General thresholds
    if score < threshold_low:
        return 'low'
    elif score < threshold_mid:
        return 'mid'
    else:
        return 'high'

# Apply to both train and test (using same thresholds)
for df, scores in [(X_train_raw, y_train_raw), (X_test_raw, y_test_raw)]:
    df['opportunity_score'] = scores.values if hasattr(scores, 'values') else scores
    df['business_density'] = df['Count_of_businesses'] / (df['Population_of_area'] + 1e-5)
    df['Opportunity_Level'] = df.apply(
        assign_opportunity_level, axis=1,
        args=('opportunity_score', 'business_density', 'Count_of_businesses', 'Population_of_area')
    )
    # Manual override for zero-business high-population areas
    df['Opportunity_Level'] = np.where(
        (df['Count_of_businesses'] == 0) & (df['Population_of_area'] > 100000),
        'high',
        df['Opportunity_Level']
    )

# Check class distribution
print("Training class distribution:")
print(X_train_raw['Opportunity_Level'].value_counts())
print("\nTest class distribution:")
print(X_test_raw['Opportunity_Level'].value_counts())

# ------------------------------
# 7. Encode target variable (fit only on train)
# ------------------------------
label_encoder = LabelEncoder()
y_train = label_encoder.fit_transform(X_train_raw['Opportunity_Level'])
y_test = label_encoder.transform(X_test_raw['Opportunity_Level'])

# ------------------------------
# 8. One-hot encode categorical features
# ------------------------------
categorical_cols = ['business_category', 'area_name']
onehot = OneHotEncoder(handle_unknown='ignore', sparse_output=False)

# Fit on train, transform both
X_train_cat = onehot.fit_transform(X_train_raw[categorical_cols])
X_test_cat = onehot.transform(X_test_raw[categorical_cols])

# Keep numeric features
numeric_cols = ['Count_of_businesses', 'Population_of_area',
                'supply_demand_ratio', 'saturation_index']
X_train_num = X_train_raw[numeric_cols].values
X_test_num = X_test_raw[numeric_cols].values

# Combine
X_train = np.hstack([X_train_num, X_train_cat])
X_test = np.hstack([X_test_num, X_test_cat])

# Save column names for later inference (especially important for one-hot)
feature_columns = numeric_cols + list(onehot.get_feature_names_out(categorical_cols))

# ------------------------------
# 9. Scale numeric features (optional, but kept for consistency)
# ------------------------------
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# ------------------------------
# 10. Train XGBoost model
# ------------------------------
model = XGBClassifier(eval_metric='logloss', random_state=42)
model.fit(X_train_scaled, y_train)

# ------------------------------
# 11. Evaluate
# ------------------------------
y_pred = model.predict(X_test_scaled)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy:.2f}")
print("Classification Report:")
print(classification_report(y_test, y_pred, target_names=label_encoder.classes_))

# ------------------------------
# 12. Save artifacts
# ------------------------------
joblib.dump(model, "pretrained_model.pkl")
joblib.dump(scaler, "scaler.pkl")
joblib.dump(label_encoder, "label_encoder.pkl")
joblib.dump(onehot, "onehot_encoder.pkl")
joblib.dump(feature_columns, "feature_columns.pkl")

print("Training complete. Model and components saved!")