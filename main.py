from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

import geocode
import weather


app = FastAPI
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/weather-at-location-and-time/", response_class=HTMLResponse)
async def submit_form(request: Request, address: str = Form(...), time: int = Form(...)):
    lat, lon = geocode.get_geocoded_address(address)
    weather_data = weather.fetch_and_display_wx_for_time(lat, lon, time)
    return templates.TemplateResponse("index.html", {"request": request, "message": weather_data})


"""
# Get Destination Location
def get_location():
    address = input("Enter the desired address or city: ")
    return geocode.get_geocoded_address(address)


def get_time():
    desired_hours = input(
        "Enter how many hours ahead you would like a forecast (up to 160 hours): ")
    return desired_hours


def main():
    # 1- Get the desired location
    address = get_location()

    # 2- Get the desired forecast time
    desired_hours = get_time()

    # 3- Get the forecast for the desired time and location
    destination_forecast = weather.fetch_and_display_wx_for_time(
        latitude, longitude, hours)
    return (f"Weather at desired location and time: {destination_forecast}")
"""
