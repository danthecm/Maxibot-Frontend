from flask import Flask, flash, render_template, request, redirect, url_for, session, logging, session
import db
from passlib.hash import sha256_crypt
from auth import RegisterForm, LoginForm
from av import get_average
from average import Current as A
from functools import wraps 

app = Flask(__name__)

app.secret_key = 'maxitest'
app.config['SESSION_TYPE'] = 'filesystem'

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
        try:
            db.register(name, email, phone, api_key, secret_key, password)
            flash("You have successfully registered Login to continue", "success")
            return redirect(url_for("login"))
        except db.mysql.Error as e:
            flash("User Already Exist with this email click on Login or enter another email", "danger")
            print(e)
            return render_template("register.html", form=form)
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

        # DATABASE QUERY
        user = db.login(email)
        if user:
            password = user["password"]
            # Compare Password
            if sha256_crypt.verify(password_candidate, password):
                session["logged_in"] = True
                session["user"] = user
                print("PASSWORD MATCHED")
                return redirect(url_for("dashboard"))
            else:
                flash("Password is incorrect", "danger")
                return render_template("login.html", form=form)
        else:
            flash("No user exist with this email kindly register", "warning")
            return render_template("login.html", form=form)
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


@app.route("/dashboard", method=["POST", "GET"])
@login_required
def dashboard():
     if request.method == "POST" and form.validate():
         api_key = request.form["api_key"]
        secret_key = request.form["secret_key"]
        product = request.form["product"]
        margin_p = float(request.form["margin_p"])
        sell_p = float(request.form["sell_p"])
        trades = int(request.form["trades"])
        users = {"api_key": api_key, "secret_key": secret_key, "product": product,
                 "margin_p": margin_p, "sell_p": sell_p, "trades": trades}
        checker = True
        return render_template("dashboard.html", checker= checker, users = users, current= A)
    return render_template("dashboard.html", av=get_average)



if __name__ == "__main__":
    app.run(debug=True)
