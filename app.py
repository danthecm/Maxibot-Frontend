from flask import Flask, render_template, request, redirect, url_for, session, logging
import db
from wtforms import Form, StringField, PasswordField, IntegerField
from wtforms import validators as v
from passlib.hash import sha256_crypt
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("home.html")


class RegisterForm(Form):
    name = StringField(
        'Full Name', 
        validators=[v.input_required(), v.length(min=8, message="Length must be at least %(min)d characters long")
        ])
    email = StringField(
        'Email', 
        validators=[v.email(), v.input_required()]
        )
    phone = IntegerField(
        "Phone", 
        validators=[v.input_required()]
        )
    api_key = StringField(
        "API Key", 
        validators=[v.input_required(), v.length(min=15, message="Length must be at least %(min)d characters long")]
        )
    secret_key = StringField(
        "SECRET Key", 
        validators=[v.input_required(), v.length(min=15, message="Length must be at least %(min)d characters long")]
        )
    password = PasswordField(
        'Password', 
        validators=[v.data_required(), v.equal_to('confirm', message='Passwords must match'), v.length(min=8, message="Length must be at least %(min)d characters long")]
        )
    confirm = PasswordField(
        'Confirm Password', validators=[v.input_required()])


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


if __name__ == "__main__":
    app.run(debug=True)
