from pybit.unified_trading import HTTP

with open('keys_bybt.txt', 'r') as file:
    lines = file.readlines()

api = [line.strip().split(':') for line in lines]

def exchange_stablecoins(api_key, api_secret, needed_trading_volume, after_timestamp):
    session = HTTP(
        testnet=False,
        api_key=api_key,
        api_secret=api_secret,
    )

    while True:
        trading_value = check_trading_value(session, after_timestamp)
        print(f'trading value now {trading_value} needed {needed_trading_volume}')

        if trading_value >= needed_trading_volume:
            break

        truncated_usdc_bal, truncated_usdt_bal = balances(session)

        if truncated_usdc_bal > 1.0:
            session.place_order(
                category="spot",
                symbol="USDCUSDT",
                side="Sell",
                orderType="Market",
                qty=truncated_usdc_bal
            )
        if truncated_usdt_bal > 1.0:
            session.place_order(
                category="spot",
                symbol="USDCUSDT",
                side="Buy",
                orderType="Market",
                qty=truncated_usdt_bal
            )

    truncated_usdc_bal, truncated_usdt_bal = balances(session)

    if truncated_usdt_bal < 1.0:
        session.place_order(
            category="spot",
            symbol="USDCUSDT",
            side="Sell",
            orderType="Market",
            qty=truncated_usdc_bal
        )
        print('Finnaly changed to usdt')

def check_trading_value(session, after_timestamp):
    orders_response = session.get_order_history(
        category="spot",
        limit=1000,
    )

    orders = orders_response['result']['list']
    trading_amount = 0  

    for order in orders:
        if int(order['updatedTime']) > after_timestamp:
            trading_amount += float(order['qty'])

    return trading_amount

def balances(session):
    usdc_balance_raw = session.get_wallet_balance(
        accountType="SPOT",
        coin="USDC",
    )

    usdt_balance_raw = session.get_wallet_balance(
        accountType="SPOT",
        coin="USDT",
    )

    try:
        usdc_bal = usdc_balance_raw['result']['list'][0]['coin'][0]['walletBalance']
        integer_part, decimal_part = usdc_bal.split('.')
        truncated_usdc_bal = float(integer_part + '.' + decimal_part[:2])
    except:
        truncated_usdc_bal = 0.0

    try:
        usdt_bal = usdt_balance_raw['result']['list'][0]['coin'][0]['walletBalance']
        integer_part, decimal_part = usdt_bal.split('.')
        truncated_usdt_bal = float(integer_part + '.' + decimal_part[:2])
    except:
        truncated_usdt_bal = 0.0

    return truncated_usdc_bal, truncated_usdt_bal

for index, (api_key, api_secret) in enumerate(api):
    print(f"BybitAcc: {index}, in work")
    needed_trading_volume = 25000
    start_snapshot = 1700179260

    exchange_stablecoins(api_key, api_secret, needed_trading_volume, start_snapshot)