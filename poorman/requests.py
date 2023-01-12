import requests
from dotenv import dotenv_values

envs = dotenv_values(".env")
key = envs["AIRTABLE_KEY"]
baseID = envs["AIRTABLE_BASE_ID"]
tableID = envs["AIRTABLE_TABLE_ID"]

BASIC_URL = "https://api.airtable.com/v0/"


class APIRepository:
    def __init__(self, base_url, auth):
        self.base_url = base_url
        self.auth = auth

    def get(self, endpoint, params=None):
        url = BASIC_URL + str(baseID) + "/" + str(tableID)
        response = requests.get(url, params=params, auth=self.auth)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(
                f"GET request to {url} returned status code {response.status_code}"
            )

    def post(self, endpoint, data, headers=None):
        url = BASIC_URL + str(baseID) + "/" + str(tableID)
        response = requests.post(url, json=data, headers=headers, auth=self.auth)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(
                f"POST request to {url} returned status code {response.status_code}"
            )

    def put(self, endpoint, data, headers=None):
        url = BASIC_URL + str(baseID) + "/" + str(tableID)
        response = requests.put(url, json=data, headers=headers, auth=self.auth)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(
                f"PUT request to {url} returned status code {response.status_code}"
            )

    def delete(self, endpoint):
        url = BASIC_URL + str(baseID) + "/" + str(tableID)
        response = requests.delete(url, auth=self.auth)
        if response.status_code == 200:
            return f""
        else:
            raise Exception(
                f"DELETE request to {url} returned status code {response.status_code}"
            )
