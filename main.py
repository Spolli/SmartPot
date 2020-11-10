#!/usr/bin/env python3
from flask import Flask, render_template, redirect, url_for

app = Flask(__name__, static_url_path='',
            static_folder='webpage/static',
            template_folder='webpage/templates')

app.config["DEBUG"] = True

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/<name>")
def user(name):
    return f"Hello-- {name}!"

@app.route("/admin")
def admin():
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(host="localhost", port=8000, debug=True)