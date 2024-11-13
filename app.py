'''cs50
Flask
Flask-Session
requests
numpy
pandas
binance-futures-connector
binance-connector
python passenger_wsgi.py
Enter to the virtual environment.To enter to virtual environment, run the command:
source /home/deddvywa/virtualenv/saponjyan/3.10/bin/activate && cd /home/deddvywa/saponjyan
'''


'''
…or create a new repository on the command line
echo "# spj2" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/Saponjyan/spj2.git
git push -u origin main

…or push an existing repository from the command line
git remote add origin https://github.com/Saponjyan/spj2.git
git branch -M main
git push -u origin main

'''
import os
from img import img
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify, send_file
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required
from datetime import datetime

import json
#####################################################################################
# для фонового бота
import logging
from logging.handlers import RotatingFileHandler
log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
log_file = 'app.log'
logger = logging.getLogger()
logger.setLevel(logging.INFO)
file_handler = RotatingFileHandler(log_file, maxBytes=1024*1024*10, backupCount=5)
file_handler.setFormatter(log_formatter)
logger.addHandler(file_handler)
logger.propagate = False

##########################################################################################
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
db = SQL("sqlite:///mydb.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    return redirect("/ai")

@app.route("/ai", methods=["GET", "POST"])
def ai():
    """AI"""
    if request.method == "POST":
        prompt = request.cookies['prompt']#request.form.get("prompt")
        img(prompt)
        chat_id = request.form.get("Telegram id")
        use = str(datetime.now())# datetime.
        # db.execute(f"INSERT INTO prompts VALUES('{use}','{prompt}','status','{chat_id}')")
        return send_file('img.png', mimetype='image/jpeg') #'picture1.png'
        # return render_template("ai.html",prompt=f"your prompt is {prompt} chat id is {chat_id}")
    else:
        return render_template("ai.html")



# @app.route("/aicolab", methods=["GET", "POST"])
# def aicolab():
#     """AIcolab"""
#     if request.method == "POST":
        
#         return render_template("ai.html",prompt=prompt)
#     else:          
#         prompt = db.execute(f"SELECT * FROM prompts WHERE status = 'status'")[0]
#         db.execute(f"UPDATE prompts SET status = 'done' WHERE  user_id = '{prompt['user_id']}' ")
#         response =  {"resp" : prompt} 
#         return jsonify(response)
#         # return send_file('picture1.png', mimetype='image/jpeg')


@app.route("/sorry", methods=["GET", "POST"])
def sorry():
    """sorry"""
    if request.method == "POST":
        return render_template("sorry.html")
    else:
        return render_template("sorry.html")

if __name__ == '__main__':
    app.run(debug=True)

