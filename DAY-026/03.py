# WEATHER FETCHER: 
# You need a free API key from: https://openweathermap.org/

# API Key: bd5e378503939ddaee76f12ad7a97608 --> NOT MINE SOMEONE'S FROM GITHUB, I JUST USE IT.


import requests
API_KEY = "bd5e378503939ddaee76f12ad7a97608"
city = input("Enter City: ")
url = (
    f"https://api.openweathermap.org/data/2.5/weather"
    f"?q={city}"
    f"&appid={API_KEY}"
    f"&units=metric"
)
response = requests.get(url)
if response.status_code == 200:
    data = response.json()
    print("\n===== WEATHER =====")
    print("City:", data["name"])
    print("Temperature:", data["main"]["temp"], "°C")
    print("Humidity:", data["main"]["humidity"], "%")
    print("Condition:",
          data["weather"][0]["description"])
else:
    print("City Not Found")