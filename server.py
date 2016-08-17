from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
import json
from model import connect_to_db, db, User, Category, UserCategory
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
    return render_template("homepage.html")


@app.route('/see-news')
def get_news_page():
    """display the news according to the users interests"""

    
    user_id = session['user_id']
    category_id_list = []
    # get list of user's chosen categories
    object_list_by_userid =UserCategory.query.filter_by(user_id=user_id).all()
    for object in object_list_by_userid:
        category = object.category_id
        category_id_list.append(category)
    category_list = []
    for category in category_id_list:
        #converting the category_id into the category name.
        category_to_query =db.session.query(Category.category).filter_by(category_id=category).first()
        #need to call the first element of every tuple at index 0.
        category_to_query=category_to_query[0]
        category_list.append(category_to_query)
    # print category_list
    dictionary_to_unpack_in_html = {}
    for category in category_list:
        subreddit_dict = get_subreddits_by_interest(category)
        # make an ordered list of titles and their associated url's
        titles=[]
        i = 0
        for item,posts in subreddit_dict.iteritems():
            title=posts['title']
            url=posts['url']
            i+=1
            titles.append((title, url))
        
        dictionary_to_unpack_in_html[category]=titles
    print dictionary_to_unpack_in_html
    
    return render_template("thenews.html",dictionary_to_unpack_in_html=dictionary_to_unpack_in_html)

@app.route('/register_form')
def get_form_to_fill_in():
    return render_template("register_form.html")


@app.route('/register_form', methods=['POST'])
def get_registration_info():
    """Process registration"""


    firstname = request.form["firstname"]
    lastname = request.form["lastname"]
    email = request.form["email"]
    password = request.form["password"]
    interests = request.form.getlist("interest")

    print firstname,lastname,email,password, str(interests)
    flash("Welcome %s %s. Now please login to see your news." % (firstname,lastname))

    #instantiate a user in the User database.
    instantiate_user(firstname,lastname,email,password)
    #using the user_id (gotten when instantiating a user) use that user_id to input into the association database)
    user_id = db.session.query(User.user_id).filter_by(email=email).first()
    #get the userid
    user_id = user_id[0]
    interest_list = []
    #look up teh category id on every category(interest) chosen to put in the association table
    for interest in interests:
        interest_add_on = db.session.query(Category.category_id).filter_by(category=interest).one()
        interest_list.append(interest_add_on[0])
    print interest_list
    #add instances to the association table
    instantiate_usercategory(user_id,interest_list)
    flash("User %s %s added." % (firstname,lastname))

    return render_template("login.html")

    
def instantiate_user(firstname,lastname,email,password):
    """Instantiate a user as a member"""


    new_user = User(firstname=firstname,
               lastname=lastname,
               email=email,
               password=password,
               )
    db.session.add(new_user)
    db.session.commit()
       

def instantiate_usercategory(user_id,interest_list):
    """"Make an association table for the member and their interests."""


    for interest in interest_list:
        association = UserCategory(user_id=user_id,category_id=interest)
        db.session.add(association)
    db.session.commit()


@app.route("/change_interests")
def get_form_change_interests():
    """take care of users who want to change what their interests are"""


    return render_template("change_interests.html")


@app.route("/change_interests" , methods=['POST'])
def change_interests():
    user_id = session['user_id']
    db.session.query(UserCategory).filter_by(user_id=user_id).delete()
    db.session.commit()
    interests = request.form.getlist("interest_change")
    interest_list = []
    #look up teh category id on every category(interest) chosen to put in the association table
    for interest in interests:
        interest_add_on = db.session.query(Category.category_id).filter_by(category=interest).one()
        interest_list.append(interest_add_on[0])
    instantiate_usercategory(user_id,interest_list)

    return render_template("homepage.html")


@app.route("/login")
def login():

    return render_template("login_form.html")


@app.route('/login',methods=['POST'])
def login_process():
    """ Process login."""
    email = request.form['email']
    password = request.form['password']

    user = User.query.filter_by(email=email).first()

    if not user:
        flash ("Please Register First")
        return render_template('homepage.html')

    if user.password != password:
        flash('Incorrect Password. Please try again.')
        return redirect('/login')

    session['user_id'] = user.user_id

    flash('Logged in')
    return render_template('homepage.html')

@app.route('/logout')
def logout():
    """Log out."""

    del session['user_id']
    flash('logged out')
    return render_template('homepage.html')


if __name__ == '__main__':
    app.debug = True

    connect_to_db(app)

    # # Use the DebugToolbar
    DebugToolbarExtension(app)
    
    app.run(debug=True, host="0.0.0.0", port=65010)




