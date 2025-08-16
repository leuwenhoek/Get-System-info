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
    return redirect(url_for("download"))

@app.route("/unable_request", methods=["POST"])
def unable_request():
    return redirect(url_for("unable_to_access"))

@app.route("/report")
def report_page():
    return render_template("report.html")

@app.route("/report", methods=["POST"])
def report():
    return redirect(url_for("report_page"))

@app.route("/about",methods=["POST","GET"])
def about():
    return render_template("about.html")

@app.route("/about_dev",methods=["POST","GET"])
def about_dev():
    return render_template("about_dev.html")
if __name__ == "__main__":
    app.run(debug=True)