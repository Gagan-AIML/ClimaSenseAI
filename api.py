import requests

# -----------------------------
# OpenWeather API Key
# -----------------------------
API_KEY = "def170ff2ceeefcf8dc003e413dd12b1"

# -----------------------------
# Get Latitude & Longitude
# -----------------------------
def get_coordinates(city):
    url = (
        "https://api.openweathermap.org/geo/1.0/direct"
        f"?q={city}&limit=1&appid={API_KEY}"
    )
    response = requests.get(url, timeout=10).json()

    if not response:
        raise ValueError("City not found")

    return float(response[0]["lat"]), float(response[0]["lon"])


# -----------------------------
# Get Weather by City
# -----------------------------
def get_weather(city):
    url = (
        "https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={API_KEY}&units=metric"
    )
    response = requests.get(url, timeout=10).json()

    if "main" not in response:
        raise ValueError("Weather data unavailable")

    return {
        "temperature": float(response["main"]["temp"]),
        "humidity": float(response["main"]["humidity"]),
        "pressure": float(response["main"]["pressure"]),
        "wind_speed": float(response.get("wind", {}).get("speed", 0)),
        "rainfall": float(response.get("rain", {}).get("1h", 0))
    }


# -----------------------------
# Get Air Quality by Lat/Lon
# -----------------------------
def get_air_quality(lat, lon):
    url = (
        "https://api.openweathermap.org/data/2.5/air_pollution"
        f"?lat={lat}&lon={lon}&appid={API_KEY}"
    )
    response = requests.get(url, timeout=10).json()

    if "list" not in response or not response["list"]:
        raise ValueError("Air quality data unavailable")

    data = response["list"][0]

    return {
        "pm25": float(data["components"]["pm2_5"]),
        "pm10": float(data["components"]["pm10"]),
        "no2": float(data["components"]["no2"]),
        "so2": float(data["components"]["so2"]),
        "o3": float(data["components"]["o3"]),
        "co": float(data["components"]["co"]),
        "aqi": int(data["main"]["aqi"])
    }


# -----------------------------
# Convenience Function
# -----------------------------
# Fetch weather + air quality together (by city)
def get_weather_air_by_city(city):
    lat, lon = get_coordinates(city)
    weather = get_weather(city)
    air = get_air_quality(lat, lon)
    return [weather, air]
