#!/usr/bin/env python

"""
Author: Nick Russo (njrusmc@gmail.com)
Purpose: Trivial script to test Python httpx.
"""

import sys
import httpx


def main(site):
    """
    Performs a GET request on the supplied website.
    """

    # Issue HTTP GET request, check for success, and print body
    resp = httpx.get(site)

    # If "is_success", do nothing. Else, raise httpx.HTTPStatusError
    # L710: ~/environments/pyhttpx/lib/python3.10/site-packages/httpx/_models.py
    resp.raise_for_status()
    print(resp.text)


if __name__ == "__main__":
    # Ensure there are at least 2 arguments; extract the
    # second one (first one after the script name)
    if len(sys.argv) >= 2:
        main(sys.argv[1])

    # Insufficient CLI args supplied; use author's homepage by default
    else:
        main("https://njrusmc.net")
