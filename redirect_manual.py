#!/usr/bin/env python

"""
Author: Nick Russo (njrusmc@gmail.com)
Purpose: Demonstrate how requests handles HTTP redirects for
a typical GET request.
"""

import requests
from print_response import print_response


def main():
    """
    Execution begins here.
    """

    # This links to my "Python 3 By Example" course on O'Reilly
    resp1 = requests.get("http://njrusmc.net/r/sltreq", allow_redirects=False)
    resp1.raise_for_status()
    print_response(resp1, dump_body=False)

    # If >= 300, it's a redirect. Errors are impossible here; those
    # would have been caught by raise_for_status() earlier
    if resp1.status_code >= 300:

        # Extract next URL from Location header
        url = resp1.headers["Location"]

        ### Perform security checks on "url" if desired ###

        # Issue another GET request to the next URL
        resp2 = requests.get(url, allow_redirects=False)
        resp2.raise_for_status()
        print_response(resp2, dump_body=False)


if __name__ == "__main__":
    main()
