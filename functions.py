from binance.client import Client

def get_asset_balance(api_key, secret_key, symbol):
    try:
        client = Client(api_key, secret_key)
        balance = client.get_asset_balance(asset=symbol)
        return format(round(float(balance["free"]), 6), 'f')
    except Exception as e:
        print(e)
        return "not found"
def get_assest_details(api_key, secret_key):
    try:
        client = Client(api_key, secret_key)
        details = client.get_asset_details()
        print(details)
    except Exception as e:
        print(e)