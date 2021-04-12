import requests
from concurrent.futures import ThreadPoolExecutor

TEST_URL = "http://localhost:8080/test.html"
NETWORK_CODES = [200, 304, 400, 404, 408]


def request_connection(network_code):
    if network_code == 200:
        return requests.get(TEST_URL)
    elif network_code == 304:
        modified = {"If-Modified-Since": "Sat, 29 Oct 2021 19:43:31 GMT"}
        return requests.get(TEST_URL, headers=modified)
    elif network_code == 400:
        test = {'key': 'value'}
        return requests.post(TEST_URL, data=test)
    elif network_code == 404:
        return requests.get("http://localhost:8080/notFound")
    elif network_code == 408:
        return requests.get("http://localhost:8080/")


with ThreadPoolExecutor(max_workers=20) as pool:
    responses = list(pool.map(request_connection, NETWORK_CODES))
    print(responses)
