#!/usr/bin/env python

"""
Author: Nick Russo (njrusmc@gmail.com)
Purpose: Iteratively collects all pokemon using HTTP pagination,
storing subsets of the total list in individual JSON files.
Documentation available at https://pokeapi.co/docs/v2.html
"""

import requests
from print_response import print_response


def main():
    """
    Execution starts here.
    """

    # Grab the first 200 and seed the iteration process
    count = 1
    headers = {"Accept": "application/json"}
    resp = requests.get(
        "https://pokeapi.co/api/v2/pokemon",
        params={"limit": 200},
        headers=headers,
    )
    resp.raise_for_status()
    print_response(resp, filename=f"get_all_pokemon_{count}")

    # Optional debugging statement
    # breakpoint()  # py3.7+
    # import pdb; pdb.set_trace()  # py3.6-

    # Additional code to iteratively check all "next" links. You don't
    # have to specify the "limit" anymore as it is automatically included in
    # the next URL, along with "offset" to identify the starting point
    data = resp.json()
    while data["next"]:
        resp = requests.get(data["next"], headers=headers)
        resp.raise_for_status()
        count += 1
        print_response(resp, filename=f"get_all_pokemon_{count}")
        data = resp.json()


if __name__ == "__main__":
    main()
