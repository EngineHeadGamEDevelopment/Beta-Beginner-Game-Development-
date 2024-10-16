import json
import os
import requests
import asyncio
from datetime import datetime
import sys
import time
from colorama import Fore, Style

# Define paths for data sources
DATA_PATH = 'data'
ASSETS_PATH = 'assets'

# Check and create necessary directories
os.makedirs(DATA_PATH, exist_ok=True)
os.makedirs(ASSETS_PATH, exist_ok=True)

# Sample data structures
user_data = {
    'interactions': [],
    'preferences': {},
    'interaction_timestamps': [],
}

external_api_data = {
    'weather': {},
    'news': {},
    'geological': {},
    'currency': {},
    'stock': {},
    'timezone': {}
}

# API keys (replace with your actual keys)
API_KEYS = {
    'weather': "8db9fee751e3fa5a3596c9cc96486f91",
    'news': "e18eb01c2b3d45908104628792035eeb",
    'geological': "ee8f7ba8bbfed94c77099072bd5be2d9",
    'currency': "2b908120946bfb453a18339c",
    'stock': "D8WS72X9TI9FZMH7",
    'timezone': "5KJZ0PM66RNQ"
}

# Utility functions
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def loading_spinner():
    """Show a loading spinner."""
    spinner = ['-', '\\', '|', '/']
    for _ in range(20):  # Adjust the range for longer loading
        for symbol in spinner:
            sys.stdout.write('\r' + symbol)
            sys.stdout.flush()
            time.sleep(0.1)

def save_data(data, filename):
    """Save data to a JSON file."""
    try:
        with open(os.path.join(DATA_PATH, filename), 'w') as f:
            json.dump(data, f, indent=4)
        print(f"{Fore.GREEN}Data saved to {filename}{Style.RESET_ALL}")
    except IOError as e:
        print(f"{Fore.RED}Error saving data to {filename}: {e}{Style.RESET_ALL}")

def load_data(filename):
    """Load data from a JSON file."""
    if os.path.exists(os.path.join(DATA_PATH, filename)):
        try:
            with open(os.path.join(DATA_PATH, filename), 'r') as f:
                return json.load(f)
        except (IOError, json.JSONDecodeError) as e:
            print(f"{Fore.RED}Error loading data from {filename}: {e}{Style.RESET_ALL}")
    return {}

def delayed_print(text, delay=0.05):
    """Print text with a delay for effect."""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()  # Move to the next line

def print_weather(city, temperature, condition):
    """Print formatted weather data."""
    print(f"{Fore.BLUE}Weather in {city}:{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Temperature: {temperature}°C{Style.RESET_ALL}")
    print(f"{Fore.GREEN}Condition: {condition}{Style.RESET_ALL}")

def add_interaction(interaction):
    """Add a user interaction."""
    if interaction:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        user_data['interactions'].append(interaction)
        user_data['interaction_timestamps'].append(timestamp)
        save_data(user_data, 'user_data.json')
        print(f"{Fore.CYAN}Interaction '{interaction}' added at {timestamp}{Style.RESET_ALL}")

def set_preference(key, value):
    """Set a user preference."""
    if key and value:
        user_data['preferences'][key] = value
        save_data(user_data, 'user_data.json')
        print(f"{Fore.CYAN}Preference '{key}' set to '{value}'{Style.RESET_ALL}")

# External data fetching and API calls
async def fetch_external_data(source, city=None):
    """Asynchronously fetch external data from APIs and display results."""
    try:
        loading_spinner()  # Show loading spinner while fetching data
        if source == 'weather' and city:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEYS['weather']}&units=metric"
            response = await asyncio.to_thread(requests.get, url)
            if response.status_code == 200:
                data = response.json()
                external_api_data['weather'] = data
                save_data(external_api_data, 'external_api_data.json')
                print_weather(data['name'], data['main']['temp'], data['weather'][0]['description'])
            else:
                print(f"{Fore.RED}Failed to fetch weather data. Status Code: {response.status_code}{Style.RESET_ALL}")

        elif source == 'news':
            url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={API_KEYS['news']}"
            response = await asyncio.to_thread(requests.get, url)
            if response.status_code == 200:
                data = response.json()
                external_api_data['news'] = data
                save_data(external_api_data, 'external_api_data.json')
                print(f"{Fore.GREEN}News data fetched successfully:{Style.RESET_ALL}")
                for article in data['articles'][:5]:  # Print the top 5 articles
                    print(f"- {article['title']}")
            else:
                print(f"{Fore.RED}Failed to fetch news data. Status Code: {response.status_code}{Style.RESET_ALL}")

    except Exception as e:
        print(f"{Fore.RED}Error fetching {source} data: {e}{Style.RESET_ALL}")

async def fetch_geological_data():
    """Fetch geological data from the registered API and display the result."""
    try:
        loading_spinner()  # Show loading spinner while fetching data
        url = f"http://api.ipstack.com/check?access_key={API_KEYS['geological']}&fields=latitude,longitude,city,region_name,country_name"
        response = await asyncio.to_thread(requests.get, url)
        if response.status_code == 200:
            data = response.json()
            external_api_data['geological'] = data
            save_data(external_api_data, 'external_api_data.json')
            print(f"{Fore.GREEN}Geological data fetched successfully:{Style.RESET_ALL}")
            print(json.dumps(data, indent=4))
        else:
            print(f"{Fore.RED}Failed to fetch geological data. Status Code: {response.status_code}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error fetching geological data: {e}{Style.RESET_ALL}")

async def fetch_currency_exchange_data(base_currency):
    """Fetch currency exchange rates."""
    try:
        loading_spinner()  # Show loading spinner while fetching data
        url = f"https://v6.exchangerate-api.com/v6/{API_KEYS['currency']}/latest/{base_currency}"
        response = await asyncio.to_thread(requests.get, url)
        if response.status_code == 200:
            data = response.json()
            external_api_data['currency'] = data
            save_data(external_api_data, 'external_api_data.json')
            print(f"{Fore.GREEN}Currency exchange rates fetched successfully:{Style.RESET_ALL}")
            for currency, rate in data['conversion_rates'].items():
                print(f"{currency}: {rate}")
        else:
            print(f"{Fore.RED}Failed to fetch currency exchange data. Status Code: {response.status_code}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error fetching currency exchange data: {e}{Style.RESET_ALL}")

async def fetch_stock_data(symbol):
    """Fetch stock data from Alpha Vantage."""
    try:
        loading_spinner()  # Show loading spinner while fetching data
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=5min&apikey={API_KEYS['stock']}"
        response = await asyncio.to_thread(requests.get, url)
        if response.status_code == 200:
            data = response.json()
            external_api_data['stock'] = data
            save_data(external_api_data, 'external_api_data.json')
            print(f"{Fore.GREEN}Stock data for {symbol} fetched successfully:{Style.RESET_ALL}")
            for time, info in data['Time Series (5min)'].items()[:5]:  # Print the top 5 entries
                print(f"{time}: Open: {info['1. open']}, High: {info['2. high']}, Low: {info['3. low']}, Close: {info['4. close']}")
        else:
            print(f"{Fore.RED}Failed to fetch stock data. Status Code: {response.status_code}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error fetching stock data: {e}{Style.RESET_ALL}")

async def fetch_timezone_data():
    """Fetch time zone data based on user location."""
    try:
        loading_spinner()  # Show loading spinner while fetching data
        url = f"http://api.timezonedb.com/v2.1/get-time-zone?key={API_KEYS['timezone']}&format=json&by=position&lat=0&lng=0"  # Modify latitude and longitude as needed
        response = await asyncio.to_thread(requests.get, url)
        if response.status_code == 200:
            data = response.json()
            external_api_data['timezone'] = data
            save_data(external_api_data, 'external_api_data.json')
            print(f"{Fore.GREEN}Timezone data fetched successfully:{Style.RESET_ALL}")
            print(f"Time Zone: {data['zoneName']}, Current Time: {data['formatted']}")
        else:
            print(f"{Fore.RED}Failed to fetch timezone data. Status Code: {response.status_code}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error fetching timezone data: {e}{Style.RESET_ALL}")

# Main asynchronous loop
async def main():
    """Main entry point."""
    clear_screen()
    print(f"{Fore.MAGENTA}Welcome to the Unified AI Project!{Style.RESET_ALL}")
    
    # User input for interaction
    while True:
        user_input = input(f"{Fore.CYAN}Enter a command (weather, news, geological, currency, stock, timezone, exit): {Style.RESET_ALL}").strip().lower()
        
        if user_input == "exit":
            break
        elif user_input == "weather":
            city = input("Enter city name: ")
            await fetch_external_data('weather', city)
        elif user_input == "news":
            await fetch_external_data('news')
        elif user_input == "geological":
            await fetch_geological_data()
        elif user_input == "currency":
            base_currency = input("Enter base currency (e.g., USD): ")
            await fetch_currency_exchange_data(base_currency)
        elif user_input == "stock":
            symbol = input("Enter stock symbol (e.g., IBM): ")
            await fetch_stock_data(symbol)
        elif user_input == "timezone":
            await fetch_timezone_data()
        else:
            print(f"{Fore.RED}Invalid command. Please try again.{Style.RESET_ALL}")

# Run the main loop
if __name__ == "__main__":
    asyncio.run(main())
