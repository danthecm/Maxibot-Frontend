from binance.client import Client

api_key = "kYxAXqc5F1q6WKdwCgn6erWaWo2sAf2k8iK8xawEIVPOel2oBmTTisjwf6DavQRe"
secret_key = "LqLDBStDa1BPACEQ1Dryml1zQTWS8YMmnsvkLDoUhPNpjPHtoptaBPrbDTFgQHCL"
API_URL = 'https://api.binance.{}/api'

client = Client(api_key, secret_key)

# order = client.order_limit_sell(
#     symbol='BTCUSDT',
#     quantity=0.02,
#     price=47900
#     )
all_buy_price = []
all_buy_qty = []
def buyTrades(trade):
    if trade["side"] == "BUY" and trade["status"] == "FILLED":
        all_buy_price.append(float(trade["price"]))
        all_buy_qty.append(float(trade["origQty"]))
        return True

current_price = client.get_symbol_ticker(symbol="BTCUSDT")
btc_balance = client.get_asset_balance(asset="BTC")
usdt_balance = client.get_asset_balance(asset="USDT")
orders = client.get_all_orders(symbol='BTCUSDT')

buy_orders = filter(buyTrades, orders)
print(orders)
buy_orders = list(buy_orders)
print("OH OH OH OH \nWAIT WAIT WAIT WATIT \nokay okay")
total_price = 0
total_qty = 0
for price in all_buy_price:
    total_price += price
for qty in all_buy_qty:
    total_qty += qty
average = total_price/total_qty
print(total_price)
print(total_qty)
print(average)
print(current_price)
print(btc_balance)
print(usdt_balance)