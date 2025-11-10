from prefect import task
import requests


@task
def fetch_nasa_data(base_url: str, api_key: str, endpoint: str) -> dict:
    url = f"{base_url}{endpoint}?api_key={api_key}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()
