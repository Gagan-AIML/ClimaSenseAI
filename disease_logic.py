def map_specific_diseases(air_data, weather_data):
    diseases = {}

    pm25 = air_data["pm25"]
    pm10 = air_data["pm10"]
    temp = weather_data["temperature"]
    humidity = weather_data["humidity"]
    rain = weather_data["rainfall"]

    # 🌫 AIR POLLUTION
    if pm25 > 100 or pm10 > 150:
        diseases["Asthma"] = 3
        diseases["COPD"] = 3
        diseases["Bronchitis"] = 2

    # 😷 COLD & AIRBORNE
    if temp < 18 and humidity > 60:
        diseases["Influenza"] = 3
        diseases["Pneumonia"] = 2

    # ☀️ HEAT STRESS
    if temp >= 38:
        diseases["Heat Exhaustion"] = 3
        diseases["Dehydration"] = 2

    # 🌧 MONSOON / WATER-BORNE
    if humidity > 75 or rain > 5:
        diseases["Water-borne Diseases"] = 3
        diseases["Skin Infection Risk"] = 2

    return sorted(diseases, key=diseases.get, reverse=True)[:5]
