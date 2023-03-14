#!/usr/bin/env python

import os
import json
import argparse
import time
from pprint import pprint

import requests
from requests.auth import HTTPBasicAuth

from config import (
    DATA_DIR,
    FHIR_URL
)
from scripts.misc import elapsed_time_hms, get_oauth2_token


def load_data(client_id, client_secret):
    """
    Register a new OAuth2 client with Aidbox. Grant type: client credentials
    """
    print(f"🛠️  Registering new OAuth2 client {client_id}")
    token = get_oauth2_token(client_id, client_secret)
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    start_time = time.time()
    for filename in os.listdir(DATA_DIR):
        filepath = os.path.join(DATA_DIR, filename)
        with open(filepath, "r") as json_file:
            data = json.load(json_file)
        endpoint = filename.split(".")[0]

        for i, resource in enumerate(data):
            try:
                print(f"Upserting {endpoint} {resource['id']}")
                resp = requests.put(
                    f"{FHIR_URL}/{endpoint}/{resource['id']}",
                    headers=headers,
                    json=resource
                )
                resp.raise_for_status()
            except requests.exceptions.HTTPError as e:
                print("Problem sending request to aidbox")
                print(resp.text)
                raise e
    print(f"\nElapsed time (hh:mm:ss): {elapsed_time_hms(start_time)}\n")


def cli():
    """
    CLI for running this script
    """
    parser = argparse.ArgumentParser(
        description='Setup aidbox app'
    )
    parser.add_argument(
        "client_id",
        help="Client ID to register with Aidbox",
    )
    parser.add_argument(
        "client_secret",
        help="Client secret to register with Aidbox",
    )
    args = parser.parse_args()

    load_data(args.client_id, args.client_secret)

    print("✅ Load data complete")


if __name__ == "__main__":
    cli()
