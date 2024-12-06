import requests
import json
import dotenv
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('api_key')


def fetch_weather(location):
    query = location.lower()

    try:
        res = requests.get(f"https://api.weatherapi.com/v1/forecast.json?key={api_key}&q={query}&aqi=yes&days=2")
        if res.status_code == 200:
            data = res.json()

            #extract data from res
            location_data = data.get('location',{})
            current_data = data.get('current',{})
            forecast_data = data.get('forecast',{})
            
            #store data in context
            context = {
                "location":location_data,
                "current":current_data,
                "forecast":forecast_data
            }
            return context

    except Exception as e:
        return {"Error":str(e)}


def calculate_rain_probability(current_data):
    precip_mm = current_data["precip_mm"]
    cloud_cover = current_data["cloud"]


    # Calculate rain probability
    rain_probability = min(precip_mm * 10 + cloud_cover, 100)
    
    return rain_probability

def air_quality(data):
    # Extract air quality indices
    us_epa_index = data["air_quality"]["us-epa-index"]
    gb_defra_index = data["air_quality"]["gb-defra-index"]


    #epa index to air quality descriptions
    descriptions = {
        1: "Good",
        2: "Moderate",
        3: "Unhealthy for Sensitive Groups",
        4: "Unhealthy",
        5: "Very Unhealthy",
        6: "Hazardous"
    }
    air_quality_description = descriptions.get(us_epa_index, "Unknown")

    return air_quality_description
