#!/usr/bin/python3

import queue
import asyncio
import requests

async def __val(handle: int, lat: float, lon: float):
    loop = asyncio.get_event_loop()
    future = loop.run_in_executor(None, requests.get, "https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat=" + str(lat) + "&lon=" + str(lon))
    response = await future

    if (response.status_code != 200):
        raise Exception("OSM Error: " + str(response.status_code))

    response = response.json()
    return (handle, "house_number" in response["address"])

def queue_get_all(q):
    items = []
    maxItemsToRetreive = 10
    for numOfItemsRetrieved in range(0, maxItemsToRetreive):
        try:
            if numOfItemsRetrieved == maxItemsToRetreive:
                break
            items.append(q.get_nowait())
        except queue.Empty:
            break
    return items

async def complete(q, tasks):
    for res in asyncio.as_completed(tasks):
        q.put(await res)
        

def val(locs: list) -> list:
    q = queue.Queue()

    methods = []
    for i in range(len(locs)):
        methods.append(__val(i, locs[i][0], locs[i][1]))

    loop = asyncio.get_event_loop()
    loop.run_until_complete(complete(q, methods))

    response = []
    for i in range(len(locs)):
        response.append(None)

    for ret in queue_get_all(q):
        response[ret[0]] = ret[1]

    return response
