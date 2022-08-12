#!/usr/bin/env python

"""
Author: Nick Russo (njrusmc@gmail.com)
Purpose: Concurrently collects all pokemon using asyncio,
storing subsets of the total list in individual JSON files.
Documentation available at https://pokeapi.co/docs/v2.html
"""

import asyncio
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
            resp = await client.get(
                url=URL, headers=HEADERS, params=params, timeout=2
            )

            # The only correct answer; break loop upon success and write data
            if resp.status_code == 200:
                print_response(
                    resp, filename=f"aio_get_all_pokemon_{params['offset']}"
                )
                break

            # Handle failures: 429 means retry, otherwise raise error
            if resp.status_code == 429:
                await asyncio.sleep(3)

            # Some other error occurred, which is a true failure. Stop trying
            else:
                print(f"FAILED BATCH {params['offset']}")
                break


def main():
    """
    Execution starts here.
    """

    # Build list of async tasks used a list comprehension
    tasks = [get_batch({"limit": QTY, "offset": i * QTY}) for i in range(6)]

    # Define a future to run the tasks
    task_future = asyncio.gather(*tasks)

    # Run the future until all contained tasks are complete
    asyncio.get_event_loop().run_until_complete(task_future)
    print("\nCOLLECTION COMPLETE")


if __name__ == "__main__":
    main()
