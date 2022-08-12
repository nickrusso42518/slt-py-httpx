#!/usr/bin/env python

"""
Author: Nick Russo (njrusmc@gmail.com)
Purpose: Demonstrate basic HTTP cache-control mechanisms using a variety
of URLs with different cache-control characteristics.
"""

import logging
import time
import requests
from cachecontrol import CacheControl
from print_response import print_response


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

    # Specify list of test files to download.
    # Go to http://njrusmc.net/cache/cache.html to see all test files
    base_url = "http://njrusmc.net/cache"
    test_list = [
        "zero128k_public60.test",  # Cache-Control: public, max-age=60
        "zero128k_nostore.test",  # Cache-Control: no-store
    ]

    # For each file, run two GET requests, and use the logger to print out
    # the relevant information as requests are processed
    for test_file in test_list:

        # Assemble the complete URL to feed into the HTTP GET request
        url = f"{base_url}/{test_file}"

        # Create the cached session object, which automatically intereprets
        # caching-related headers (requests doesn't do it natively)
        cached_sess = CacheControl(requests.session())

        # Print information from first run, include key headers
        logger.info("First GET to %s", url)
        resp = cached_sess.get(url)
        resp.raise_for_status()
        print_response(resp, dump_body=False)
        print(f"\n\n{'*' * 80}\n\n")

        # Slight delay just to show the cache timer countdown
        # Print information from second run, but focus is on background debugs
        time.sleep(2)
        logger.info("Second GET to %s", url)
        resp = cached_sess.get(url)
        resp.raise_for_status()
        print_response(resp, dump_body=False)
        print(f"\n\n{'*' * 80}\n\n")


if __name__ == "__main__":
    main()
