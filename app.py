from flask import Flask, render_template, request, redirect
import db
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("home.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/reg", methods=["POST", "GET"])
def reg():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        api_key = request.form["api_key"]
        secret_key = request.form["secret_key"]
        password = request.form["password"]

        try:
            db.register(name, email, int(phone), api_key, secret_key, password) 
            message = "You Have Successfully Registered Kindly Login"
            return render_template("home.html", message = message)
        except db.mysql.Error as e:
            message = "You've have already Registered with this email kindly proceed to Login"
            print(e)
            return render_template("register.html", message=message)    

    else:
        message = "Hello there"
        return render_template("register.html", message= message)

if __name__ == "__main__":
    app.run(debug=True)