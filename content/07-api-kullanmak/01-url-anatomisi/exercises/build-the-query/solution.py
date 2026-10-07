from urllib.parse import urlencode

forecast_base = "https://api.example.com/v1/forecast"
forecast_params = {"city": "New York", "units": "metric", "days": 3}

search_base = "https://api.example.com/v1/search"

url = forecast_base + "?" + urlencode(forecast_params)
search_url = search_base + "?" + urlencode({"q": "fish & chips", "lang": "en"})

print(url)
print(search_url)
