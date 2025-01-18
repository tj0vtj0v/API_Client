import logging

import requests


class APIClient:
    def __init__(
            self, api_url: str,
            login_suffix: str,
            username: str,
            password: str,
            refresh_suffix: str = None
    ) -> None:
        self.__api_url = api_url
        self.__login_suffix = login_suffix
        self.__refresh_suffix = refresh_suffix
        self.__username = username
        self.__password = password

        self.__session = requests.Session()
        self.__access_token = self.__login()

    def __enter__(self) -> "APIClient":
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback) -> None:
        self.__access_token = None

    def __login(self) -> str:
        credentials = {
            "username": self.__username,
            "password": self.__password
        }

        try:
            if self.__refresh_suffix is not None:
                response = self.__session.post(f"{self.__api_url}{self.__refresh_suffix}")

                if response.status_code == 202:
                    return response.json().get("access_token")

            response = self.__session.post(f"{self.__api_url}{self.__login_suffix}", data=credentials)

            if response.status_code == 202:
                return response.json().get("access_token")

        except ConnectionError as e:
            logging.error(f"a connection error occurred: {e}")
            return self.__login()

        logging.critical(
            f"failed to authenticate at {self.__api_url}{self.__login_suffix} with username={self.__username}"
        )
        raise Exception(response.status_code)

    def post(self, url: str, data: dict, retry: bool = False) -> dict:
        headers = {
            "Authorization": f"Bearer {self.__access_token}"
        }

        response = requests.post(f"{self.__api_url}/{url}", json=data, headers=headers)

        if response.status_code == 201:
            return response.json()

        if response.status_code == 401 and not retry:
            self.__access_token = self.__login()
            return self.post(url, data, True)

        logging.warning(f"adding entry with data={data} at '{url}' failed: {response.status_code} - {response.reason}")
        raise Exception(response.status_code)

    def post_all(self, url: str, data: list[dict]) -> list[dict]:
        responses = []

        for entry in data:
            try:
                answer = self.post(url, entry)
            except Exception as e:
                answer = e

            responses.append(answer)

        return responses

    def get_data(self, url: str, retry: bool = False) -> dict | list[dict]:
        headers = {
            "Authorization": f"Bearer {self.__access_token}"
        }

        response = requests.get(f"{self.__api_url}/{url}", headers=headers)

        if response.status_code == 200:
            return response.json()

        if response.status_code == 401 and not retry:
            self.__access_token = self.__login()
            return self.get_data(url, True)

        logging.warning(f"getting data at '{url}' failed: {response.status_code} - {response.reason}")
        raise Exception(response.status_code)

    def delete(self, url: str, retry: bool = False) -> None:
        headers = {
            "Authorization": f"Bearer {self.__access_token}"
        }

        response = requests.delete(f"{self.__api_url}/{url}", headers=headers)

        if response.status_code == 204:
            return

        if response.status_code == 401 and not retry:
            self.__access_token = self.__login()
            return self.delete(url, True)

        logging.warning(
            f"deleting data at '{url}' failed: {response.status_code} - {response.reason}")
        raise Exception(response.status_code)

    def delete_all(self, urls: list[str]) -> list:
        responses = []

        for url in urls:
            try:
                responses.append(self.delete(url))
            except Exception as e:
                responses.append(e)

        return responses
