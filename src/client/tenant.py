"""
This is a client of another fake API.

It is used in this boilerplate to show how to mock an external API and how to
chaine errors between APIs.
"""
import requests

from src.config.pricing_config import pricing_data_source


def get_tenant_data():
    response = requests.get("{base_url}/readProductModelData".format(base_url=pricing_data_source["pricing_base_url"]))

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception('An error occurred in the fetching API response !')
