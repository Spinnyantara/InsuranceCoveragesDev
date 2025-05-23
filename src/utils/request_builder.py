import requests


class RequestBuilder:
    @staticmethod
    def post(url, data, token=None, headers=None):
        h = headers or {}
        if token:
            h["Authorization"] = f"Bearer {token}"
        return requests.post(url, json=data, headers=h)

    @staticmethod
    def get(url, token=None, headers=None, params=None):
        h = headers or {}
        if token:
            h["Authorization"] = f"Bearer {token}"
        return requests.get(url, headers=h, params=params)
