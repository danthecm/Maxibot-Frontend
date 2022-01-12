from flask import Flask, render_template
import time as t
import os
import json
import requests

from binance.client import Client
from dotenv import load_dotenv
load_dotenv()



from users.views import users_blueprint
from platforms.views import platform_blueprint
from bots.views import bots_blueprint
from login import login_manager

app = Flask(__name__)
app.secret_key = 'maxitest'
app.config['SESSION_TYPE'] = 'filesystem'
app.jinja_env.add_extension('jinja2.ext.do')
login_manager.init_app(app)
maxi_backend = os.getenv("MAXIBOT_BACKEND")

app.register_blueprint(users_blueprint)
app.register_blueprint(platform_blueprint, url_prefix="/platform")
app.register_blueprint(bots_blueprint, url_prefix="/bots")

login_manager.login_view = "users.login"

@app.route("/")
def index():
    return render_template("home.html")

if __name__ == "__main__":
    app.run(debug=True, port=8080)
