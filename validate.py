#!/usr/bin/python3

import queue
import asyncio
import requests

async def __val(handle: int, lat: float, lon: float):
    loop = asyncio.get_event_loop()
    future = loop.run_in_executor(None, requests.get, "https://maps.googleapis.com/maps/api/geocode/json?latlng=" + str(lat) + "," + str(lon) + "&key=AIzaSyC0DraVSBKXdfu8SXS4ZBAmzyx_eON8OMk")
    response = await future

    if (response.status_code != 200):
        raise Exception("OSM Error: " + str(response.status_code))

    response = response.json()
    v = False
    for comp in response["results"][0]["address_components"]:
        if ("street_number" in comp["types"]):
            v = True
            break

    return (handle,v) 

def queue_get_all(q, i):
    items = []
    for numOfItemsRetrieved in range(i):
        try:
            if numOfItemsRetrieved == i:
                break
            items.append(q.get_nowait())
        except queue.Empty:
            break
    return items

async def complete(q, tasks):
    for res in asyncio.as_completed(tasks):
        q.put(await res)

def inner_val(locs: list) -> list:
    q = queue.Queue()
    length = len(locs)

    methods = []
    for i in range(length):
        methods.append(__val(i, locs[i][0], locs[i][1]))

    loop = asyncio.get_event_loop()
    loop.run_until_complete(complete(q, methods))

    response = []
    for i in range(length):
        response.append(None)

    for ret in queue_get_all(q, length):
        response[ret[0]] = ret[1]

    return response

def val(locs: list) -> list:
    total_length = len(locs)
    left = total_length
    index = 0
    res = []
    size = 64

    while (left > size):
        res.extend(inner_val(locs[index:index+size]))
        left -= size
        index += size

    res.extend(inner_val(locs[index:]))
    return res
