from binance.client import Client

api_key = "kYxAXqc5F1q6WKdwCgn6erWaWo2sAf2k8iK8xawEIVPOel2oBmTTisjwf6DavQRe"
secret_key = "LqLDBStDa1BPACEQ1Dryml1zQTWS8YMmnsvkLDoUhPNpjPHtoptaBPrbDTFgQHCL"
def get_average(api_key, secret_key):
    try:
        client = Client(api_key, secret_key)
        all_buy_price = []
        all_buy_qty = []

        def buyTrades(trade):
            if trade["side"] == "BUY" and trade["status"] == "FILLED":
                all_buy_price.append(float(trade["price"]))
                all_buy_qty.append(float(trade["origQty"]))
                return True

        current_price = client.get_symbol_ticker(symbol="BNBGBP")
        first_coin = client.get_asset_balance(asset="BNB")
        second_coin = client.get_asset_balance(asset="GBP")
        orders = client.get_all_orders(symbol='BNBGBP')

        buy_orders = filter(buyTrades, orders)
        buy_orders = list(buy_orders)
        print(f"You've made a total of {len(orders)} orders")
        total_price = 0
        total_qty = 0
        for price in all_buy_price:
            total_price += price
        for qty in all_buy_qty:
            total_qty += qty
        average = total_price/total_qty
        average_p = client.get_avg_price(symbol="BNBGBP")
        print(f"The total buy amount is {total_price}")
        print(f"The total buy quantity is {total_qty}")
        print(f"The average price is {average}")
        print(f"The current price is {current_price}")
        print(f"{first_coin}")
        print(f"{second_coin}")
        print(f"Average from binance is {average_p}")
        return average_p
    except Exception as e:
        print(e)
        return "Your API KEY is invalid"