import json
import pickle
import numpy as np

__locations = None
__data_columns = None
__model = None

def get_estimated_price(location, sqft, bhk, bath):
    try:
        loc_index = __data_columns.index(location.lower())
    except ValueError:
        loc_index = -1

    x = np.zeros(len(__data_columns))
    x[0] = sqft
    x[1] = bhk
    x[2] = bath
    if loc_index >= 0:
        x[loc_index] = 1
    return round(__model.predict([x])[0], 2)

def get_locations_names():
    return __locations

def load_saved_artifacts():
    global __data_columns
    global __locations
    global __model

    print("Loading saved artifacts starts...")
    
    try:
        # Load columns.json
        with open("columns.json", 'r') as f:
            data = json.load(f)
            __data_columns = data.get('data columns', [])  # Adjust to match JSON key 'data columns'
            __locations = __data_columns[3:]  # Assuming __locations is derived from __data_columns

        # Load Bangalore_house_price_model.pickle
        with open("Bangalore_house_price_model.pickle", 'rb') as f:
            __model = pickle.load(f)

        print("Loading saved artifacts done....")

    except FileNotFoundError:
        print("Error: File not found. Make sure 'columns.json' and 'Bangalore_house_price_model.pickle' exist.")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Automatically load artifacts when this script is executed directly
load_saved_artifacts()

# Example usage for testing purposes
if __name__ == '__main__':
    print(get_locations_names())
    print(get_estimated_price('1st Phase JP Nagar', 1000, 3, 3))
    print(get_estimated_price('1st Phase JP Nagar', 1000, 2, 2))


