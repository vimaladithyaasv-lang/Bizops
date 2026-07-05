import pandas as pd
import joblib

# Load artifacts
model = joblib.load("models/pretrained_model.pkl")
scaler = joblib.load("models/scaler.pkl")
label_encoder = joblib.load("models/label_encoder.pkl")
feature_columns = joblib.load("models/X_columns.pkl")

# Sample input
data = [
    {
        "business_category": "Retail",
        "area_name": "Downtown",
        "Count_of_businesses": 10,
        "Population_of_area": 5000
    }
]

# Convert to DataFrame
new_inputs = pd.DataFrame(data)
new_inputs['Count_of_businesses'] = new_inputs['Count_of_businesses'].fillna(0).astype(int)
new_inputs['Population_of_area'] = new_inputs['Population_of_area'].fillna(1).astype(float)

# Feature engineering
new_inputs['supply_demand_ratio'] = new_inputs['Population_of_area'] / (new_inputs['Count_of_businesses'] + 1)
new_inputs['saturation_index'] = new_inputs['Count_of_businesses'] / (new_inputs['Population_of_area'] + 1e-5)
new_inputs['adjusted_opportunity_score'] = 1 / (new_inputs['supply_demand_ratio'] + new_inputs['saturation_index'] + 1e-5)
new_inputs['normalized_opportunity_score'] = (
    (new_inputs['adjusted_opportunity_score'] - new_inputs['adjusted_opportunity_score'].min()) /
    (new_inputs['adjusted_opportunity_score'].max() - new_inputs['adjusted_opportunity_score'].min() + 1e-5)
)

# Reindex and scale
new_inputs = pd.get_dummies(new_inputs, columns=['business_category', 'area_name'], drop_first=True)
new_inputs = new_inputs.reindex(columns=feature_columns, fill_value=0)
scaled_inputs = scaler.transform(new_inputs)

# Predict
predictions = model.predict(scaled_inputs)
predictions_labels = label_encoder.inverse_transform(predictions)

print("Predictions:", predictions_labels)
