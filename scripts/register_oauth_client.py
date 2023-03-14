#!/usr/bin/env python

import os
import json
import argparse
from pprint import pprint
from pathlib import Path
import yaml

import requests
from requests.auth import HTTPBasicAuth

from config import (
    AIDBOX_HOST,
    AIDBOX_PORT,
    AIDBOX_ADMIN_CLIENT_ID,
    AIDBOX_ADMIN_CLIENT_SECRET,
    BASE_URL,
)


def register_client(client_file, client_secret):
    """
    Register a new OAuth2 client with Aidbox. Grant type: client credentials
    """
    with open(client_file, "r") as yaml_file:
        payload = yaml.safe_load(yaml_file)
    payload["secret"] = client_secret
    client_id = payload["id"]

    print(f"🛠️  Registering new OAuth2 client {client_id}")
    headers = {
        "Content-Type": "application/json",
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


def cli():
    """
    CLI for running this script
    """
    parser = argparse.ArgumentParser(
        description='Register OAuth 2 client with client credentials grant'
    )
    parser.add_argument(
        "client_file",
        type=lambda p: Path(p).absolute(),
        help="Path to the client file",
    )
    parser.add_argument(
        "client_secret",
        help="Client secret for the client defined in client_file",
    )
    args = parser.parse_args()

    register_client(args.client_file, args.client_secret)

    print("✅ OAuth2 client registration complete")


if __name__ == "__main__":
    cli()
