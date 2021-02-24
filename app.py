from flask import Flask, render_template, request

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
        return f"This is a post request name {name} email {email} phone {phone} API KEY {api_key} SECRET key {secret_key} Password {password} "
    else:
        return "Opss you made a get request"

if __name__ == "__main__":
    app.run(debug=True)