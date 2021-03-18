from binance.client import Client


def get_asset_balance(api_key, secret_key, symbol):
    try:
        client = Client(api_key, secret_key)
        balance = client.get_asset_balance(asset=symbol)
        return format(round(float(balance["free"]), 6), 'f')
    except Exception as e:
        print(e)
        return "not found"


def get_order(api_key, secret_key, pairs, order_id):
    try:
        client = Client(api_key, secret_key)
        order = client.get_order(
            symbol=pairs,
            orderId=order_id)
        return order
    except Exception as e:
        print(e)

def get_all_order(api_key, secret_key):
    try:
        client = Client(api_key, secret_key)
        order = client.get_all_orders(symbol="CHZGBP")
        print(order)
        return order
    except Exception as e:
        print(e)