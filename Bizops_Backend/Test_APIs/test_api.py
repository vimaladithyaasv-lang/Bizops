import requests
import json

# Base URL of your running Flask server
BASE_URL = "http://localhost:5000/api/data-by-city"

def test_api(city_name, area_name=None):
    """Send a GET request to the API and print the response."""
    params = {"city_name": city_name}
    if area_name:
        params["area_name"] = area_name

    print(f"\n=== Testing: city={city_name}, area={area_name} ===")
    try:
        response = requests.get(BASE_URL, params=params)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print("Response JSON:")
            print(json.dumps(data, indent=2))
        else:
            print("Error response:")
            print(response.json())
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

def main():
    # Test 1: Valid city without area
    test_api("Chennai")

    # Test 2: Valid city with an area that exists (adjust area name to match your data)
    test_api("Chennai", "Anna Nagar")   # Replace with an area from your dataset

    # Test 3: Invalid city
    test_api("InvalidCity")

    # Test 4: Valid city but invalid area
    test_api("Chennai", "NonExistentArea")

    # Test 5: Missing city name (should return 400)
    test_api("")

if __name__ == "__main__":
    main()