from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/help")
def unable_to_access():
    return render_template("unable_to_access.html")

if __name__ == "__main__":
    app.run(debug=True)