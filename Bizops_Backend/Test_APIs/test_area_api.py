import requests
import json

# Base URL of your running Flask server
BASE_URL = "http://localhost:5000/api/data-by-area"

def test_area_api(area_name, city_name):
    """
    Test the /api/data-by-area endpoint with given area and city names
    """
    print("\n" + "="*60)
    print(f"Testing: area='{area_name}', city='{city_name}'")
    print("="*60)
    
    # Prepare the JSON payload
    payload = {
        "area_name": area_name,
        "city_name": city_name
    }
    
    try:
        # Send POST request
        response = requests.post(BASE_URL, json=payload)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("\n✅ Response received successfully!")
            print(json.dumps(data, indent=2, ensure_ascii=False))
            
            # Print summary
            print("\n📊 Summary:")
            print(f"  - Business Categories Count: {len(data.get('business_categories_area', []))}")
            print(f"  - Missing Categories Count: {len(data.get('missing_categories', []))}")
            print(f"  - Population: {data.get('population_sums', {})}")
            
        else:
            print("\n❌ Error response:")
            print(json.dumps(response.json(), indent=2, ensure_ascii=False))
            
    except requests.exceptions.ConnectionError:
        print(f"❌ Connection Error: Could not connect to {BASE_URL}")
        print("   Make sure the Flask server is running!")
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

def test_multiple_scenarios():
    """
    Test multiple scenarios to verify API behavior
    """
    print("🚀 Starting API Tests for /api/data-by-area")
    print("="*60)
    
    # Test cases based on your dataset (Anna Nagar appears in the dataset)
    test_cases = [
        # Valid area from dataset
        {"area_name": "Anna Nagar", "city_name": "Chennai", "description": "Valid area - Anna Nagar"},
        
        # Another area (if exists in your data, adjust accordingly)
        {"area_name": "T Nagar", "city_name": "Chennai", "description": "Valid area - T Nagar"},
        
        # Area with spaces (should normalize)
        {"area_name": "  Anna  Nagar  ", "city_name": "Chennai", "description": "Area with extra spaces"},
        
        # Different case (should normalize)
        {"area_name": "anna nagar", "city_name": "CHENNAI", "description": "Lowercase area and uppercase city"},
        
        # Invalid area
        {"area_name": "NonExistentArea", "city_name": "Chennai", "description": "Non-existent area"},
        
        # Missing area name
        {"area_name": "", "city_name": "Chennai", "description": "Missing area name"},
        
        # Missing city name
        {"area_name": "Anna Nagar", "city_name": "", "description": "Missing city name"},
        
        # Empty payload
        {"area_name": "", "city_name": "", "description": "Empty payload"},
    ]
    
    # Run all test cases
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📝 Test Case {i}: {test_case['description']}")
        test_area_api(test_case["area_name"], test_case["city_name"])
        print("\n" + "-"*60)

def interactive_test():
    """
    Interactive mode to test with custom area and city names
    """
    print("\n🔧 Interactive Test Mode")
    print("Enter area and city names to test (or 'quit' to exit)")
    
    while True:
        print("\n" + "-"*40)
        area_name = input("Enter area name (or 'quit'): ").strip()
        if area_name.lower() == 'quit':
            break
            
        city_name = input("Enter city name: ").strip()
        if city_name.lower() == 'quit':
            break
        
        if area_name and city_name:
            test_area_api(area_name, city_name)
        else:
            print("⚠️  Both area name and city name are required!")

def quick_test_single(area_name, city_name):
    """
    Quick test with specific area and city names
    """
    print(f"\n🚀 Quick test: area='{area_name}', city='{city_name}'")
    test_area_api(area_name, city_name)

if __name__ == "__main__":
    print("="*60)
    print("API Testing Script for /api/data-by-area")
    print("="*60)
    
    # Check if server is reachable
    try:
        response = requests.get("http://localhost:5000/", timeout=2)
        print("✅ Flask server is reachable!")
    except:
        print("⚠️  Warning: Could not reach Flask server at http://localhost:5000/")
        print("   Make sure the server is running before testing.")
        print("   Start server with: python app.py")
        print("\n")
    
    # Menu for selecting test mode
    print("\nSelect test mode:")
    print("1. Run all predefined test cases")
    print("2. Interactive mode (enter your own test data)")
    print("3. Quick test (test with Anna Nagar, Chennai)")
    print("4. Quick test with specific area (enter area name)")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == "1":
        test_multiple_scenarios()
    elif choice == "2":
        interactive_test()
    elif choice == "3":
        quick_test_single("Anna Nagar", "Chennai")
    elif choice == "4":
        area = input("Enter area name: ").strip()
        city = input("Enter city name: ").strip()
        if area and city:
            quick_test_single(area, city)
        else:
            print("❌ Both area and city names are required!")
    else:
        print("Invalid choice. Running default test...")
        quick_test_single("Anna Nagar", "Chennai")
    
    print("\n" + "="*60)
    print("Testing completed!")
    print("="*60)