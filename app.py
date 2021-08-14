from flask import Flask, flash, render_template, request, redirect, url_for, session, logging, session
# import db
import time as t
import os
import json
import requests
from requests.exceptions import ConnectionError
from multiprocessing import Process
from passlib.hash import sha256_crypt
from auth import RegisterForm, LoginForm
from functools import wraps
from functions import get_asset_balance, get_order
from binance.client import Client
app = Flask(__name__)

# Access the CLODUAMQP_URL environment variable and parse it (fallback to localhost)
broker_url = os.environ.get(
    'CLOUDAMQP_URL', "amqps://wrombhgt:zZyzwmcqhoPenQ_-AmdZQoCmWYM9EDFJ@toad.rmq.cloudamqp.com/wrombhgt")
broker_pool_limit = 1  # Will decrease connection usage
broker_heartbeat = None  # We're using TCP keep-alive instead
# May require a long timeout due to Linux DNS timeouts etc
broker_connection_timeout = 30
# AMQP is not recommended as result backend as it creates thousands of queues
result_backend = None
# Will delete all celeryev. queues without consumers after 1 minute.
event_queue_expires = 240
# Disable prefetching, it's causes problems and doesn't help performance
worker_prefetch_multiplier = 1
worker_concurrency = 10


app.secret_key = 'maxitest'
app.config['SESSION_TYPE'] = 'filesystem'
# app.config['CELERY_RESULT_BACKEND'] = 'db+mysql://admin:maxitest@maxitest.cepigw2nhp7p.us-east-2.rds.amazonaws.com/MaxiBot'
# app.config['CELERY_BROKER_URL'] = broker_url
maxi_backend = os.environ.get(
    "MAXIBOT_BACKEND", "https://maxibot-backend.herokuapp.com/api/v1/")

# app.config["CELERYBEAT_SCHEDULE"] = {
#     'add-every-30-seconds': {
#         'task': 'tasks.my_test.my_task',
#         'schedule': timedelta(seconds=5),
#         'args': ("woooooooo"),
#         "maxinterval": 2
#     },
# }

@app.route("/")
def index():
    return render_template("home.html")

@app.route("/register", methods=["POST", "GET"])
def register():
    form = RegisterForm(request.form)
    if request.method == "POST" and form.validate():
        name = form.name.data
        email = form.email.data
        phone = form.phone.data
        api_key = form.api_key.data
        secret_key = form.secret_key.data
        password = sha256_crypt.hash(form.password.data)
        status = "Activated"
        my_form = {"name": name, "email": email, "phone": phone,
                   "api_key": api_key, "secret_key": secret_key, "password": password, "status": status}
        my_form = json.dumps(my_form)
        print(my_form)
        try:
            req = requests.post(
                f"{maxi_backend}register", data=my_form)
            print(req.status_code)
            response = req.content
            response = response.decode("UTF-8")
            print(response)
            if req.status_code == 200 and response == "Success":
                flash("You were successfully registered kindly login", "success")
                return redirect(url_for("login"))
            elif req.status_code == 503:
                flash("Server is currently down")
                return render_template("register.html", form=form)
            elif response == "Email Error":
                flash("Email Already in use kindly use another email", "warning")
            elif response == "API Error":
                flash("Your API key already exist kindly use another one", "danger")
            return render_template("register.html", form=form)
        except ConnectionError as e:
            print(e)
            flash("There is an issue with the server try lager", "warning")
            return render_template("register.html", form=form)
        except Exception as e:
            print(e)
            flash("Email address or Api key already exist", "warning")
            return render_template("register.html", form=form)
        # try:
        #     db.register(name, email, phone, api_key, secret_key, password)
        #     flash("You have successfully registered Login to continue", "success")
        #     return redirect(url_for("login"))
        # except db.mysql.Error as e:
        #     flash(
        #         "User Already Exist with this email click on Login or enter another email", "danger")
        #     print(e)
        #     return render_template("register.html", form=form)
    elif request.method == "POST" and not form.validate():
        flash("Please fill out all fields properly", "warning")
        return render_template("register.html", form=form)
    return render_template("register.html", form=form)


@app.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm(request.form)
    if request.method == "POST" and form.validate():
        # GET FORM DATA
        email = form.email.data
        password_candidate = form.password.data
        # print(email)
        # DATABASE QUERY
        try:
            req = requests.get(f"{maxi_backend}login", data=email)
        except ConnectionError as e:
            print("There was an error connecting to the server")
            flash("There is an issue with the server try again")
        else:
            response = req.content
            response = response.decode("UTF-8")
            print(req.status_code)
            if req.status_code == 200 and response != "No Email":
                user = response
                user = json.loads(user)
                password = user['password']
                if sha256_crypt.verify(password_candidate, password):
                    session["logged_in"] = True
                    user_id = user["id"]
                    session["user_id"] = user_id
                    print(f"Weclome User with id of {user_id}")
                    return redirect(url_for("dashboard"))
                else:
                    flash("Password is incorrect", "danger")
                    return render_template("login.html", form=form)
            elif response == "No Email":
                flash("No user found with this email kindly register", "warning")
            return render_template("login.html", form=form)
        # if user != None and user != "Connection Error":
        #     password = user["password"]
        #     # Compare Password
        #     if sha256_crypt.verify(password_candidate, password):
        #         session["logged_in"] = True
        #         session["user"] = user
        #         return redirect(url_for("dashboard"))
        #     else:
        #         flash("Password is incorrect", "danger")
        #         return render_template("login.html", form=form)
        # elif user == "Connection Error":
        #     flash("No internet Connection check your network and try again")
        #     return render_template("login.html", form=form)
        # else:
        #     flash("No user exist with this email kindly register", "warning")
        #     return render_template("login.html", form=form)
    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    session.clear()
    flash("Successfuly Logout out", "success")
    return redirect(url_for("login"))


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/dashboard")
@app.route("/dashboard/<int:page_num>")
@login_required
def dashboard(page_num=1):
    #############################################
    ############ GET USER DETAILS ###############
    #############################################
    try:
        user_req = requests.get(f"{maxi_backend}user/{session['user_id']}")
        user = user_req.content
        user = user.decode("UTF-8")
        user = json.loads(user)
        print(user_req.status_code)
        data = [session["user_id"],page_num]
        data = json.dumps(data)
        trade_req = requests.get(f"{maxi_backend}my_trades", data=data)
        print(f"the trade request return a status of {trade_req.status_code}")
        trades_res = trade_req.content
        trades_res = trades_res.decode("UTF-8")
        data = json.loads(trades_res)
        trades = data[0]
        page_iter = data[1]
    except Exception as e:
        print(f"There was an error {e}")
        flash("There is an error in the application just give us some time to fix it", "danger")
        redirect(url_for("login"))
    else:
        return render_template("index.html",user= user, trades=trades, page_iter = page_iter, round=round, float=float, balance=get_asset_balance)

@app.route("/new_trade", methods=["POST"])
@login_required
def new_trade():
    user_id = session["user_id"]
    pairs = request.form["pairs"]
    strategy = request.form["strategy"]
    print(user_id, pairs, strategy)
    my_pair = pairs.split("/")
    first_symbol = my_pair[0]
    second_symbol = my_pair[1]
    my_pair = f"{first_symbol}{second_symbol}"
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
    app.run(debug=True)
