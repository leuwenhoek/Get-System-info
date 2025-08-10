from flask import Flask
from flask import render_template,redirect,url_for

app = Flask(__name__)

@app.route("/")
def home():
    return redirect(url_for("unable_to_access"))

@app.route("/help")
def unable_to_access():
    return render_template("unable_to_access.html")

if __name__ == "__main__":
    app.run(debug=True)