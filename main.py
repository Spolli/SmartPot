#!/usr/bin/env python3
from flask import Flask, render_template, redirect, url_for

app = Flask(__name__, static_url_path='',
            static_folder='webpage/static',
            template_folder='webpage/templates')

app.config["DEBUG"] = True

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

if __name__ == "__main__":
    app.run(host="localhost", port=8001, debug=True)