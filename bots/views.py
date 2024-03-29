from difflib import restore
from email import header
from sys import platform
from flask import Blueprint, redirect, url_for, render_template, request, flash, session, abort
import requests, os
import time as t

from flask_login import login_required, current_user
from flask_paginate import Pagination

from requests.exceptions import ConnectionError


maxi_backend = os.getenv(
    "MAXIBOT_BACKEND", "http://132.226.211.117")
bots_blueprint = Blueprint("bots", __name__, template_folder="templates")


@bots_blueprint.route("/new", methods=["POST"])
@login_required
def add():
    form = request.form
    my_json = {**form}
    try:
        if session["platform"]["name"] == "Binance":
            from binance import Client
            client = Client()
            current_price = client.get_symbol_ticker(symbol=my_json["pairs"])
            current_price = float(current_price["price"])
        elif session["platform"]["name"] == "Coinbase Pro":
            from cbpro import PublicClient
            client = PublicClient()
            current_price = client.get_product_ticker(my_json["pairs"])
            current_price = float(current_price["price"])
        elif session["platform"]["name"] == "Kraken":
            from krakenex import API
            client = API()
            pairs = my_json.get("pairs")
            current_price_query = client.query_public("Ticker", {"pair": pairs})
            current_price_query = current_price_query.get("result")
            current_price = float(current_price_query.get(pairs).get("c")[0])
        my_json["current_price"] = current_price
        my_json["status"] = "RUNNING"
        bot_req = requests.post(f"{maxi_backend}/new_bot", json=my_json, headers=session["headers"])
        if bot_req.status_code == 201:
            flash("Successfully created", "success")
        else:
            flash(f"{bot_req.text}", "warning")
    except Exception as e:
        flash("There was an error creating a new bot", "danger")
    return redirect(url_for("users.dashboard"))

@bots_blueprint.route("/<int:id>")
@bots_blueprint.route("/<int:id>/<int:page>")
@login_required
def view(id, page=1):
    bot_req = requests.get(f"{maxi_backend}/bot/{id}")
    if bot_req.status_code == 200:
        bot = bot_req.json()
        orders = []
        open_orders = list(filter(lambda x: x["status"].lower() == "open", bot.get("orders")))
        closed_orders = list(filter(lambda x: x["status"].lower() == "close", bot.get("orders")))
        filled_orders = list(filter(lambda x: x["status"].lower() == "filled", bot.get("orders")))
        def append_list(name, lists):
            for list in lists:
                for item in list:
                    name.append(item)
        append_list(orders,[open_orders, closed_orders, filled_orders])
        pagination = Pagination(page=page, per_page=5, total=len(orders), record_name='orders')
        my_orders = orders[(pagination.per_page * (page - 1)):(pagination.per_page * page)]
        return render_template("bot.html", bot=bot, orders=my_orders, pagination=pagination)

@bots_blueprint.route("/edit/<int:id>", methods=["POST"])
@login_required
def edit(id):
    data = request.form
    json_data = {**data}
    edit_req = requests.put(f"{maxi_backend}/bot/{id}", headers=session["headers"], json=json_data)
    flash("Successfully updated the bot info", "success")
    return redirect(url_for("bots.view", id=id))


@bots_blueprint.route("/pause/<int:id>")
@login_required
def pause(id):
    json = {"status": "PAUSED"}
    pause_req = requests.patch(f"{maxi_backend}/bot/{id}", headers=session["headers"], json=json)
    if pause_req.status_code > 200:
        flash("There was an error pausing this bot", "warning")
    else:
        flash("Successfully paused the bot", "success")
    return redirect(url_for("bots.view", id=id))

@bots_blueprint.route("/play/<int:id>")
@login_required
def play(id):
    json = {"status": "RUNNING"}
    pause_req = requests.patch(f"{maxi_backend}/bot/{id}", headers=session["headers"], json=json)
    if pause_req.status_code > 200:
        flash("There was an error resuming this bot", "warning")
    else:
        flash("Successfully resumed the bot", "success")
    return redirect(url_for("bots.view", id=id))


@bots_blueprint.route("/delete/<int:id>")
@login_required
def delete(id):
    delete_req = requests.delete(f"{maxi_backend}/bot/{id}", headers=session["headers"])
    if delete_req.status_code > 200:
        flash("There was an error deleting this bot", "danger")
        return redirect(url_for("bots.view", id=id))
    flash("Bot successfully deleted", "success")
    return redirect(url_for("users.dashboard"))

@bots_blueprint.route("/reset/<int:id>")
@login_required
def reset(id):
    # json = {"status": "RESET"}
    # reset_req = requests.patch(f"{maxi_backend}/bot/{id}", headers=session["headers"], json=json)
    # if reset_req.status_code > 200 and id == 0:
    #     flash("Error reseting all the bots", "danger")
    #     return redirect(url_for("users.dashboard"))
    # elif reset_req.status_code > 200 and id != 0:
    #     flash("Error reseting this bot", "danger")
    #     return redirect(url_for("bots.view", id=id))
    flash("Bot reset feature is still in progress", "success")
    return redirect(url_for("users.dashboard" if id == 0 else "bots.view", id=id))