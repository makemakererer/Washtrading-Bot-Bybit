import os
from bybit_with_proxy import Bybit

from dotenv import load_dotenv
load_dotenv()

APIKEY=os.environ.get('APIKEY')
APISECRET=os.environ.get('APISECRET')

bybit_instance = Bybit(APIKEY, APISECRET)
bybit_instance.get_coin_balance('USDT')