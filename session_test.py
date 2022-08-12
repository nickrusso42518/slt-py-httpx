#!/usr/bin/env python

"""
Author: Nick Russo (njrusmc@gmail.com)
Purpose: Demonstrate how a long-lived TCP session works with requests.
"""

import logging
import requests


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
    url = "http://njrusmc.net"

    # Issue two HTTP GET requests without using a session
    logger.info("Individual, stateless requests")
    requests.get(url)
    requests.get(url)

    # Now use a session; setup occurs only once
    logger.info("Long-lived, stateful TCP session")
    sess = requests.session()
    sess.get(url)
    sess.get(url)


if __name__ == "__main__":
    main()
