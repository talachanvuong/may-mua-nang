import requests
# Search Api
SEARCH_URL = "https://geocoding-api.open-meteo.com/v1/search"

# Detail Weather api
DETAIL_WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

# Air quality Api
AIR_QUALITY_URL = "https://air-quality-api.open-meteo.com/v1/air-quality"

# include get weather information and get location method
class WeatherService:
    # Search a coordination
    @staticmethod
    def search(cor_name:str, lang = "vi"):
        try:
            params = {
                "name" : cor_name,
                "language" : lang
            }
            response = requests.get(SEARCH_URL, params=params)
            response.raise_for_status()
            
            data = response.json()
            print(data)
            
            return data.get("results",[])
        except requests.exceptions.RequestException as e:
            print(f"Error:{e}")
            return []
        
    # Get detail of weather (include basic info and air quality)
    @staticmethod
    def get_weather_info(latitude, longitude):
        try:
            # get basic weather
            forecast_params = {
                "latitude": latitude,
                "longitude": longitude,
                "current": "temperature_2m,relative_humidity_2m,precipitation,rain,wind_speed_10m,cloud_cover",
                "timezone": "auto",
            }
            forecast_response = requests.get(DETAIL_WEATHER_URL, params=forecast_params)
            forecast_data = forecast_response.json()
            
            # get air quality
            air_params = {
                "latitude": latitude,
                "longitude": longitude,
                'current': 'european_aqi,pm2_5',
                'timezone': 'auto'
            }
            air_response = requests.get(AIR_QUALITY_URL, params=air_params)
            air_data = air_response.json()
            
            # merge data
            current_weather = forecast_data.get("current", {})
            current_air = air_data.get("current", {})
            
            result = {
                "temperature": current_weather.get("temperature_2m"),
                "humidity": current_weather.get("relative_humidity_2m"),
                "precipitation": current_weather.get("precipitation"),
                "rain": current_weather.get("rain"),
                "wind_speed": current_weather.get("wind_speed_10m"),
                "cloud_cover": current_weather.get("cloud_cover"),
                "air_quality_index": current_air.get("european_aqi"),
                "pm10": current_air.get("pm10"),
                "pm2_5": current_air.get("pm2_5"),
            }
            return result
        except Exception as e:
            print("Error occurs when get weather information", e)
            return None
