#!/usr/bin/env python

"""
Author: Nick Russo (njrusmc@gmail.com)
Purpose: Trivial script to test Python httpx with logging enabled.
"""

import logging
import sys
import httpx


def main(site):
    """
    Performs a GET request on the supplied website with
    additional logging enabled.
    """

    # Create a basic logger using a common configuration
    # Example format: 2020-05-20 07:12:38 INFO Hello world!
    logging.basicConfig(
        format="%(asctime)s %(levelname)-8s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.DEBUG,
    )
    logger = logging.getLogger()

    # Optional debugging statement
    # breakpoint()  # py3.7+
    # import pdb; pdb.set_trace()  # py3.6-

    # Issue HTTP GET request, check for success, and print body
    logger.info("Sending GET to %s", site)
    resp = httpx.get(site)
    logger.info("Completed GET to %s", site)

    # If not "ok", raise HTTPError, otherwise do nothing
    resp.raise_for_status()
    logger.info("Response headers: %s", resp.headers)


if __name__ == "__main__":
    # Ensure there are at least 2 arguments; extract the
    # second one (first one after the script name)
    if len(sys.argv) >= 2:
        main(sys.argv[1])

    # Insufficient CLI args supplied; use author's homepage by default
    else:
        main("https://njrusmc.net")
