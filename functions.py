from flask import request
from urllib.parse import urlparse, urljoin

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc

def get_asset_balance(client, symbol):
    try:
        balance = client.get_asset_balance(asset=symbol)
        return format(round(float(balance["free"]), 6), 'f')
    except Exception as e:
        print(e)
        return "not found"

def get_balance_coinbase(client, currency):
    accounts = client.get_accounts()
    balance = {u["currency"]: u for u in accounts}
    return balance[currency]["available"]

def get_kraken_balance(client, currency):
    # result = client.query_private("Balance")["result"]
    # return float(result.get(currency, 0))
    return "not found"

def get_all_order(api_key, secret_key):
    try:
        client = Client(api_key, secret_key)
        order = client.get_all_orders(symbol="CHZGBP")
        return order
    except Exception as e:
        print(e)