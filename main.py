import geocode
import weather

from fastapi import FastAPI


app = FastAPI

# Get Destination Location


def get_location():
    address = input("Enter the desired address or city: ")
    return geocode.get_geocoded_address(address)
