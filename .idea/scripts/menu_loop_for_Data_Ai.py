import json
import requests

def save_data(file_name, data):
    with open(file_name, 'w') as file:
        json.dump(data, file, indent=4)

def fetch_weather_data():
    weather_api_url = "http://api.openweathermap.org/data/2.5/weather"
    parameters = {"q": "Cape Town", "appid": "your_api_key"}
    response = requests.get(weather_api_url, params=parameters)
    if response.status_code == 200:
        data = response.json()
        save_data("external_api_data.json", data)
        print("Weather data fetched successfully:")
        print(json.dumps(data, indent=4))
    else:
        print("Failed to fetch weather data.")

def fetch_news_data():
    news_api_url = "https://newsapi.org/v2/top-headlines"
    parameters = {"country": "us", "apiKey": "your_api_key"}
    response = requests.get(news_api_url, params=parameters)
    if response.status_code == 200:
        data = response.json()
        save_data("external_api_data.json", data)
        print("News data fetched successfully:")
        print(json.dumps(data, indent=4))
    else:
        print("Failed to fetch news data.")

def main():
    while True:
        print("\nOptions:\n1. Add Interaction\n2. Set Preference\n3. Fetch Weather Data\n4. Fetch News Data\n5. Fetch Geological Data\n6. Exit")
        choice = input("Choose an option: ")
        
        if choice == '3':
            fetch_weather_data()
        elif choice == '4':
            fetch_news_data()
        elif choice == '6':
            print("Exiting...")
            break
        else:
            print("Invalid option, please choose again.")

if __name__ == "__main__":
    main()