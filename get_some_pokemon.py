#!/usr/bin/env python

"""
Author: Nick Russo (njrusmc@gmail.com)
Purpose: Collects a subset of pokemon items then digs one level
deeper to reveal individual characteristics of each.
Documentation available at https://pokeapi.co/docs/v2.html
"""

import requests
from print_response import print_response


def main():
    """
    Execution starts here.
    """

    # Grab the first 20 (by default) pokemon available
    headers = {"Accept": "application/json"}
    resp = requests.get("https://pokeapi.co/api/v2/pokemon", headers=headers)

    # If an error occurred (resp.status_code >= 400), raise an HTTPError
    resp.raise_for_status()
    print_response(resp, filename="get_pokemon")

    # Optional debugging statement
    # breakpoint()  # py3.7+
    # import pdb; pdb.set_trace()  # py3.6-

    # Go deeper; get the specific details for each pokemon
    # For brevity, let's just grab the first 3 using a slice
    for pokemon in resp.json()["results"][:3]:
        resp = requests.get(pokemon["url"], headers=headers)

        # You don't HAVE to raise exceptions for failed requests. Can test
        # for "ok" which passes when resp.status_code < 400
        if resp.ok:
            print_response(resp, filename=f"get_{pokemon['name']}")
        else:
            print(f"Could not load {pokemon['name']} details")


if __name__ == "__main__":
    main()
