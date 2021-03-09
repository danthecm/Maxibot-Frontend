from binance.client import Client
from db import new_order
# from settings import api_key_new, api_secret_new
# import settings as s
import time
import re
# Insert API and Secret key in quotation mark


def Current(user_id, api_key, secret_key, product, amount, margin_p, sell_p, trades):
    strategy = "Current"
    try:
        client = Client(api_key, secret_key)
        first_index = 0
        for i in range(len(product)):
            if product[i] == "/":
                first_index = i
                break
        second_index = first_index + 1
        first_symbol = product[0:first_index]
        second_symbol = product[second_index:]
        pairs = f"{first_symbol}{second_symbol}"
        open_orders = client.get_open_orders(symbol=pairs)
        first_coin_balance = client.get_asset_balance(asset=first_symbol)
        second_coin_balance = client.get_asset_balance(asset=second_symbol)

        print(f"Welcome your {first_symbol} balance is {first_coin_balance}")
        print(f"You are using the Current Strategy")
        print(f"Your {second_symbol} balance is {second_coin_balance}")
        open_orders = client.get_open_orders(symbol=pairs)
        print(f"You have {len(open_orders)} Open Order")

        buy_id = []
        sell_id = []

        retries = 0
    except Exception as e:
        print(e)
        print("Cound not connect")
    while True:
        try:
            # all_orders = client.get_all_orders(symbol=pairs)
            counter = 0

            # for order in open_orders:
            #     cancel_or = client.cancel_order(symbol=pairs, orderId=order["orderId"])

            fees = client.get_trade_fee(symbol=pairs)
            fee = float(fees["tradeFee"][0]["taker"])
            while counter < trades:
                open_orders = client.get_open_orders(symbol=pairs)
                print(f"starting running counter = {counter}")
                first_coin_price = client.get_symbol_ticker(symbol=pairs)
                first_coin_price = float(first_coin_price["price"])

                # STOP INFINATE RETRIES
                if retries > 5 and len(buy_id) == 0:
                    message = "There were to many retries i have to cancle"
                    print(message)
                    break
                print(f"Retry currently at {retries} ")
                # CHECK BUY ORDER AND PLACE ORDER
                if len(open_orders) < 100 and len(buy_id) < 3:
                    print(f"The current price is {first_coin_price}")
                    margin_p = 1 - float(margin_p / 100)
                    print(margin_p)
                    margin_p = round(margin_p, 2)
                    buy_price = first_coin_price * margin_p
                    buy_price = buy_price - (buy_price * fee)
                    buy_price = round(buy_price, 2)
                    amount = float(amount)
                    print(f"Margin Percent Entered {margin_p}")
                    print(f"Amount Entered {amount}")
                    quantity = float(amount/buy_price)
                    quantity = round(quantity, 5)
                    print(f"quantity without regular express is {quantity} ")
                    # FORMAT QUANTITY USING REGULAR EXPRESSION
                    pattern = re.compile(r"([0-9]{1,}[.][0]{,5}[1-9]{,2})")
                    matches = pattern.match(str(quantity))
                    quantity = float(matches.group())

                    print(f"Quantity Entered {quantity}")
                    print(f"Buy price is {buy_price} and current price is {first_coin_price}")
                    print(f"ABOUT TO PLACE BUY ORDER")
                    buy_order = client.order_limit_buy(
                        symbol=pairs,
                        quantity=quantity,
                        price=buy_price)
                    print(f"{buy_price}")
                    new_order(user_id, strategy, pairs, buy_order["orderId"], time.time())
                    buy_id.append(buy_order['orderId'])
                    counter += 1
                    print(f"Successfully Placed Buy Order for {quantity} of {product} at {buy_price}")
                    print(buy_id)
                    continue
                
                if len(buy_id) > 0:
                    print("Initing sell order")
                    for id in buy_id:
                        print("Looping through buy order id")
                        order = client.get_order(symbol=pairs, orderId=id)
                        while True:
                            try:
                                order = client.get_order(symbol=pairs, orderId=id)
                                print("check buy order status ")
                                if order['status'] == "FILLED":
                                    print(f"Calculating Sell Price")
                                    order_price = float(order["price"])
                                    sell_p = float(sell_p / 100)
                                    sell_price = order_price + (order_price * sell_p)
                                    sell_price = sell_price + (sell_price * fee)
                                    sell_price = round(sell_price, 2)
                                    sell_qty = float(order["origQty"])
                                    sell_order = client.order_limit_sell(
                                        symbol=pairs,
                                        quantity=sell_qty,
                                        price=sell_price)
                                    new_order(user_id, strategy, pairs, sell_order["orderId"], time.time())
                                    sell_id.append(sell_order["orderId"])
                                    counter += 1
                                    print(sell_id)
                                    print(f"Successfully Placed Sell order for {sell_qty} of {product} at {sell_price} you bought it at {buy_price}")
                                    message = "All succesful"
                                    break
                            except Exception:
                                print("There was an error retrying soon ")
                                retries += 1
                                continue
                            time.sleep(30)
                    break
        except Exception as e:
            print(f"{e} \n There was an error retryin ASAP")
            retries += 1
            time.sleep(10)
            continue
        break

# while trades <= 3:
#     open_orders = client.get_open_orders(symbol='BTCUSDT')
#     first_coin_price = client.get_symbol_ticker(symbol="BTCUSDT")
#     btc_bal = client.get_asset_balance(asset="BTC")
#     if len(open_orders) < 3:
#         first_coin_price = float(first_coin_price['price'])
#         buy_price = first_coin_price - (first_coin_price * margin_percent)
#         print(first_coin_price)
# Current("kYxAXqc5F1q6WKdwCgn6erWaWo2sAf2k8iK8xawEIVPOel2oBmTTisjwf6DavQRe", "LqLDBStDa1BPACEQ1Dryml1zQTWS8YMmnsvkLDoUhPNpjPHtoptaBPrbDTFgQHCL", "BTCUSDT", 0.02, 0.04, 2)

def Average(user_id, api_key, secret_key, product, amount, margin_p, sell_p, trades):
    strategy = "Average"
    try:
        client = Client(api_key, secret_key)
        first_index = 0
        for i in range(len(product)):
            if product[i] == "/":
                first_index = i
                break
        second_index = first_index + 1
        first_symbol = product[0:first_index]
        second_symbol = product[second_index:]
        pairs = f"{first_symbol}{second_symbol}"
        open_orders = client.get_open_orders(symbol=pairs)
        first_coin_balance = client.get_asset_balance(asset=first_symbol)
        second_coin_balance = client.get_asset_balance(asset=second_symbol)

        print(f"Welcome your {first_symbol} balance is {first_coin_balance}")
        print("You are using the Average Strategy")
        print(f"Your {second_symbol} balance is {second_coin_balance}")
        open_orders = client.get_open_orders(symbol=pairs)
        print(f"You have {len(open_orders)} Open Order")

        buy_id = []
        sell_id = []
        all_buy_price = []
        all_buy_qty = []
        retries = 0

        def buyTrades(trade):
            if trade["side"] == "BUY" and trade["status"] == "FILLED":
                price = float(trade["price"])
                qty = float(trade["origQty"])
                total_cost = price * qty
                all_buy_price.append(total_cost)
                all_buy_qty.append(qty)
                return True

    except Exception as e:
        print(e)
        print("Cound not connect")
    while True:
        try:
            counter = 0
            total_price = 0
            total_qty = 0
            fees = client.get_trade_fee(symbol=pairs)
            fee = float(fees["tradeFee"][0]["taker"])
            while counter < trades:
                open_orders = client.get_open_orders(symbol=pairs)
                print(f"starting running counter = {counter}")
                first_coin_price = client.get_symbol_ticker(symbol=pairs)
                first_coin_price = float(first_coin_price["price"])

                # STOP INFINATE RETRIES
                if retries > 5 and len(buy_id) == 0:
                    message = "There was an error"
                    print(message)
                    break
                print(f"Retry currently at {retries} ")
                # CHECK BUY ORDER AND PLACE ORDER
                if len(open_orders) < 100 and len(buy_id) < 3:

                    # CALCULATE AVERAGE PRICE
                    orders = client.get_all_orders(symbol=pairs, limit=50)
                    buy_orders = filter(buyTrades, orders)
                    buy_orders = list(buy_orders)
                    for price in all_buy_price:
                        total_price += price
                    for qty in all_buy_qty:
                        total_qty += qty
                    average = total_price/total_qty


                    print(f"The average price is {average}")
                    margin_p = 1 - float(margin_p / 100)
                    margin_p = round(margin_p, 2)
                    if average > first_coin_price:
                        average = first_coin_price
                    buy_price = average * margin_p
                    buy_price = buy_price - (buy_price * fee)
                    buy_price = round(buy_price, 2)
                    amount = float(amount)
                    print(f"Margin Percent Entered {margin_p}")
                    print(f"Amount Entered {amount}")
                    print(f"the buy price is {buy_price}")
                    quantity = float(amount/buy_price)
                    quantity = round(quantity, 5)
                    print(f'Quantity without regex formating {quantity} ')

                    # FORMAT QUANTITY USING REGULAR EXPRESSION
                    pattern = re.compile(r"([0-9]{1,}[.][0]{,5}[1-9]{,2})")
                    matches = pattern.match(str(quantity))
                    quantity = float(matches.group())

                    print(f"Quantity Entered {quantity}")
                    print(f"Buy price is {buy_price} and current price is {first_coin_price}")
                    print(f"ABOUT TO PLACE BUY ORDER")
                    buy_order = client.order_limit_buy(
                        symbol=pairs,
                        quantity=quantity,
                        price=buy_price)
                    print(f"{buy_price}")
                    new_order(user_id, strategy, pairs, buy_order["orderId"], time.time())
                    buy_id.append(buy_order['orderId'])
                    counter += 1
                    print(f"Successfully Placed Buy Order for {quantity} of {product} at {buy_price}")
                    print(buy_id)
                    continue
                
                if len(buy_id) > 0:
                    print("Initing sell order")
                    for id in buy_id:
                        print("Looping through buy order id")
                        order = client.get_order(symbol=pairs, orderId=id)
                        while True:
                            try:
                                order = client.get_order(symbol=pairs, orderId=id)
                                print("check buy order status ")
                                if order['status'] == "FILLED":
                                    print(f"Calculating Sell Price")
                                    order_price = float(order["price"])
                                    sell_p = float(sell_p / 100)
                                    sell_price = order_price + (order_price * sell_p)
                                    sell_price = sell_price + (sell_price * fee)
                                    sell_price = round(sell_price, 2)
                                    sell_qty = float(order["origQty"])
                                    sell_order = client.order_limit_sell(
                                        symbol=pairs,
                                        quantity=sell_qty,
                                        price=sell_price)
                                    new_order(user_id, strategy, pairs, sell_order["orderId"], time.time())
                                    sell_id.append(sell_order["orderId"])
                                    counter += 1
                                    print(sell_id)
                                    print(f"Successfully Placed Sell order for {sell_qty} of {product} at {sell_price} you bought it at {buy_price}")
                                    message = "All succesful"
                                    break
                            except Exception:
                                print("There was an error retrying soon ")
                                retries += 1
                                continue
                            time.sleep(30)
                    break
        except Exception as e:
            print(f"{e} \n There was an error retryin ASAP")
            retries += 1
            time.sleep(10)
            continue
        break
