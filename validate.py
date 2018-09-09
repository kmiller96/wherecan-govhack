#!/usr/bin/python3

import requests

def val(lat: float, lon: float) -> bool:
    response = requests.get("https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat=" + str(lat) + "&lon=" + str(lon))
    if (response.status_code != 200):
        raise Exception("OSM Error: " + str(response.status_code))

    response = response.json()
    return len(response["address"]) > 7
