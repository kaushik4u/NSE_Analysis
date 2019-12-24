from flask import Flask, render_template, request, redirect, url_for
import sqlite3

# Opens file if exists, else creates file
connex = sqlite3.connect("./data/nse_data.db")
# This object lets us actually send messages to our DB and receive results
cur = connex.cursor()

@app.route("/")
def index():
   return render_template("index.html")
