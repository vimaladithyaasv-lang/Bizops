import pandas as pd
from flask import Flask, jsonify, request
import os
import traceback
import numpy as np
import joblib
import pickle
from flask import Flask, request, jsonify


app = Flask(__name__)
 

model = joblib.load("models/pretrained_model.pkl")
scaler = joblib.load("models/scaler.pkl")
label_encoder = joblib.load("models/label_encoder.pkl")
feature_columns = joblib.load("models/X_columns.pkl")

MASTER_FILE =  r"C:\BIZOP\BIZOP\bizops-hackathon\Bizops_Backend\datasets\Updated_BizOps_datasets_with_count.csv" 

# Load master data
if os.path.exists(MASTER_FILE):
    try:
        master_data = pd.read_csv(MASTER_FILE)
        print(f"Master data loaded: {MASTER_FILE}, shape: {master_data.shape}")
    except Exception as e:
        print(f"Error reading {MASTER_FILE}: {e}")
        master_data = None
else:
    print(f"File not found: {MASTER_FILE}")
    master_data = None

@app.route('/api/data-by-city', methods=['GET'])
def home():
    try:
        # Get query parameters
        city_name = request.args.get('city_name', '').strip()
        area_name = request.args.get('area_name', '').strip()
        
        print(f"Received city_name: {city_name}, area_name: {area_name}")
        
        if not city_name:
            return jsonify({"error": "City name is required"}), 400

        # Check data availability
        if master_data is None:
            return jsonify({"error": f"Master data not available. Check file '{MASTER_FILE}'."}), 500

        # Rename columns if they exist
        column_rename_map = {
            "Total Population (in thousands)": "Total Population",
            "Population - Male (in thousands)": "Population - Male",
            "Population - female (in thousands)": "Population - Female"
        }
        available_columns = set(master_data.columns)
        master_data.rename(columns={k: v for k, v in column_rename_map.items() if k in available_columns}, inplace=True)

        # Ensure required columns exist
        required_columns = ["Total Population", "Population - Male", "Population - Female", 
                            "Standardized Area Name", "City Name"]
        missing_columns = [col for col in required_columns if col not in master_data.columns]
        if missing_columns:
            return jsonify({"error": f"Missing columns: {missing_columns}", 
                            "available_columns": list(master_data.columns)}), 500

        # Filter data
        if area_name:
            filtered_data = master_data[master_data['Standardized Area Name'].str.upper() == area_name.upper()]
            if filtered_data.empty:
                return jsonify({"error": f"No data found for area: {area_name} in city: {city_name}"}), 404
        else:
            filtered_data = master_data[master_data['City Name'].str.upper() == city_name.upper()]
            if filtered_data.empty:
                return jsonify({"error": f"No data found for city: {city_name}"}), 404

        # Business categories
        business_categories = (
            filtered_data.groupby('Business Type__polygon')
            .size()
            .reset_index(name='Count')
        )
        business_categories['Business Type__polygon'] = business_categories['Business Type__polygon'].fillna('Store')

        # Population summary
        population_data = filtered_data[['Standardized Area Name', 'Total Population', 
                                         'Population - Male', 'Population - Female']].drop_duplicates()
        population_sums = {
            'TotalPopulationSum': float(population_data['Total Population'].sum() * 1000),
            'MalePopulationSum': float(population_data['Population - Male'].sum() * 1000),
            'FemalePopulationSum': float(population_data['Population - Female'].sum() * 1000)
        }

        # Build response
        response = {
            'BusinessCategories': [
                {"BusinessCategory": row['Business Type__polygon'], "Count": int(row['Count'])}
                for _, row in business_categories.iterrows()
            ],
            'AreaNames': filtered_data['Standardized Area Name'].unique().tolist(),
            'SummedPopulation': population_sums
        }

        return jsonify(response)

    except Exception as e:
        print("Error details:", str(e))
        return jsonify({"error": str(e)}), 500

@app.route('/api/data-by-area', methods=['POST'])
def get_data_by_area():
    try:
        data = request.get_json()
        area_name = data.get('area_name', '').strip()
        city_name = data.get('city_name', '').strip()
        master_data_area = master_data

        print("Request Details", area_name, city_name)

        if not area_name or not city_name:
            return jsonify({"error": "Both area_name and city_name are required"}), 400

        # Normalize inputs
        area_name_normalized = area_name.replace(" ", "").upper()
        city_name_normalized = city_name.replace(" ", "").upper()

        # Rename columns for consistency
        column_rename_map = {
            "Total Population (in thousands)": "Total Population in thousands",
            "Population - Male (in thousands)": "Population - Male in thousands",
            "Population - female (in thousands)": "Population - Female in thousands"
        }
        master_data_area.rename(columns=column_rename_map, inplace=True)

        # Normalize area names in master data
        master_data_area['Standardized Area Name'] = (
            master_data_area['Standardized Area Name']
            .astype(str)
            .str.strip()
            .str.replace(" ", "")
            .str.upper()
        )

        # Filter for the requested area
        filtered_area_data = master_data_area[
            master_data_area['Standardized Area Name'] == area_name_normalized
        ]

        if filtered_area_data.empty:
            print("filtered_area_data_missing")
            return jsonify({"error": f"No data found for area: {area_name}"}), 404

        # Business categories for the area
        business_categories_area = (
            filtered_area_data.groupby('Business Type__polygon')
            .size()
            .reset_index(name='Count')
        )
        business_categories_area['Business Type__polygon'] = business_categories_area['Business Type__polygon'].fillna('Unknown')

        # Overall business categories (to compute missing categories)
        business_categories_overall = (
            master_data_area.groupby('Business Type__polygon')
            .size()
            .reset_index(name='Count')
        )
        missing_categories = set(business_categories_overall['Business Type__polygon']) - \
                             set(business_categories_area['Business Type__polygon'])

        # Population data
        population_data = filtered_area_data[[
            'Total Population in thousands',
            'Population - Male in thousands',
            'Population - Female in thousands'
        ]].drop_duplicates()

        population_sums = {
            'Total Population Sum': float(population_data['Total Population in thousands'].sum(numeric_only=True)),
            'Male Population Sum': float(population_data['Population - Male in thousands'].sum(numeric_only=True)),
            'Female Population Sum': float(population_data['Population - Female in thousands'].sum(numeric_only=True))
        }

        # Build response (no MongoDB, Instagram, land, rent, restaurant data)
        response = {
            "business_categories_area": [
                {"Business Category": row['Business Type__polygon'], "Count": int(row['Count'])}
                for _, row in business_categories_area.iterrows()
            ],
            "missing_categories": list(missing_categories),
            "population_sums": population_sums
        }

        print("response json", jsonify(response))
        return jsonify(response)

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

@app.route('/api/predict-opportunity', methods=['POST'])
def predict_opportunity():
    master_data_area = master_data
    try:
        data = request.get_json()
        if not data or not isinstance(data, list):
            return jsonify({"error": "Expected a JSON array of entries."}), 400

        for entry in data:
            required = ["business_category", "area_name", "Count_of_businesses", "Population_of_area"]
            if not all(k in entry for k in required):
                return jsonify({"error": f"Each entry must contain {required}"}), 400

        new_inputs = pd.DataFrame(data)
        new_inputs['Count_of_businesses'] = new_inputs['Count_of_businesses'].fillna(0).astype(int)
        new_inputs['Population_of_area'] = new_inputs['Population_of_area'].fillna(1).astype(float)

        # Feature engineering (aligned with training)
        new_inputs['supply_demand_ratio'] = new_inputs['Population_of_area'] / (new_inputs['Count_of_businesses'] + 1)
        new_inputs['saturation_index'] = new_inputs['Count_of_businesses'] / (new_inputs['Population_of_area'] + 1e-5)
        new_inputs['adjusted_opportunity_score'] = 1 / (new_inputs['supply_demand_ratio'] + new_inputs['saturation_index'] + 1e-5)
        new_inputs['normalized_opportunity_score'] = (
            (new_inputs['adjusted_opportunity_score'] - new_inputs['adjusted_opportunity_score'].min()) /
            (new_inputs['adjusted_opportunity_score'].max() - new_inputs['adjusted_opportunity_score'].min() + 1e-5)
        )

        # One-hot encode and reindex
        new_inputs = pd.get_dummies(new_inputs, columns=['business_category', 'area_name'], drop_first=True)
        new_inputs = new_inputs.reindex(columns=feature_columns, fill_value=0)
        scaled_inputs = scaler.transform(new_inputs)

        # Predict
        predictions = model.predict(scaled_inputs)
        predictions_labels = label_encoder.inverse_transform(predictions)

        # Build messages
        messages = {
            "high": lambda bc, an: f"High opportunity in {an} for {bc}. Great potential.",
            "mid": lambda bc, an: f"Moderate opportunity in {an} for {bc}. Consider competition.",
            "low": lambda bc, an: f"Low opportunity in {an} for {bc}. Market is oversaturated."
        }
        prediction_messages = [
            messages[label](entry["business_category"], entry["area_name"])
            for label, entry in zip(predictions_labels, data)
        ]

        # Retrieve business info per entry
        businesses_information = []
        for entry in data:
            area_data = master_data_area[
                (master_data_area['Standardized Area Name'] == entry["area_name"]) &
                (master_data_area['Business Type__point'] == entry["business_category"])
            ]
            if area_data.empty:
                area_data = master_data_area[master_data_area['Business Type__point'] == entry["business_category"]]
            business_data = area_data[['Name__point', 'Rating__point', 'Address__point']].fillna(0)
            businesses_information.append(business_data.to_dict(orient='records'))

        response = {
            "predictions": predictions_labels.tolist(),
            "prediction_messages": prediction_messages,
            "businesses_information": businesses_information
        }
        return jsonify(response)

    except Exception as e:
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)