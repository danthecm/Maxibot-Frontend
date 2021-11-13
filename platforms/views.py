from flask import Blueprint, redirect, url_for, render_template, request, flash, session, abort
import requests, os
import time as t

from flask_login import login_required, current_user

from requests.exceptions import ConnectionError
from platforms.forms import PlatformForm
from binance.client import Client
from binance.exceptions import BinanceAPIException


maxi_backend = os.environ.get(
    "MAXIBOT_BACKEND", "http://127.0.0.1:5000")
platform_blueprint = Blueprint("platforms", __name__, template_folder="templates", static_folder="static")


@platform_blueprint.route("/add", methods=["GET", "POST"])
@login_required
def add():
    form = PlatformForm(request.form)
    if request.method == "POST" and form.validate():
        name = request.form["name"]
        api_key = request.form["api_key"]
        secret_key = request.form["secret_key"]
        passphrase = request.form["passphrase"]
        print(name, api_key, secret_key, passphrase)
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {session['access_token']}"}
        if name == "Binance":
            try:
                client = Client(api_key, secret_key)
                info = client.get_account()
            except BinanceAPIException as e:
                flash(f"Invalid credentials for {name}", "danger")
                return redirect(url_for("platforms.add"))
            except ConnectionError:
                flash(f"could not connect to {name} Check your internet connection", "warning")
                return redirect(url_for("platforms.add"))
        elif name == "Coinbase Pro":
            url = "https://api.exchange.coinbase.com/accounts"
            
            headers = { 
                        "Accept": "application/json",
                        "cb-access-key": api_key,
                        "cb-access-passphrase": passphrase,
                        "cb-access-sign": secret_key,
                        "cb-access-timestamp": f"{t.time()}"
                        }

            response = requests.request("GET", url, headers=headers)
            message = response.json()
            if message["message"] == "Invalid API Key":
                flash(f"Invalid credentials for {name}", "danger")
                return redirect(url_for("platforms.add"))
        new_platform = {"user_id": session["user_id"], "name": name, "api_key": api_key, "secret_key": secret_key, "passphrase": passphrase}
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {session['access_token']}"}
        # new_platform = json.dump(new_platform)
        req = requests.post(f"{maxi_backend}/new_platform", json=new_platform, headers=headers)
        if req.status_code == 201:
            flash("Platform successfully registered")
            session["platform"] = current_user.platforms[0]
            return redirect(url_for("users.dashboard"))
        else:
            flash(f"There was an error registering platform {req.text}")
            return redirect(url_for("platforms.add"))

    return render_template("add.html", form=form)



@platform_blueprint.route("/switch/<string:name>")
@login_required
def switch(name):
    name = name
    all_platforms = current_user.platforms
    for platform in all_platforms:
        if platform["name"] == name:
            session["platform"] = platform
            print(platform)
    print(name)
    return redirect(url_for("users.dashboard"))

@platform_blueprint.route("/test")
@login_required
def test():
    
    url = "https://api.exchange.coinbase.com/accounts"

    headers = {
                "Accept": "application/json",
                "cb-access-key": current_user.access_token,
                "cb-access-passphrase": current_user.passphrase,
                "cb-access-sign": current_user.secret_key,
                "cb-access-timestamp": t.time()
            }

    response = requests.get(url, headers=headers)
    print(response.text)
    print(response.json())

    print(response.text)