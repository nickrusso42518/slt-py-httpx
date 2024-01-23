#!/usr/bin/env python

"""
Author: Nick Russo (njrusmc@gmail.com)
Purpose: Demonstrate how a long-lived TCP session works with httpx.
"""

import logging
import httpx


def main():
    """
    Execution begins here.
    """

    # Use our standard logger template
    logging.basicConfig(
        format="%(asctime)s %(levelname)-8s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.DEBUG,
    )
    logger = logging.getLogger()

    # Define generic URL to test
    url = "https://njrusmc.net"

    # Issue two HTTP GET requests without using a session
    logger.info("Individual, stateless requests")
    httpx.get(url)
    httpx.get(url)

    with httpx.Client() as client:
        # Now use a session; setup occurs only once
        logger.info("Long-lived, stateful TCP session")
        client.get(url)
        client.get(url)


if __name__ == "__main__":
    main()
