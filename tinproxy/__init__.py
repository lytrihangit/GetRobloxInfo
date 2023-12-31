from .exceptions import ProxyError, CannotFetchProxyDataError

import requests


class TinProxy:
    BASE_URL = 'https://api.tinproxy.com/proxy'

    def __init__(self, api_key: str, user_agent: str):
        if api_key == "":
            return

        self.param = {
            'api_key': api_key
        }

        self.session = requests.Session()
        self.session.headers['User-Agent'] = user_agent

    def get_data(self, data: dict) -> tuple:
        try:
            data = data['data']
            authentication = data['authentication']
            http_ipv4 = data['http_ipv4']
            username = authentication['username']
            password = authentication['password']
            next_request = data['next_request']
            proxy = f'{username}:{password}@{http_ipv4}'

            return next_request, proxy
        except:
            pass

        raise CannotFetchProxyDataError(data)

    def get_current_proxy(self) -> tuple:
        response = self.session.get(
            url=f'{self.BASE_URL}/get-current-proxy',
            params=self.param
        )

        data = response.json()
        nex_request, proxy = self.get_data(data)

        if len(proxy) < 5:
            raise ProxyError(data)

        return nex_request, proxy

    def get_proxy(self) -> str:
        response = self.session.get(
            url=f'{self.BASE_URL}/get-new-proxy',
            params=self.param
        )

        data = response.json()
        _, proxy = self.get_data(data)

        if len(proxy) < 5:
            raise ProxyError(data)

        return proxy
