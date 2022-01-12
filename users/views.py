from flask import Blueprint, redirect, url_for, render_template, request, flash, session, abort

from flask_paginate import Pagination, get_page_parameter
from flask_login import login_required, login_user, logout_user, current_user
from requests import api
from werkzeug.datastructures import Authorization
from login import login_manager

from functions import is_safe_url, get_asset_balance, get_balance_coinbase, get_kraken_balance
import requests, os
from krakenex import API

from requests.exceptions import ConnectionError
from requests.auth import AuthBase
from users.forms import RegisterForm, LoginForm
from users.models import User

users_blueprint = Blueprint("users", __name__, template_folder="templates")

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

maxi_backend = os.getenv(
    "MAXIBOT_BACKEND", "http://132.226.211.117")

@users_blueprint.route("/register", methods=["POST", "GET"])
def register():
    form = RegisterForm(request.form)
    if request.method == "POST" and form.validate():
        name = form.name.data
        email = form.email.data
        phone = form.phone.data
        password = form.password.data
        status = "Activated"
        my_form = {"name": name, "email": email, "phone": phone, "password": password, "status": status}
        try:
            req = requests.post(
                f"{maxi_backend}/register", json=my_form, headers={"Content-Type": "application/json"})
            response = req.json()
            if req.status_code == 201:
                flash("You were successfully registered kindly login", "success")
                return redirect(url_for("users.login"))
            elif req.status_code == 503:
                flash("Server is currently down")
                return render_template("register.html", form=form)
            elif req.status_code == 400 or req.status_code == 404:
                message = response["message"]
                flash(message, "warning")
                return render_template("register.html", form=form)
            return render_template("register.html", form=form)
        except ConnectionError as e:
            print(e)
            flash("There is an issue with the server try later", "warning")
            return render_template("register.html", form=form)
        except Exception as e:
            print(e)
            flash("Email address or Api key already exist", "warning")
            return render_template("register.html", form=form)
    elif request.method == "POST" and not form.validate():
        flash("Please fill out all fields properly", "warning")
        return render_template("register.html", form=form)
    return render_template("register.html", form=form)


@users_blueprint.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm(request.form)
    next = request.args.get('next')
    if request.method == "POST" and form.validate():
        # GET FORM DATA
        email = form.email.data
        password_candidate = form.password.data
        # DATABASE QUERY
        try:
            req = requests.post(f"{maxi_backend}/login", json={"email": email, "password": password_candidate}, headers={"Content-Type": "application/json"})
        except ConnectionError as e:
            flash("There is an issue with the server try again", "warning")
        else:
            response = req.json()
            if req.status_code == 200:
                user_id = response["id"]
                access_token = response["access_token"]
                refresh_token = response["refresh_token"]
                session["logged_in"] = True
                session["user_id"] = user_id
                session["access_token"] = access_token
                session["refresh_token"] = refresh_token
                headers = {"Content-Type": "application/json", "Authorization": f"Bearer {access_token}"}
                user_req = requests.get(f"{maxi_backend}/user/{user_id}", headers=headers)
                response = user_req.json()
                user = User(**response)
                user.access_token = access_token
                user.refresh_token = refresh_token
                login_user(user)
                if len(response["platforms"]) < 1:
                    return redirect(next or url_for("platforms.add"))
                else:
                    session["platform"] = current_user.platforms[0]
                if not is_safe_url(next):
                    return abort(400)
                return redirect(url_for("users.dashboard"))
            elif req.status_code >= 400:
                flash(response["message"], "warning")
            return redirect(next or url_for("users.login"))
    return render_template("login.html", form=form)


@users_blueprint.route("/logout")
def logout():
    user = current_user
    user.authenticated = False
    session.clear()
    logout_user()
    flash("Successfuly Logout out", "success")
    return redirect(url_for("users.login"))


@users_blueprint.route("/dashboard")
@users_blueprint.route("/dashboard/<int:num>")
@login_required
def dashboard(num=1):
    #############################################
    ############ GET USER DETAILS ###############
    #############################################
    search = False
    q = request.args.get('q')
    if q:
        search = True

    page = num
    
    try:
        # pagination.active = response["active"]
        # print(pagination.pages)
        
        symbols = []
        platform = session["platform"]
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {current_user.access_token}"}
        plat_req = requests.get(f"{maxi_backend}/platform/{platform['id']}", headers=headers)
        response = plat_req.json()
        current_user.active_platform = response
        session["platform"] = current_user.active_platform
        bots = current_user.active_platform["bots"]
        active_bot = list(filter(lambda x:x["status"] == "RUNNING", bots))
        paused_bot = list(filter(lambda x:x["status"] == "PAUSED", bots))
        stopped_bots = list(filter(lambda x: x["status"] == "STOPPED", bots))
        error_bots = list(filter(lambda x: x["status"] == "ERROR APIError(code=-2010): Account has insufficient balance for requested action.", bots))
        pagination = Pagination(page=page, per_page=5, total=len(bots), search=search, record_name='bots')
        my_bots = []
        def append_list(name, lists):
            for list in lists:
                for item in list:
                    name.append(item)
        append_list(my_bots,[active_bot,paused_bot,stopped_bots, error_bots])
        my_bots = my_bots[(pagination.per_page * (num - 1)):(pagination.per_page * num)]
        pagination.active = len(active_bot)
        pagination.paused = len(paused_bot)
        # print(platform["bots"])
        if platform["name"] == "Coinbase Pro":
            from cbpro import AuthenticatedClient
            api_key = platform.get("api_key")
            secret_key = platform.get("secret_key")
            passphrase = platform.get("passphrase")
            client = AuthenticatedClient(api_key, secret_key, passphrase)
            all_products = client.get_products()
            symbols = [product['id'] for product in all_products]
            symbols = list(filter(lambda x: "GBP" in x or "USD" in x or "EUR" in x, symbols))
            symbols.sort()
            # print(symbols)
        elif platform["name"] == "Binance":
            #####################################################
            ############ GET ALL COINS FROM BINANCE #############
            #####################################################
            from binance import Client
            client = Client(platform.get("api_key"), platform.get("secret_key"))
            sym_req = requests.get("https://api.binance.com/api/v1/exchangeInfo")
            response = sym_req.json()
            symbols = response["symbols"]
            symbols = [x["symbol"] for x in symbols]
            symbols = list(filter(lambda x: "GBP" in x or "USDT" in x or "EUR" in x, symbols))
            symbols.sort()
        
        elif platform["name"] == "Kraken":
            client = API(platform.get("api_key"), platform.get("secret_key"))
            symbols = client.query_public("AssetPairs")
            symbols = list(symbols.get("result").keys())
            symbols = list(filter(lambda x: "GBP" in x or "USD" in x or "EUR" in x, symbols))
            symbols.sort()

        else:
            symbols = []


    except Exception as e:
        print(f"There was an error {e}")
        # flash("There is an error in the application just give us some time to fix it", "danger")
        return abort(500)
    else:
        return render_template("index.html", client=client, coinbase_balance=get_balance_coinbase, binance_balance=get_asset_balance, kraken_balance=get_kraken_balance, symbols=symbols, pagination=pagination, my_bots=my_bots)
    # return render_template("index.html",user= user, trades=trades, page_iter = page_iter, round=round, float=float, balance=get_asset_balance, symbols=symbols, pagination=pagination)
        # return render_template("index.html", balance= get_asset_balance, trades=trades,round=round, float=float, pagination=pagination, symbols=symbols)