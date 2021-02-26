from flask import Flask, render_template, request, redirect, url_for, session, logging, session
import db
from passlib.hash import sha256_crypt
from auth import RegisterForm, LoginForm
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
        password = sha256_crypt.encrypt(form.password.data)
        try:
            db.register(name, email, phone, api_key, secret_key, password)
            message = "You Have Successfully Registered Kindly Login"
            return render_template("home.html", message=message)
        except db.mysql.Error as e:
            message = "You've have already Registered with this email kindly proceed to Login"
            print(e)
            return render_template("register.html", message=message, form=form)
    elif request.method == "POST" and not form.validate():
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
        try:
            user = db.login(email)
        except:
            message = "No active internet connection try again"
            return render_template("login.html", form=form, error=message)
        if user:
            password = user["password"]
            # Compare Password
            if sha256_crypt.verify(password_candidate, password):

                session["logged_in"] = True
                session["user"] = user
                app.logger.info("PASSWORD MATCHED")
                return redirect(url_for("dashboard"))
            else:
                error = "Password is incorrect"
                return render_template("login.html", form=form, error=error)
        else:
            error = "No user exist kindly register"
            return render_template("login.html", form=form, error=error)
    return render_template("login.html", form=form)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")

if __name__ == "__main__":
    app.run(debug=True)
