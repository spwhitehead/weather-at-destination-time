import requests
from datetime import datetime, timedelta


def fetch_and_display_wx_for_time(latitude: float, longitude: float, hours: int):
    # Get the estimated arrival time
    arrival_time = datetime.now() + timedelta(hours=hours)
    # Weather API endpoint for the given coordinates
    url = f"https://api.weather.gov/points/{latitude},{longitude}"
    response = requests.get(url)
    if response.status_code != 200:
        print("Failed to retrieve weather data.")
        return

    # Get forecast URL from the response

    forecast_url = response.json()["properties"]["forecastHourly"]
    forecast_response = requests.get(forecast_url)
    if forecast_response.status_code != 200:
        print("Failed to retried hourly forecast.")
        return

    # Parse the forecast data
    forecast_data = forecast_response.json()
    periods = forecast_data["properties"]["periods"]

    # Find the forecast closest to the given number of hours
    closest_forecast = None
    min_time_diff = float("inf")
    for period in periods:
        forecast_time = datetime.strptime(
            period["startTime"], "%Y-%m-%dT%H:%M:%S%z")
        # Gets the ABS of the given travel time
        time_diff = abs((forecast_time - arrival_time).total_seconds())
        if time_diff < min_time_diff:
            closest_forecast = period
            min_time_diff = time_diff

    if closest_forecast:
        # Display the relevant forecast information
        print(f"Weather forecast at your given time:")
        print(f"""
            Temperature:    {closest_forecast['temperature']}°{closest_forecast['temperatureUnit']}
            Wind:           {closest_forecast['windSpeed']} from {closest_forecast['windDirection']}
            Forecast:       {closest_forecast['shortForecast']}
            """)
    else:
        print("No suitable forecast found for the estimated arrival time.")
