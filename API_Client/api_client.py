import logging

import requests


class Client_Exception(Exception):
    def __init__(self, response) -> None:
        self.response = response


class APIClient:
    def __init__(
            self, base_url: str,
            auth_endpoint: str,
            username: str,
            password: str,
            refresh_endpoint: str = None
    ) -> None:
        self.__base_url = base_url
        self.__auth_endpoint = auth_endpoint
        self.__refresh_endpoint = refresh_endpoint
        self.__username = username
        self.__password = password

        self.__session = requests.Session()
        self.__access_token = self.__login()

    def __enter__(self) -> "APIClient":
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback) -> None:
        self.__access_token = None
        del self

    def __login(self) -> str:
        credentials = {
            "username": self.__username,
            "password": self.__password
        }

        try:
            if self.__refresh_endpoint is not None:
                response = self.__session.post(f"{self.__base_url}{self.__refresh_endpoint}")

                if response.status_code == 202:
                    return response.json().get("access_token")

            response = self.__session.post(f"{self.__base_url}{self.__auth_endpoint}", data=credentials)

            if response.status_code == 202:
                return response.json().get("access_token")

        except ConnectionError as e:
            logging.error(f"a connection error occurred: {e}")
            return self.__login()

        logging.critical(
            f"failed to authenticate at {self.__base_url}{self.__auth_endpoint} with username={self.__username}"
        )
        raise Client_Exception(response)

    def post(self, url: str, data: dict, retry: bool = False) -> dict:
        headers = {
            "Authorization": f"Bearer {self.__access_token}"
        }

        response = requests.post(f"{self.__base_url}/{url}", json=data, headers=headers)

        if response.status_code == 201:
            return response.json()

        if response.status_code == 401 and not retry:
            self.__access_token = self.__login()
            return self.post(url, data, True)

        logging.warning(f"adding entry with data={data} at '{url}' failed: {response.status_code} - {response.reason}")
        raise Client_Exception(response)

    def post_all(self, url: str, data: list[dict]) -> list[dict]:
        responses = []

        for entry in data:
            try:
                answer = self.post(url, entry)
            except Exception as e:
                answer = e

            responses.append(answer)

        return responses

    def get(self, url: str, retry: bool = False) -> dict | list[dict]:
        headers = {
            "Authorization": f"Bearer {self.__access_token}"
        }

        response = requests.get(f"{self.__base_url}/{url}", headers=headers)

        if response.status_code == 200:
            return response.json()

        if response.status_code == 401 and not retry:
            self.__access_token = self.__login()
            return self.get(url, True)

        logging.warning(f"getting data at '{url}' failed: {response.status_code} - {response.reason}")
        raise Client_Exception(response)

    def delete(self, url: str, retry: bool = False) -> None:
        headers = {
            "Authorization": f"Bearer {self.__access_token}"
        }

        response = requests.delete(f"{self.__base_url}/{url}", headers=headers)

        if response.status_code == 204:
            return

        if response.status_code == 401 and not retry:
            self.__access_token = self.__login()
            return self.delete(url, True)

        logging.warning(
            f"deleting data at '{url}' failed: {response.status_code} - {response.reason}")
        raise Client_Exception(response)

    def delete_all(self, urls: list[str]) -> list:
        responses = []

        for url in urls:
            try:
                responses.append(self.delete(url))
            except Exception as e:
                responses.append(e)

        return responses
