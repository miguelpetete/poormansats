import requests

class APIRepository:
    def __init__(self, base_url, auth):
        self.base_url = base_url
        self.auth = auth
    
    def get(self, endpoint, params=None):
        url = f''
        response = requests.get(url, params=params, auth=self.auth)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f'GET request to {url} returned status code {response.status_code}')
    
    def post(self, endpoint, data, headers=None):
        url = f''
        response = requests.post(url, json=data, headers=headers, auth=self.auth)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f'POST request to {url} returned status code {response.status_code}')

    def put(self, endpoint, data, headers=None):
        url = f''
        response = requests.put(url, json=data, headers=headers, auth=self.auth)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f'PUT request to {url} returned status code {response.status_code}')
    
    def delete(self, endpoint):
        url = f''
        response = requests.delete(url, auth=self.auth)
        if response.status_code == 200:
            return f''
        else:
            raise Exception(f'DELETE request to {url} returned status code {response.status_code}')