import requests

import config


class ApiService:
    BASE_URL = config.base_url

    @classmethod
    def _generate_url(cls, action_url):
        if action_url:
            return cls.BASE_URL + action_url

        return cls.BASE_URL

    @classmethod
    def get(cls, action_url):
        url = cls._generate_url(action_url)
        response = requests.get(url=url)
        return response

    @classmethod
    def post(cls, body, action_url=None):
        url = cls._generate_url(action_url)
        response = requests.post(url=url, json=body)
        return response


class UserService:

    @staticmethod
    def find_user(data, id):
        for item in data:
            if item.get('id') == id:
                return item

        return None
