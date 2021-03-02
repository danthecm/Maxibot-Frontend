from binance.client import Client
# from settings import api_key_new, api_secret_new
# import settings as s
import time
# Insert API and Secret key in quotation mark


def Current(api_key, secret_key, product, amount, margin_p, sell_p, trades):
    while True:
        try:
            client = Client(api_key, secret_key)
            print(client.API_URL)
            current_symbol = product
            open_orders = client.get_open_orders(symbol=current_symbol)
            btc_balance = client.get_asset_balance(asset="BNB")
            usdt_balance = client.get_asset_balance(asset="GBP")
            # all_orders = client.get_all_orders(symbol=current_symbol)

            buy_id = []
            sell_id = []

            counter = 0
            print(len(open_orders))
            print(open_orders)

            # for order in open_orders:
            #     cancel_or = client.cancel_order(symbol=current_symbol, orderId=order["orderId"])

            open_orders = client.get_open_orders(symbol=current_symbol)
            print(f"Welcome your BTC balance is {btc_balance}")
            print(f"Your GBP balance is {usdt_balance}")
            print(f"You have {len(open_orders)} Open Order")
            fees = client.get_trade_fee(symbol=current_symbol)
            print(f"the trading fee is {fees}")
            while counter < trades:
                open_orders = client.get_open_orders(symbol=current_symbol)
                print(f"starting running counter = {counter}")
                btc_price = client.get_symbol_ticker(symbol=current_symbol)
                btc_price = float(btc_price["price"])
                if len(open_orders) < 100 and len(buy_id) < 1:
                    print(f"The current price is {btc_price}")
                    print(f"Started calculating buy order \n number of trade currently at {counter}")
                    margin_p = 1 - float(margin_p / 100)
                    print(margin_p)
                    margin_p = round(margin_p, 2)
                    buy_price = btc_price * margin_p
                    buy_price = round(buy_price, 2)
                    amount = float(amount)
                    print(f"Margin Percent Entered {margin_p}")
                    print(f"Amount Entered {amount}")
                    quantity = float(amount/buy_price)
                    quantity = round(quantity, 3)
                    print(f"Quantity Entered {quantity}")
                    print(f"Buy price is {buy_price} and current price is {btc_price}")
                    print(f"ABOUT TO PLACE BUY ORDER")
                    buy_order = client.order_limit_buy(
                        symbol=current_symbol,
                        quantity=quantity,
                        price=buy_price)
                    print(f"{buy_price}")
                    buy_id.append(buy_order['orderId'])
                    counter += 1
                    print(f"Successfully Placed Buy Order for {quantity} of {product} at {buy_price}")
                    print(buy_id)
                    continue
                if len(buy_id) > 0:
                    print("Initing sell order")
                    for id in buy_id:
                        print("Looping through buy order id")
                        order = client.get_order(symbol=current_symbol, orderId=id)
                        while True:
                            try:
                                order = client.get_order(symbol=current_symbol, orderId=id)
                                print("check buy order status ")
                                if order['status'] == "FILLED":
                                    print(f"Calculating Sell Price")
                                    order_price = float(order["price"])
                                    sell_p = float(sell_p / 100)
                                    sell_price = order_price + (order_price * sell_p)
                                    sell_price = round(sell_price, 2)
                                    sell_qty = float(order["origQty"])
                                    buy_order = client.order_limit_sell(
                                        symbol=current_symbol,
                                        quantity=sell_qty,
                                        price=sell_price)
                                    sell_id.append(sell_order["orderId"])
                                    counter += 1
                                    print(sell_id)
                                    print(f"Successfully Placed Buy Order for {sell_qty} of {product} at {sell_price}")
                                    break
                            except Exception:
                                print("There was an error retrying soon ")
                                continue
                            time.sleep(5)

                    break
        except Exception as e:
            print(f"{e} \n There was an error retryin ASAP")
            time.sleep(10)
            continue
        break

# while trades <= 3:
#     open_orders = client.get_open_orders(symbol='BTCUSDT')
#     btc_price = client.get_symbol_ticker(symbol="BTCUSDT")
#     btc_bal = client.get_asset_balance(asset="BTC")
#     if len(open_orders) < 3:
#         btc_price = float(btc_price['price'])
#         buy_price = btc_price - (btc_price * margin_percent)
#         print(btc_price)
# Current("kYxAXqc5F1q6WKdwCgn6erWaWo2sAf2k8iK8xawEIVPOel2oBmTTisjwf6DavQRe", "LqLDBStDa1BPACEQ1Dryml1zQTWS8YMmnsvkLDoUhPNpjPHtoptaBPrbDTFgQHCL", "BTCUSDT", 0.02, 0.04, 2)
