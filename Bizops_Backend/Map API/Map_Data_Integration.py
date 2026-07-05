import requests
import pandas as pd
from pymongo import MongoClient

def get_google_places_data(api_key, location, radius, types=None, max_results=20):
    base_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "key": api_key,
        "location": location,
        "radius": radius,
        "types": types,
        "maxResults": max_results
    }

    results = []

    while True:
        response = requests.get(base_url, params=params)
        data = response.json()
        results.extend(data.get('results', []))

        if 'next_page_token' not in data:
            break

        # Wait for a short time before making the next request
        import time
        time.sleep(5)

        # Update the params with the next_page_token
        params['pagetoken'] = data['next_page_token']

    return results


def get_places_data(places,areaName):
    data = {
        "Area Name" : [],
        "Name": [],
        "Latitude": [],
        "Longitude": [],
        "Rating": [],
        "Total Ratings": [],
        "Address": [],
        "Types": [],
        "Price Level": [],
        "Business Status": [],
        "Open Now": []
    }

    
    for place in places:
        data["Area Name"].append(areaName)
        data["Name"].append(place["name"])
        data["Latitude"].append(place["geometry"]["location"]["lat"])
        data["Longitude"].append(place["geometry"]["location"]["lng"])
        data["Rating"].append(place.get("rating", None))
        data["Total Ratings"].append(place.get("user_ratings_total", None))
        data["Address"].append(place.get("vicinity", None))
        data["Types"].append(place.get("types", None))
        data["Price Level"].append(place.get("price_level", None))
        data["Business Status"].append(place.get("business_status", None))
        data["Open Now"].append(place["opening_hours"]["open_now"] if "opening_hours" in place else None)

    return pd.DataFrame(data)

def insert_into_mongodb(df, mongodb_uri, db_name, collection_name):
    client = MongoClient(mongodb_uri)
    db = client[db_name]
    collection = db[collection_name]

    # Convert the DataFrame to a dictionary for MongoDB insertion
    data_dict = df.to_dict(orient='records')

    # Insert data into MongoDB
    collection.insert_many(data_dict)

if __name__ == "__main__":
    # Replace 'YOUR_API_KEY' with your actual Google Places API key.
    api_key = 'AIzaSyAVUMEUA9b4n92gNAa5U9dS_f86KdCiN1w'
    
    # Specify the location and radius for the search.
    #location = "13.067439,80.237617"  # Example coordinates for Chennai, India
    locationData = {
        "areas": [
            
            {
            "name": "Anna Nagar",
            "latitude": 13.0878,
            "longitude": 80.2164
            },
            {
            "name": "Mylapore",
            "latitude": 13.0336,
            "longitude": 80.2707
            },
            {
            "name": "Adyar",
            "latitude": 13.0064,
            "longitude": 80.2574
            },
            {
            "name": "Alwarpet",
            "latitude": 13.0334,
            "longitude": 80.2545
            },
            {
            "name": "Besant Nagar",
            "latitude": 12.9953,
            "longitude": 80.2660
            },
            {
            "name": "Egmore",
            "latitude": 13.0725,
            "longitude": 80.2586
            },
            {
            "name": "Mogappair",
            "latitude": 13.0726,
            "longitude": 80.1671
            },
            {
            "name": "Velachery",
            "latitude": 12.9784,
            "longitude": 80.2204
            },
            {
            "name": "Guindy",
            "latitude": 13.0085,
            "longitude": 80.2207
            },
            {
            "name": "Kodambakkam",
            "latitude": 13.0510,
            "longitude": 80.2244
            },
            {
            "name": "Nungambakkam",
            "latitude": 13.0601,
            "longitude": 80.2496
            },
            {
            "name": "Royapettah",
            "latitude": 13.0585,
            "longitude": 80.2642
            },
            {
            "name": "Saidapet",
            "latitude": 13.0200,
            "longitude": 80.2238
            },
            {
            "name": "Vadapalani",
            "latitude": 13.0502,
            "longitude": 80.2126
            },
            {
            "name": "T. Nagar (Thyagaraya Nagar)",
            "latitude": 13.0429,
            "longitude": 80.2344
            }
        ]
}
    
    print(f"Total Areas : {len(locationData['areas'])}")

    area_counter = 1

    for area in locationData["areas"]:
        radius = 2000  # Example radius in meters

       
        
        # Specify the types of places you are interested in (optional).
        types = "restaurant"

        location = f"{area['latitude']},{area['longitude']}"

        print(f"Fetching For Location {area['name']} - Remaining Areas : {len(locationData['areas']) -  area_counter } ")


        area_counter += 1
        
        # Make the API request and get the response.
        api_response = get_google_places_data(api_key, location, radius, types=types)

        # Extract and transform the data.
        places_df = get_places_data(api_response,area['name'])

        # Specify MongoDB connection details.
        mongodb_uri = 'mongodb://localhost:27017/'
        database_name = "BizOp"
        collection_name = "Chennai"


    
        # List of all place types you want to loop through
        # place_types = [
        #     # "car_dealer",
        #     # "car_rental",
        #     # "car_repair",
        #     # "car_wash",
        #     # "electric_vehicle_charging_station",
        #     # "gas_station",
        #     # "parking",
        #     # "rest_stop",
        #     # "farm",
        #     # "art_gallery",
        #     # "museum",
        #     # "performing_arts_theater",
        #     # "library",
        #     # "preschool",
        #     # "primary_school	school",
        #     # "secondary_school",
        #     # "university",
        #     # # "amusement_center",
        #     # #Upto This Data Retrieved
        #     # "amusement_park",
        #     # "aquarium",
        #     # "banquet_hall",
        #     # "bowling_alley",
        #     # "casino",
        #     # "community_center",
        #     # "convention_center",
        #     # "cultural_center",
        #     # "dog_park",
        #     # "event_venue",
        #     # "hiking_area",
        #     # "historical_landmark",
        #     # "marina",
        #     # "movie_rental",
        #     "movie_theater",
        #     # "national_park",
        #     "night_club",
        #     "park",
        #     # "tourist_attraction",
        #     # # "visitor_center",
        #     # # "wedding_venue",
        #     # # "zoo",
        #     # # "accounting",
        #     # # "atm",
        #     # # "bank",
        #     "american_restaurant",
        #     "bakery",
        #     "bar",
        #     "barbecue_restaurant",
        #     "brazilian_restaurant",
        #     "breakfast_restaurant",
        #     "brunch_restaurant",
        #     "cafe",
        #     "chinese_restaurant",
        #     "coffee_shop",
        #     "fast_food_restaurant",
        #     "french_restaurant",
        #     "greek_restaurant",
        #     "hamburger_restaurant",
        #     "ice_cream_shop",
        #     "indian_restaurant",
        #     "indonesian_restaurant",
        #     "italian_restaurant",
        #     "japanese_restaurant",
        #     "korean_restaurant",
        #     "lebanese_restaurant",
        #     "meal_delivery",
        #     "meal_takeaway",
        #     "mediterranean_restaurant",
        #     "mexican_restaurant",
        #     "middle_eastern_restaurant",
        #     "pizza_restaurant",
        #     "ramen_restaurant",
        #     "restaurant",
        #     "sandwich_shop",
        #     "seafood_restaurant",
        #     "spanish_restaurant",
        #     "steak_house",
        #     "sushi_restaurant",
        #     "thai_restaurant",
        #     "turkish_restaurant",
        #     "vegan_restaurant",
        #     "vegetarian_restaurant",
        #     "vietnamese_restaurant",
        #     # "administrative_area_level_1",
        #     # "administrative_area_level_2",
        #     # "country",
        #     # "locality",
        #     # "postal_code",
        #     # "school_district",
        #     # "city_hall",
        #     # "courthouse",
        #     # "embassy",
        #     # "fire_station",
        #     # "local_government_office",
        #     # "police",
        #     # "post_office",
        #     # "dental_clinic",
        #     # "dentist",
        #     # "doctor",
        #     # "drugstore",
        #     # "hospital",
        #     # "medical_lab",
        #     # "pharmacy",
        #     # "physiotherapist",
        #     # "spa",
        #     # "bed_and_breakfast",
        #     # "campground",
        #     # "camping_cabin",
        #     # "cottage",
        #     # "extended_stay_hotel",
        #     # "farmstay",
        #     # "guest_house",
        #     # "hostel",
        #     # "hotel",
        #     # "lodging",
        #     # "motel",
        #     # "private_guest_room",
        #     # "resort_hotel",
        #     # "rv_park",
        #     # "church",
        #     # "hindu_temple",
        #     # "mosque",
        #     # "synagogue",
        #     # "barber_shop",
        #     # "beauty_salon",
        #     # "cemetery",
        #     # "child_care_agency",
        #     # "consultant",
        #     # "courier_service",
        #     # "electrician",
        #     # "florist",
        #     # "funeral_home",
        #     # "hair_care",
        #     # "hair_salon",
        #     # "insurance_agency",
        #     # "laundry",
        #     # "lawyer",
        #     # "locksmith",
        #     # "moving_company",
        #     # "painter",
        #     # "plumber",
        #     # "real_estate_agency",
        #     # "roofing_contractor",
        #     # "storage",
        #     # "tailor",
        #     # "telecommunications_service_provider",
        #     # "travel_agency",
        #     # "veterinary_care",
        #     "auto_parts_store",
        #     "bicycle_store",
        #     "book_store",
        #     "cell_phone_store",
        #     "clothing_store",
        #     "convenience_store",
        #     "department_store",
        #     "discount_store",
        #     "electronics_store",
        #     "furniture_store",
        #     "gift_shop",
        #     "grocery_store",
        #     "hardware_store",
        #     "home_goods_store",
        #     "home_improvement_store",
        #     "jewelry_store",
        #     "liquor_store",
        #     "market",
        #     "pet_store",
        #     "shoe_store",
        #     "shopping_mall",
        #     "sporting_goods_store",
        #     "store",
        #     "supermarket",
        #     "wholesaler",
        #     # "athletic_field",
        #     # "fitness_center",
        #     # "golf_course",
        #     # "gym",
        #     # "playground",
        #     # "ski_resort",
        #     # "sports_club",
        #     # "sports_complex",
        #     # "stadium",
        #     # "swimming_pool",
        #     # "airport",
        #     # "bus_station",
        #     # "bus_stop",
        #     # "ferry_terminal",
        #     # "heliport",
        #     # "light_rail_station",
        #     # "park_and_ride",
        #     # "subway_station",
        #     # "taxi_stand",
        #     # "train_station",
        #     # "transit_depot",
        #     # "transit_station",
        #     # "truck_stop",
        #     # "administrative_area_level_3",
        #     # "administrative_area_level_4",
        #     # "administrative_area_level_5",
        #     # "administrative_area_level_6",
        #     # "administrative_area_level_7",
        #     # "archipelago",
        #     # "colloquial_area",
        #     # "continent",
        #     # "establishment",
        #     # "floor",
        #     "food",
        #     # "general_contractor",
        #     # "geocode",
        #     # "health",
        #     # "intersection",
        #     # "landmark",
        #     # "natural_feature",
        #     # "neighborhood",
        #     # "place_of_worship",
        #     # "plus_code",
        #     # "point_of_interest",
        #     "political",
        #     # "post_box",
        #     # "postal_code_prefix",
        #     # "postal_code_suffix",
        #     # "postal_town",
        #     # "premise",
        #     # "room",
        #     # "route",
        #     # "street_address",
        #     # "street_number",
        #     # "sublocality",
        #     # "sublocality_level_1",
        #     # "sublocality_level_2",
        #     # "sublocality_level_3",
        #     # "sublocality_level_4",
        #     # "sublocality_level_5",
        #     # "subpremise",
        #     # "town_square"


        # ]

        place_types = [
        "car_dealer",
        "car_rental",
        "car_repair",
        "car_wash",
        "electric_vehicle_charging_station",
        "gas_station",
        "parking",
        "rest_stop",
        "farm",
        "art_gallery",
        "museum",
        "performing_arts_theater",
        "library",
        "preschool",
        "primary_school	school",
        "secondary_school",
        "university",
        "amusement_center",
        "amusement_park",
      
        "aquarium",
        "banquet_hall",
        "bowling_alley",
        "casino",
        "community_center",
        "convention_center",
        "cultural_center",
        "dog_park",
        "event_venue",
        "hiking_area",
        "historical_landmark",
        "marina",
        "movie_rental",
        "national_park",

        "tourist_attraction",
        "visitor_center",
        "wedding_venue",
        "zoo",
        "accounting",
        "atm",
        "bank",
      
        "administrative_area_level_1",
        "administrative_area_level_2",
        "country",
        "locality",
        "postal_code",
        "school_district",
        "city_hall",
        "courthouse",
        "embassy",
        "fire_station",
        "local_government_office",
        "police",
        "post_office",
        "dental_clinic",
        "dentist",
        "doctor",
        "drugstore",
        "hospital",
        "medical_lab",
        "pharmacy",
        "physiotherapist",
        "spa",
        "bed_and_breakfast",
        "campground",
        "camping_cabin",
        "cottage",
        "extended_stay_hotel",
        "farmstay",
        "guest_house",
        "hostel",
        "hotel",
        "lodging",
        "motel",
        "private_guest_room",
        "resort_hotel",
        "rv_park",
        
   

        "church",
        "hindu_temple",
        "mosque",
        "synagogue",
        "barber_shop",
        "beauty_salon",
        "cemetery",
        "child_care_agency",
        "consultant",
        "courier_service",
        "electrician",
        "florist",
        "funeral_home",
        "hair_care",
        "hair_salon",
        "insurance_agency",
        "laundry",
        "lawyer",
        "locksmith",
        "moving_company",
        "painter",
        "plumber",
        "real_estate_agency",
        "roofing_contractor",
        "storage",
        "tailor",
        "telecommunications_service_provider",
        "travel_agency",
        "veterinary_care",

        "athletic_field",
        "fitness_center",
        "golf_course",
        "gym",
        "playground",
        "ski_resort",
        "sports_club",
        "sports_complex",
        "stadium",
        "swimming_pool",

        "airport",
        "bus_station",
        "bus_stop",
        "ferry_terminal",
        "heliport",
        "light_rail_station",
        "park_and_ride",
        "subway_station",
        "taxi_stand",
        "train_station",
        "transit_depot",
        "transit_station",
        "truck_stop",
        "administrative_area_level_3",
        "administrative_area_level_4",
        "administrative_area_level_5",
        "administrative_area_level_6",
        "administrative_area_level_7",
        "archipelago",
        "colloquial_area",
        "continent",
        "establishment",
        "floor",

        "general_contractor",
        "geocode",
        "health",
        "intersection",
        "landmark",
        "natural_feature",
        "neighborhood",
        "place_of_worship",
        "plus_code",
        "point_of_interest",

        "post_box",
        "postal_code_prefix",
        "postal_code_suffix",
        "postal_town",
        "premise",
        "room",
        "route",
        "street_address",
        "street_number",
        "sublocality",
        "sublocality_level_1",
        "sublocality_level_2",
        "sublocality_level_3",
        "sublocality_level_4",
        "sublocality_level_5",
        "subpremise",
        "town_square"


        ]


        print(f"Total Types : {len(place_types)}")

        counter = 1

        for place_type in place_types:
            # Wait for a short time before making the next request
            print(f"Data Collecting for {place_type} - Remaining Types : {len(place_types) - counter}")
            
            # Make the API request for the current place type
            places_data = get_google_places_data(api_key, location, radius, types=place_type.lower().replace(" ", "_"))

            # Extract and transform the data
            places_df = get_places_data(places_data,area['name'])

            # Check if documents is a non-empty list
            if not places_df.empty:
                # Insert documents into the collection
                # Insert the data into MongoDB
                insert_into_mongodb(places_df,mongodb_uri, database_name, collection_name   )

            else:
                print(f"Data for {place_type} in {area['name']} is Empty")

            

            print(f"Data for {place_type} in {area['name']} has been successfully collected and inserted into MongoDB.")

            counter += 1
            import time
            time.sleep(5)
