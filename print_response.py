#!/usr/bin/env python

"""
Author: Nick Russo (njrusmc@gmail.com)
Purpose: Simple printing mechanism for HTTP responses that come back
from the 'httpx' library for troubleshooting/learning.
"""

import json
import httpx


def print_response(resp, filedir="resp", filename=None, dump_body=True):
    """
    Print the key details from a given response. Set dump_body to true
    to reveal the body content in the most appropriate format based on
    the response's Content-Type header.
    """

    # For context, print the original request
    # ... and a line of dashes of equal length
    header = f"\n\n{resp.request.method} {resp.request.url}"
    print(header)
    print(len(header) * "-")

    # Print the status code and reason, along with the elapsed time
    print(f"Result: {resp.status_code}/{resp.reason_phrase}")
    print(f"Elapsed time: {resp.elapsed.microseconds} us")

    # Iterate over all kv-pairs in the headers dictionary and print them
    print("HTTP headers:")
    for header_name, header_value in resp.headers.items():
        print(f"  - {header_name}: {header_value}")

    # Print the number of redirects. If any exist, print out the URL/status
    print(f"HTTP redirect count: {len(resp.history)}")
    for hist in resp.history:
        print(f"  - {hist.url} -> {hist.status_code}/{hist.reason}")

    # Optionally dump the body; useful for plain text responses (not files)
    if dump_body:
        # First, determine the content type, defaulting to "html"
        content_type = resp.headers.get("Content-Type", "html")

        # If a filename was not supplied, create a dynamic one using
        # the method name and the in-memory ID of the response object
        if not filename:
            filename = f"{resp.request.method}_{id(resp)}".lower()

        # Define the entire filepath using the directory and name
        filepath = f"{filedir}/{filename}"

        # Based on the content type, create different files.
        # Add more options if you want ...
        if "html" in content_type:
            filepath += ".html"
            with open(filepath, "w", encoding="utf-8") as handle:
                handle.write(resp.text)
        elif "json" in content_type:
            filepath += ".json"
            with open(filepath, "w", encoding="utf-8") as handle:
                json.dump(resp.json(), handle, indent=2)

        print(f"HTTP body written to {filepath}")


def main():
    """
    Performs a quick test on the print_response() function.
    """

    resp = httpx.get("https://njrusmc.net")
    resp.raise_for_status()
    print_response(resp, filename="get_nick_website")


if __name__ == "__main__":
    main()
