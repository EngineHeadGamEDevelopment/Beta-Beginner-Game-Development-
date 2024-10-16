import requests

def get_weather(city):
    weather_api_key = "YOUR_WEATHER_API_KEY"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}&units=metric"
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather = data['weather'][0]['description']
        temp = data['main']['temp']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        return {
            "description": weather,
            "temperature": temp,
            "humidity": humidity,
            "wind_speed": wind_speed
        }
    else:
        print("Error fetching weather data:", response.status_code)
        return None

# Example usage
city_name = "Cape Town, South Africa"
weather_info = get_weather(city_name)
print(f"Weather in {city_name}: {weather_info['description']}, Temperature: {weather_info['temperature']}°C, Humidity: {weather_info['humidity']}%, Wind Speed: {weather_info['wind_speed']} m/s")