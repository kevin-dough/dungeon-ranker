from flask import Flask, redirect, url_for, render_template, request
import aboutdata

app = Flask(__name__)

@app.route("/home")
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html", groupdatalist=aboutdata.groupdata())

@app.route("/testapi")
def testapi():
    return render_template("testapi.html")

if __name__ == "__main__":
    app.run(debug=True)