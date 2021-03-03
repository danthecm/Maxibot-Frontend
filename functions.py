from binance.client import Client

def get_asset_balance(api_key, secret_key, symbol):
    try:
        client = Client(api_key, secret_key)
        balance = client.get_asset_balance(asset=symbol)
        return format(round(float(balance["free"]), 6), 'f')
    except Exception as e:
        print(e)
        return "not found"