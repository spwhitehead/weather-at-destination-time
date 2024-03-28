import requests
from datetime import datetime, timedelta, timezone

# For Testing only!!!
# latitude = 33.98720773169573
# longitude = -118.27262854661085
# hours = 4
# End testing !!!


def fetch_and_display_wx_for_time(latitude: float, longitude: float, hours: int):
    # Get the estimated arrival time
    future_time = datetime.now(timezone.utc) + timedelta(hours=hours)
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
        print("Failed to retrieve hourly forecast.")
        return

    # Parse the forecast data
    forecast_data = forecast_response.json()
    periods = forecast_data["properties"]["periods"]

    # Find the forecast closest to the given number of hours
    closest_forecast = min(periods, key=lambda period: abs(
        datetime.strptime(period["startTime"], "%Y-%m-%dT%H:%M:%S%z") - future_time))

    if closest_forecast:
        # Construct the forecast information string
        forecast_info = (
            f"Temperature:    {closest_forecast['temperature']}°{
                closest_forecast['temperatureUnit']}\n"
            f"Wind:           {closest_forecast['windSpeed']} from the {
                closest_forecast['windDirection']}\n"
            f"Forecast:       {closest_forecast['shortForecast']}\n"
        )
    else:
        forecast_info = "No suitable forecast found for the estimated arrival time."

    return forecast_info
