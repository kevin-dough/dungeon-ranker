from flask import Flask, redirect, url_for, render_template, request, flash

app = Flask(__name__)

#routes

#home route
@app.route("/home")
@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)