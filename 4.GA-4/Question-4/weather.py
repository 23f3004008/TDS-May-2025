import requests
import json

API_KEY = "AGbFAKx58hyjQScCXIYrxuEwJh2W2cmv"

# Fixed city list extracted from the JS snippet you gave
CITIES = {
    "New York", "Los Angeles", "London", "Tokyo", "Osaka", "Paris", "New Delhi", "Sydney", "Toronto",
    "Mexico City", "Shanghai", "Dubai", "Moscow", "Istanbul", "Mumbai", "Bangkok", "Cape Town", "Singapore",
    "Hong Kong", "Barcelona", "Berlin", "Rome", "Chicago", "Buenos Aires", "Madrid", "San Francisco",
    "Rio de Janeiro", "Seoul", "Santiago", "Lisbon", "Vienna", "Amsterdam", "Cairo", "Jakarta", "Lagos",
    "Kuala Lumpur", "Vancouver", "Manila", "Athens", "Warsaw", "Budapest", "Helsinki", "Stockholm", "Brussels",
    "Prague", "Oslo", "Zurich", "Tel Aviv", "Doha", "Dublin", "Lima", "Bogota", "Montreal", "Miami", "Seattle",
    "Boston", "Houston", "Phoenix", "Dallas", "Atlanta", "San Diego", "Caracas", "Sao Paulo", "Melbourne",
    "Auckland", "Wellington", "Perth", "Brisbane", "Copenhagen", "Hanoi", "Ho Chi Minh City", "Taipei",
    "Nairobi", "Accra", "Casablanca", "Algiers", "Kinshasa", "Kigali", "Addis Ababa", "Luanda", "Abu Dhabi",
    "Muscat", "Jeddah", "Riyadh", "Kuwait City", "Tehran", "Karachi", "Dhaka", "Lahore", "Colombo", "Kathmandu",
    "Islamabad", "Tashkent", "Baku", "Yerevan", "Tbilisi", "Bishkek", "Nur-Sultan", "Ulaanbaatar", "Almaty",
    "Beijing"
}

def get_location_id(city_name):
    if city_name not in CITIES:
        raise ValueError(f"City '{city_name}' is not supported. Please choose from the fixed city list.")
    
    params = {
        "api_key": API_KEY,
        "stack": "aws",
        "locale": "en",
        "filter": "international",
        "place-types": "settlement,airport,district",
        "order": "importance",
        "s": city_name,
        "a": "true",
        "format": "json"
    }
    url = "https://locator-service.api.bbci.co.uk/locations"
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    results = data.get("response", {}).get("results", {}).get("results", [])
    if not results:
        raise ValueError(f"No location found for city '{city_name}'")

    return results[0]["id"]

def get_weather_forecast(location_id):
    url = f"https://weather-broker-cdn.api.bbci.co.uk/en/forecast/aggregated/{location_id}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def extract_forecast_description(weather_data):
    forecasts = weather_data.get("forecasts", [])
    forecast_map = {}
    for day in forecasts:
        report = day.get("summary", {}).get("report", {})
        local_date = report.get("localDate")
        description = report.get("enhancedWeatherDescription")
        if local_date and description:
            forecast_map[local_date] = description
    return forecast_map

def main():
    city = input("Enter city name (from fixed list): ").strip()
    try:
        location_id = get_location_id(city)
        weather_data = get_weather_forecast(location_id)
        forecast = extract_forecast_description(weather_data)
        print(json.dumps(forecast, indent=2))
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
