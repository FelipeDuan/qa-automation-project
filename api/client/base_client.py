import requests
from requests.exceptions import RequestException, Timeout, ConnectionError


class BaseClient:
    def __init__(self, base_url, timeout=10):
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})

    def _make_request(self, method, endpoint, **kwargs):
        kwargs.setdefault('timeout', self.timeout)
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = self.session.request(method, url, **kwargs)
            return response
        except Timeout:
            raise TimeoutError(f"Request to {url} timed out after {self.timeout}s")
        except ConnectionError:
            raise ConnectionError(f"Failed to connect to {url}")
        except RequestException as e:
            raise Exception(f"Request failed: {str(e)}")

    def get(self, endpoint, **kwargs):
        return self._make_request("GET", endpoint, **kwargs)

    def post(self, endpoint, **kwargs):
        return self._make_request("POST", endpoint, **kwargs)

    def put(self, endpoint, **kwargs):
        return self._make_request("PUT", endpoint, **kwargs)

    def delete(self, endpoint, **kwargs):
        return self._make_request("DELETE", endpoint, **kwargs)
