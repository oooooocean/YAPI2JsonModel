from urllib.parse import urljoin
import requests
import config


def fetch(api_id: str):
    url = urljoin(config.HOST, config.PATH)
    headers = {
        'Accept': 'application/json',
        'Cookie': f'_yapi_token={config.TOKEN}; _yapi_uid={config.UID}'
    }
    response = requests.get(url, params={'id': api_id}, headers=headers)
    json = response.json()
    if json['errcode'] != 0:
        raise requests.exceptions.RequestException(response=response)
    return json['data']
