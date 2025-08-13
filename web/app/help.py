from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)

@app.route("/")
def home():
    return redirect(url_for("home_"))

@app.route("/home")
def home_():
    return render_template("home.html")

@app.route("/help")
def unable_to_access():
    return render_template("unable_to_access.html")

@app.route("/download")
def download():
    return render_template("download.html")

@app.route("/download_request", methods=["POST"])
def download_request():
    # You can log, process, or handle the request here
    # For now, just redirect to download page
    return redirect(url_for("download"))

@app.route("/unable_request", methods=["POST"])
def unable_request():
    # You can log, process, or handle the request here
    # For now, just redirect to unable_to_access page
    return redirect(url_for("unable_to_access"))

if __name__ == "__main__":
    app.run(debug=True)