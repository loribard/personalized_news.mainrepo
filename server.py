from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Subreddit
# import praw
# import os
from reddit import r,get_authorize_reddit_link, authorized, get_subreddits_by_interest

app = Flask(__name__)
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def homepage():
    """ home page, going to ask pass in secret key and code to reddit in order to get OAuth code to use in authorized"""


    return "<a href='%s' >Click here </a>to start" % get_authorize_reddit_link()
   


@app.route('/authorize_callback')
def get_authorized():
    """actually get into the api after getting the callback information"""

    actual_link = authorized()  
    subreddit_dict = get_subreddits_by_interest('funny') 

    return render_template("base.html")



@app.route("/login")
def login():
    return render_template("login_form.html")
# @app.route('/register', methods=['POST'])
# def register_process():
#     """Process registration."""

#     # Get form variables
#     email = request.form["email"]
#     password = request.form["password"]
#     age = int(request.form["age"])
#     zipcode = request.form["zipcode"]

#     new_user = User(email=email, password=password, age=age, zipcode=zipcode)

#     db.session.add(new_user)
#     db.session.commit()

#     flash("User %s added." % email)
#     return redirect("/")

if __name__ == '__main__':
    # app.debug = True

    # connect_to_db(app)

    # # Use the DebugToolbar
    # DebugToolbarExtension(app)
    # r = praw.Reddit('Test of Reddit API ')
    # r.set_oauth_app_info(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)
    
    app.run(debug=True, host="0.0.0.0", port=65010)




