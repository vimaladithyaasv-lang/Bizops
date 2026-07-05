import requests
import json

# Replace with your actual endpoint URL
url = "http://localhost:5000/api/predict-opportunity"

# Sample request (two entries)
payload = [
    {
        "business_category": "Retail",
        "area_name": "Downtown",
        "Count_of_businesses": 10,
        "Population_of_area": 5000
    },
    {
        "business_category": "Restaurant",
        "area_name": "Suburb",
        "Count_of_businesses": 50,
        "Population_of_area": 20000
    }
]

headers = {"Content-Type": "application/json"}

response = requests.post(url, data=json.dumps(payload), headers=headers)

print("Status Code:", response.status_code)
print("Response JSON:")
print(json.dumps(response.json(), indent=2))

# Basic assertions
assert response.status_code == 200
data = response.json()
assert "predictions" in data
assert "prediction_messages" in data
assert "businesses_information" in data
assert len(data["predictions"]) == len(payload)
assert len(data["prediction_messages"]) == len(payload)
assert len(data["businesses_information"]) == len(payload)

# Optional: Check that predictions are valid labels
valid_labels = {"high", "mid", "low"}
for pred in data["predictions"]:
    assert pred in valid_labels

print("All tests passed!")