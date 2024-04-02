from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

import geocode
import weather


app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/weather-at-location-and-time/", response_class=HTMLResponse)
async def submit_form(request: Request, address: str = Form(...), time: int = Form(...)):
    lat, lon = geocode.get_geocoded_address(address)
    weather_data = weather.fetch_and_display_wx_for_time(lat, lon, time)
    return templates.TemplateResponse("index.html", {"request": request, "message": weather_data, "time": time})
