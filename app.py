from flask import Flask, flash, render_template, request, redirect, url_for, session, logging, session
from flask_login import login_required
# import db
import time as t
import os
import json
import requests

from functions import get_asset_balance, get_order
from binance.client import Client


from users.views import users_blueprint
from platforms.views import platform_blueprint
from bots.views import bots_blueprint
from login import login_manager

app = Flask(__name__)
app.secret_key = 'maxitest'
app.config['SESSION_TYPE'] = 'filesystem'
app.jinja_env.add_extension('jinja2.ext.do')
# app.config['CELERY_RESULT_BACKEND'] = 'db+mysql://admin:maxitest@maxitest.cepigw2nhp7p.us-east-2.rds.amazonaws.com/MaxiBot'
# app.config['CELERY_BROKER_URL'] = broker_url
maxi_backend = os.environ.get(
    "MAXIBOT_BACKEND", "http://127.0.0.1:5000/")

app.register_blueprint(users_blueprint)
app.register_blueprint(platform_blueprint, url_prefix="/platform")
app.register_blueprint(bots_blueprint, url_prefix="/bots")

login_manager.login_view = "users.login"

@app.route("/")
def index():
    return render_template("home.html")



@app.route("/logout")
def logout():
    session.clear()
    flash("Successfuly Logout out", "success")
    return redirect(url_for("login"))




@app.route("/new_trade", methods=["POST"])
@login_required
def new_trade():
    user_id = session["user_id"]
    pairs = request.form["pairs"]
    strategy = request.form["strategy"]
    print(user_id, pairs, strategy)
    my_pair = pairs
    try:
        client = Client()
        current_price = client.get_symbol_ticker(symbol=my_pair)
        current_price = float(current_price["price"])
    except Exception as e:
        current_price = 3489.34343
    if strategy == "AC":
        status = "NEW"
        first_grid = 0
        grid_int = 0
        average_m = float(request.form["average_m"])
        current_m = float(request.form["current_m"])
        trades = int(request.form["trades"])
    else:
        status = "RUNNING"
        average_m = 0
        current_m = 0
        trades = 0
        first_grid = float(request.form["first_grid"])
        grid_int = float(request.form["grid_int"])
    amount = float(request.form["amount"])
    sell_m = float(request.form["sell_m"])
    renew = 0
    time = t.time()
    my_form = {
        "user_id": user_id,
        "pairs": pairs,
        "strategy": strategy,
        "current_price": current_price,
        "first_grid": first_grid,
        "grid_int": grid_int,
        "average_margin": average_m,
        "current_margin": current_m,
        "amount": amount,
        "sell_margin": sell_m,
        "trades": trades,
        "renew": renew,
        "status": status,
        "time": time
    }

    #########################################################################
    ############ SEND DETAILS TO THE BACKEND TRADE TABLE ####################
    #########################################################################
    try:
        my_form = json.dumps(my_form)
        print(my_form)
        req = requests.post(f"{maxi_backend}new_trade", data=my_form)
        response = req.content
        response = response.decode("UTF-8")
        print(req.status_code)
        print(response)
        if req.status_code == 200 and response == "Success":
            flash(f"The bot is successfully scheduled to run ", "success")
            return redirect(url_for("dashboard"))
        else:
            flash(f"There was an error sending your trade", "danger")
            return redirect(url_for("dashboard"))
    except Exception as e:
        print(e)

@app.route("/stop_trade/<int:_id>")
@login_required
def stop_trade(_id):
    print(f"The entered trade id is {_id}")
    req = requests.patch(f"{maxi_backend}stop_trade/{_id}")
    response = req.content
    response = response.decode("UTF-8")
    print(f"The trade responsed with {response}")
    if req.status_code == 200 and response == "Success":
        flash("Trade was successfully stoped", "success")
    else:
        flash("There was an error stopping this trade", "danger")
    return redirect(url_for("dashboard"))

@app.route("/edit_trade/<int:_id>",  methods=["POST", "GET"])
def edit_trade(_id):
    req = requests.get(f"{maxi_backend}trade/{_id}")
    res = req.content
    trade = json.loads(res)
    user_req = requests.get(f"{maxi_backend}user/{session['user_id']}")
    user = user_req.content
    user = json.loads(user)

    if request.method == "POST":
        user_id = request.form["user_id"]
        trade_id = _id
        strategy = request.form["strategy"]
        amount = request.form["amount"]
        sell_m = request.form["sell_m"]
        time = t.time()
        if strategy == "Grid":
            first_grid = request.form["first_grid"]
            grid_int = request.form["grid_int"]
            my_data = {"user_id": user_id, "trade_id": trade_id, "first_grid": first_grid, "grid_int": grid_int, "amount": amount, "sell_margin": sell_m, "time": time}
        else:
            average_m = request.form["average_m"]
            current_m = request.form["current_m"]
            trades = request.form["trades"]
            my_data = {"user_id": user_id, "trade_id": trade_id, "average_margin": average_m, "current_margin": current_m, "trades": trades, "amount": amount, "sell_margin": sell_m, "time": time}
        my_data = json.dumps(my_data)    
        req = requests.patch(f"{maxi_backend}update_trade/{_id}", data=my_data)
        res = req.content
        res = res.decode("UTF-8")
        if res == "Success":
            flash(f"Trade with id {_id} successfully updated", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Error updating trade", "danger")
    return render_template("update.html", trade=trade, user= user,balance=get_asset_balance)

if __name__ == "__main__":
    login_manager.init_app(app)
    app.run(debug=True, port=8080)
