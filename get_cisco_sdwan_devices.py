#!/usr/bin/env python

"""
Author: Nick Russo (njrusmc@gmail.com)
Purpose: Basic consumption of Cisco SD-WAN REST API using the
public Cisco DevNet sandbox.
"""

import httpx
from print_response import print_response

# Request timeout (default is 5 seconds and sometimes fails)
TIMEOUT = 20


def main():
    """
    Execution begins here.
    """

    # Define base URL for preferred sandbox
    # api_path = "https://sandbox-sdwan-1.cisco.com"
    api_path = "https://sandbox-sdwan-2.cisco.com"

    # These credentials are supplied by Cisco DevNet on the sandbox page:
    # https://developer.cisco.com/sdwan/learn/
    creds = {"j_username": "devnetuser", "j_password": "RG!_Yw919_83"}

    # Open "client" session and issue POST request. "data" will unpack the dict
    # into key/value pairs. Also, disable SSL validation
    with httpx.Client(verify=False) as client:
        auth_resp = client.post(
            f"{api_path}/j_security_check", data=creds, timeout=TIMEOUT
        )

        # Optional debugging statement
        # breakpoint()  # py3.7+
        # import pdb; pdb.set_trace()  # py3.6-

        # An authentication request has failed if we receive a failing return
        # code OR if there is any text supplied in the response. Failing auth
        # often return code 200 (OK) but includes any HTML content, indicating
        # a failure. If a failure does occur, exit the program using code 1.
        if auth_resp.is_error or auth_resp.text:
            raise httpx.HTTPStatusError(
                message="Authentication failed",
                request=auth_resp.request,
                response=auth_resp,
            )

        # Authentication succeeded; issue HTTP GET to collect devices
        dev_resp = client.get(f"{api_path}/dataservice/device", timeout=TIMEOUT)
        dev_resp.raise_for_status()
        print_response(dev_resp, filename="get_cisco_sdwan_devices")


if __name__ == "__main__":
    main()
