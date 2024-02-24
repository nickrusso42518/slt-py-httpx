#!/usr/bin/env python

"""
Author: Nick Russo (njrusmc@gmail.com)
Purpose: Concurrently collects all pokemon using asyncio,
storing subsets of the total list in individual JSON files.
Documentation available at https://pokeapi.co/docs/v2.html
"""

import asyncio
from math import ceil
import httpx
from print_response import print_response

# Common technique for defining global "constants"
URL = "https://pokeapi.co/api/v2/pokemon"
HEADERS = {"Accept": "application/json"}
QTY = 200


async def get_batch(params):
    """
    Coroutine to collect a batch of pokemon based on the supplied
    limit and offset key/value pairs within the query params argument.
    On success, executes print_responses(). On failure, prints a message.
    On rate-limit (HTTP 429 code), sleeps 3 seconds and tries again.
    """

    # Create an async client context manager
    async with httpx.AsyncClient() as client:
        # Loop forever (ie, keep trying to get the info)
        while True:
            # Send asyncio-style GET request using query params
            resp = await client.get(url=URL, headers=HEADERS, params=params)

            # 200 is the only correct answer; write data and break loop
            if resp.status_code == httpx.codes.OK:
                filename = f"aio_get_all_pokemon_{params['offset']}"
                print_response(resp, filename=filename)
                break

            # Handle failures: 429 means retry, otherwise raise error
            if resp.status_code == httpx.codes.TOO_MANY_REQUESTS:
                await asyncio.sleep(3)

            # Some other error occurred, which is a true failure. Stop trying
            else:
                print(f"FAILED BATCH {params['offset']}")
                break


async def main():
    """
    Execution starts here (coroutine).
    """

    # Determine batch count by collecting a minimal amount of information,
    # then accessing the total count. Perform ceiling division to round up
    resp = httpx.get(URL, headers=HEADERS, params={"limit": 1})
    b_cnt = ceil(resp.json()["count"] / QTY)

    # Instantiate coroutines into objects using a list comprehension
    # Calling a coroutine, such as get_batch(), returns a coroutine object!
    coros = [get_batch({"limit": QTY, "offset": i * QTY}) for i in range(b_cnt)]

    # Encapsulate all coros in a future, then await concurrent completion
    coro_future = asyncio.gather(*coros)
    await coro_future

    print("\nCOLLECTION COMPLETE")


if __name__ == "__main__":
    asyncio.run(main())
