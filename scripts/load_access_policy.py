#!/usr/bin/env python

import os
import json
import argparse
import time
from pprint import pprint
from pathlib import Path
import yaml

import requests
from requests.auth import HTTPBasicAuth

from config import (
    BASE_URL,
    AIDBOX_ADMIN_CLIENT_ID,
    AIDBOX_ADMIN_CLIENT_SECRET,

)
from scripts.misc import get_oauth2_token


def load_policy(policy_file, client_ids):
    """
    Create AccessPolicy for list of clients
    """
    with open(policy_file, "r") as yaml_file:
        policy = yaml.safe_load(yaml_file)

    policy_id = policy["id"]
    print(f"🛂 Apply access policy {policy_id} to {client_ids}")

    clients = [{"id": cid, "resourceType": "Client"} for cid in client_ids]
    policy["link"] = clients
    headers = {
        "Content-Type": "application/json",
    }
    try:
        resp = requests.put(
            f"{BASE_URL}/AccessPolicy/{policy_id}",
            auth=HTTPBasicAuth(
                AIDBOX_ADMIN_CLIENT_ID,
                AIDBOX_ADMIN_CLIENT_SECRET
            ),
            headers=headers,
            json=policy
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
        "policy_file",
        type=lambda p: Path(p).absolute(),
        help="Path to the access policy file",
    )
    parser.add_argument(
        "client_ids",
        type=lambda id_list: [id_.strip() for id_ in id_list.split(",")],
        help="List of client IDs to apply the policy to",
    )
    args = parser.parse_args()

    load_policy(args.policy_file, args.client_ids)

    print("✅ Load access policy complete")


if __name__ == "__main__":
    cli()
