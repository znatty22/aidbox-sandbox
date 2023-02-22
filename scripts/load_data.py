#!/usr/bin/env python

import os
import json
import argparse
import time
from pprint import pprint

import requests
from requests.auth import HTTPBasicAuth

from config import (
    AIDBOX_HOST,
    AIDBOX_PORT,
    AIDBOX_ADMIN_CLIENT_ID,
    AIDBOX_ADMIN_CLIENT_SECRET,
    DATA_DIR,
    BASE_URL,
    FHIR_URL
)


def elapsed_time_hms(start_time):
    """
    Get time elapsed since start_time in hh:mm:ss str format
    """
    elapsed = time.time() - start_time
    return time.strftime('%H:%M:%S', time.gmtime(elapsed))


def get_oauth2_token(client_id, client_secret):
    """
    Exchange client credentials for Bearer token
    """
    print(f"Get Bearer token for {client_id}")
    headers = {
        "Content-Type": "application/json",
    }
    payload = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "client_credentials"
    }
    try:
        resp = requests.post(
            f"{BASE_URL}/auth/token",
            headers=headers,
            json=payload
        )
        resp.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print("Problem sending request to aidbox")
        print(resp.text)
        raise e

    return resp.json()["access_token"]


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
