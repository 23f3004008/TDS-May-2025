import requests

def get_bounding_box_value(city, country, bbox_type, coord_type):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        'city': city,
        'country': country,
        'format': 'jsonv2'
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (compatible; MyApp/1.0; +http://yourdomain.com/yourapp)'
    }

    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    data = response.json()

    city_results = [item for item in data if item.get('addresstype') == 'city']
    if not city_results:
        raise ValueError(f"No city results found for {city}, {country}")

    city_results.sort(key=lambda x: x.get('importance', 0), reverse=True)
    city_data = city_results[0]

    boundingbox = city_data.get('boundingbox')
    if not boundingbox or len(boundingbox) != 4:
        raise ValueError("Bounding box data not found or invalid")

    # boundingbox = [min_lat, max_lat, min_lon, max_lon]
    if bbox_type == 'minimum' and coord_type == 'latitude':
        return float(boundingbox[0])
    elif bbox_type == 'maximum' and coord_type == 'latitude':
        return float(boundingbox[1])
    elif bbox_type == 'minimum' and coord_type == 'longitude':
        return float(boundingbox[2])
    elif bbox_type == 'maximum' and coord_type == 'longitude':
        return float(boundingbox[3])
    else:
        raise ValueError("Invalid bbox_type or coord_type")

def main():
    city = input("Enter city: ").strip()
    country = input("Enter country: ").strip()
    bbox_type = input("Enter 'minimum' or 'maximum' (for bounding box): ").strip().lower()
    while bbox_type not in ['minimum', 'maximum']:
        bbox_type = input("Please enter 'minimum' or 'maximum': ").strip().lower()

    coord_type = input("Enter 'latitude' or 'longitude': ").strip().lower()
    while coord_type not in ['latitude', 'longitude']:
        coord_type = input("Please enter 'latitude' or 'longitude': ").strip().lower()

    value = get_bounding_box_value(city, country, bbox_type, coord_type)
    print(f"The {bbox_type} {coord_type} of the bounding box of {city} in {country} is: {value}")

if __name__ == "__main__":
    main()
