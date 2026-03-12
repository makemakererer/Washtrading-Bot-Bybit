import requests
import hmac
import hashlib

class Bybit:
    def __init__(self, APIKEY: str, APISECRET: str):
        self.apikey = APIKEY
        self.apisecret = APISECRET
        self.baseURL = 'https://api.bybit.com'

        endpoint = '/v5/market/time'
        url = f'{self.baseURL}{endpoint}'
        response = requests.get(url)
        self.timestamp = str(int(response.json()['result']['timeSecond']) * 1000)

    def get_coin_balance(self, coin):
        recv_window = "5000"
        queryString = f"accountType=SPOT&coin={coin}"
        sign_string = self.timestamp + self.apikey + recv_window + queryString

        signature = hmac.new(self.apisecret.encode('utf-8'), sign_string.encode('utf-8'), hashlib.sha256).hexdigest()

        headers = {
            'X-BAPI-SIGN': signature,
            'X-BAPI-API-KEY': self.apikey,
            'X-BAPI-TIMESTAMP': self.timestamp,
            'X-BAPI-RECV-WINDOW': recv_window,
        }

        url = 'https://api.bybit.com/v5/account/wallet-balance?' + queryString


        response = requests.get(url, headers=headers)
        print(response.json())

    def withdraw_token_info(self, coin):
        recv_window = "5000"
        queryString = f"coin={coin}"
        sign_string = self.timestamp + self.apikey + recv_window + queryString

        signature = hmac.new(self.apisecret.encode('utf-8'), sign_string.encode('utf-8'), hashlib.sha256).hexdigest()

        headers = {
            'X-BAPI-SIGN': signature,
            'X-BAPI-API-KEY': self.apikey,
            'X-BAPI-TIMESTAMP': self.timestamp,
            'X-BAPI-RECV-WINDOW': recv_window,
        }

        url = 'https://api.bybit.com/v5/asset/coin/query-info?' + queryString

        response = requests.get(url, headers=headers)
        chains = response.json()['result']['rows'][0]['chains']

        for chain in chains:
            print(chain['chainType'], chain['withdrawFee'])

