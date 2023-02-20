#!/usr/bin/env python

import os
import json
import argparse
from pprint import pprint

import requests
from requests.auth import HTTPBasicAuth

from config import (
    AIDBOX_HOST,
    AIDBOX_PORT,
    AIDBOX_ADMIN_CLIENT_ID,
    AIDBOX_ADMIN_CLIENT_SECRET,
    BASE_URL,
)


def register_client(client_id, client_secret):
    """
    Register a new OAuth2 client with Aidbox. Grant type: client credentials
    """
    print(f"🛠️  Registering new OAuth2 client {client_id}")
    headers = {
        "Content-Type": "application/json",
    }
    payload = {
        "secret": client_secret,
        "grant_types": [
            "client_credentials"
        ]
    }
    try:
        resp = requests.put(
            f"{BASE_URL}/Client/{client_id}",
            auth=HTTPBasicAuth(
                AIDBOX_ADMIN_CLIENT_ID,
                AIDBOX_ADMIN_CLIENT_SECRET
            ),
            headers=headers,
            json=payload
        )
        resp.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print("Problem sending request to aidbox")
        print(resp.text)
        raise e


def setup_access_policy(client_id):
    """
    Set allow all access policy for OAuth2 client
    """
    print(f"🛂 Setup allow all access policy for {client_id}")

    headers = {
        "Content-Type": "application/json",
    }
    payload = {
        "engine": "allow",
        "link": [
            {
                "id": client_id,
                "resourceType": "Client"
            }
        ]
    }
    try:
        resp = requests.put(
            f"{BASE_URL}/AccessPolicy/{client_id}",
            auth=HTTPBasicAuth(
                AIDBOX_ADMIN_CLIENT_ID,
                AIDBOX_ADMIN_CLIENT_SECRET
            ),
            headers=headers,
            json=payload
        )
        resp.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print("Problem sending request to aidbox")
        print(resp.text)
        raise e


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

    register_client(args.client_id, args.client_secret)
    setup_access_policy(args.client_id)

    print("✅ OAuth2 client registration complete")


if __name__ == "__main__":
    cli()
