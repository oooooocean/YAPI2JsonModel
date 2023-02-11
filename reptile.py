from urllib.parse import urljoin
import requests
import config
from exceptions import ReptileError, ParseError
from json import loads, JSONDecodeError


def fetch(api_id: str) -> dict:
    url = urljoin(config.HOST, config.PATH)
    headers = {
        'Accept': 'application/json',
        'Cookie': f'_yapi_token={config.TOKEN}; _yapi_uid={config.UID}'
    }
    try:
        response = requests.get(url, params={'id': api_id}, headers=headers)
        json = response.json()
        if json['errcode'] != 0:
            raise ReptileError(f'数据错误: {json["errmsg"]}')
        data = loads(json['data']['res_body'])
    except JSONDecodeError as e:
        raise ParseError(f'json解析失败: {e.__str__()}')
    except KeyError as e:
        raise ParseError(f'解析失败: {e.__str__()}')
    except Exception as e:
        raise ReptileError(f'请求失败: {e.__str__()}')  # requests.exceptions.RequestException(response=response)
    else:
        return data['properties']
