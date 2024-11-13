import os
import requests
import urllib.parse

from flask import redirect, render_template, request, session
from functools import wraps


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                        ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function



##################################################################
def send_plot(coin,procent,flag, myprice):
    pl(coin,procent,flag, myprice)

    bot_token = '6460907609:AAH0ZCfogSLjFUc0aVnS8ZO9McP7OF8DLek'
    chat_id = "6346385312"
    
    file = "graph.png"

    files = {
        'photo': open(file, 'rb')
    }

    message = ('https://api.telegram.org/bot'+ bot_token + '/sendPhoto?chat_id=' 
            + chat_id)
    send = requests.post(message, files = files)
    
    
def send_text(text):
    tok = "6460907609:AAH0ZCfogSLjFUc0aVnS8ZO9McP7OF8DLek" #@Saponjyan_Bot
    my_id = "6346385312"  
    url_req = "https://api.telegram.org/bot" + tok + "/sendMessage" + "?chat_id=" + my_id + "&text=" + text
    results = requests.get(url_req)