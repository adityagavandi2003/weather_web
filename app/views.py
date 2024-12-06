from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpRequest
from app.weatherapi import fetch_weather
from app.weatherapi import calculate_rain_probability
from app.weatherapi import air_quality
from datetime import datetime

def index(request):
    context = {}  # Initialize context to prevent errors
    default_location = "india"  # Set your default location

    # Get the temperature unit selected by the user (from the session)
    converter = request.session.get('converter','°C')  # Default to '°C' if not set


    # Retrieve previous location data from the session
    previous_location = request.session.get('previous_location')
    if previous_location:
        previous_location['converter'] = converter
        context.update(previous_location)

    # First page load or no search input
    if request.method != 'POST' and not previous_location:
        try:
            data = fetch_weather(default_location)  # Fetch weather for default location
            if 'Error' not in data:
                # Extract data from API response
                location = data['location']
                current = data['current']
                forecast = data["forecast"]["forecastday"][0]
                next_forecast = data["forecast"]["forecastday"][1]

                # Call custom functions
                rain = calculate_rain_probability(current)
                airquality = air_quality(current)

                # Local day
                local_datetime = datetime.strptime(location['localtime'], "%Y-%m-%d %H:%M")
                day_of_week = local_datetime.strftime("%A")
                time_of_day = local_datetime.strftime("%I:%M %p")
                
                # Forecast data
                forecast_day = forecast["day"]
                next_day_forecast = next_forecast['day']

                forecast_datetime = datetime.strptime(next_forecast['date'], "%Y-%m-%d")
                next_day = forecast_datetime.strftime("%A")

                # Extract data from above data
                condition = current['condition']
                forecast_condition = forecast_day['condition']
                nextday_condition = next_day_forecast['condition']

                # Astronomy
                astro = forecast["astro"]

                # Update context with default location data
                default_data = {
                    'location': location,
                    'current': current,
                    'forecast': forecast,
                    'condition': condition,
                    'rain': rain,
                    'airquality': airquality,
                    'day': day_of_week,
                    'time': time_of_day,
                    'forecasteday': forecast_day,
                    'forecast_condition': forecast_condition,
                    'next_day_forecast': next_day_forecast,
                    'next_day': next_day,
                    'nextday_condition': nextday_condition,
                    'astro': astro,
                    'converter':converter
                }
                context.update(default_data) # if I removed this doesn't appear at 1st time after refresh it apperar

                # Save default location data to the session
                request.session['previous_location'] = default_data
            else:
                context['error'] = "Unable to fetch weather for default location."

        except Exception as e:
            context['error'] = f"Search place. Displaying previous location."

    # Handle POST requests (user searches for a location)
    elif request.method == 'POST':
        search = request.POST.get('search')  # Search place

        if not search:  # If input is empty
            search = previous_location  # Use previous location

        try:
            data = fetch_weather(search)  # Fetch weather using custom function

            if 'Error' not in data:
                # Extract data from API response
                location = data['location']
                current = data['current']
                forecast = data["forecast"]["forecastday"][0]
                next_forecast = data["forecast"]["forecastday"][1]

                # Call custom functions
                rain = calculate_rain_probability(current)
                airquality = air_quality(current)

                # Local day
                local_datetime = datetime.strptime(location['localtime'], "%Y-%m-%d %H:%M")
                day_of_week = local_datetime.strftime("%A")
                time_of_day = local_datetime.strftime("%I:%M %p")

                # Forecast data
                forecast_day = forecast["day"] # fetching data of 0 index 
                next_day_forecast = next_forecast['day'] # fetching data of 1 index 
                forecast_datetime = datetime.strptime(next_forecast['date'], "%Y-%m-%d") # next day date
                next_day = forecast_datetime.strftime("%A") # date convert in Day

                # Extract data from above data
                condition = current['condition'] #current time condition
                forecast_condition = forecast_day['condition'] # today condition
                nextday_condition = next_day_forecast['condition'] # next day condition

                # Astronomy
                astro = forecast["astro"] # sunrise and sunshine

                # Update context with the current data
                new_data = {
                    'location': location,
                    'current': current,
                    'forecast': forecast,
                    'condition': condition,
                    'rain': rain,
                    'airquality': airquality,
                    'day': day_of_week,
                    'time': time_of_day,
                    'forecasteday': forecast_day,
                    'forecast_condition': forecast_condition,
                    'next_day_forecast': next_day_forecast,
                    'next_day': next_day,
                    'nextday_condition': nextday_condition,
                    'astro': astro,
                    'converter':converter
                }
                context.update(new_data) # if I removed this doesn't appear after 1st time search it apperar after second search

                # Save the current data to the session
                request.session['previous_location'] = new_data
            else:
                context['error'] = f"You're Offline. Displaying previous location."

        except Exception as e:
            context['error'] = f"Displaying previous location."

    return render(request, 'index.html', context)


def convert_temp(request):
    # Store the selected temperature unit in the session
    if request.method == 'POST':
        converter = request.POST.get('converter')
        # Store the selected unit (°C or °F) in the session
        request.session['converter'] = converter

    return redirect("/")
