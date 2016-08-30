import json


from jinja2 import StrictUndefined
from flask import Flask, render_template, request, flash, redirect, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
import praw

from model import connect_to_db, db, User, Category, UserCategory, categories
from reddit import r,get_authorize_reddit_link
from main_program import get_news, get_declared_interests, personalize_name
from headlines import get_headlines
app = Flask(__name__)
app.secret_key = "ABC"

app.jinja_env.undefined = StrictUndefined


@app.route('/')
def homepage():
    """ home page, going to ask pass in secret key and code to reddit in order to get OAuth code to use in authorized"""

  
    # if session.get('user_id'):
    #     # check if logged into Reddit
    #     try:
    #         user = r.get_me()
    #         return render_template("homepage.html")
    #     except praw.errors.OAuthScopeRequired:
    #         url_for_api = get_authorize_reddit_link()
    #         return redirect(url_for_api)
    # else:
    return render_template('homepage.html')


@app.route('/authorize_callback')
def get_authorized():
    """actually get into the api after getting the callback information"""


    state = request.args.get('state', '')
    code = request.args.get('code', '')
    info = r.get_access_information(code)
    return redirect('/')
    

@app.route('/news_quote')
def print_news_quote():
    """ Prints a random quote about the news"""


    return get_news_quote()


@app.route('/see-news')
def get_news_page():
    """display the news according to the users interests"""


    if session.get('user_id'):
        dictionary_to_unpack_in_html = get_news()
        return render_template("thenews.html",dictionary_to_unpack_in_html=dictionary_to_unpack_in_html)
    else:
        flash("Please login if you're a member or register to become a member to see your news")
        return redirect('/')


@app.route('/register_form')
def get_form_to_fill_in():
    """display the registration form to fill in"""


    return render_template("register_form.html")


@app.route('/register_form', methods=['POST'])
def get_registration_info():
    """Process registration"""


    firstname = request.form.get("firstname")
    lastname = request.form.get("lastname")
    email = request.form.get("email")
    password = request.form.get("password")
    flash("Welcome %s %s. Please check the categories you're interested in." % (firstname,lastname))
    #instantiate a user in the User database.
    new_user = User.instantiate_user(firstname,lastname,email,password)
    session['user_id'] = new_user.user_id 
    
    return redirect('/declare_interests')

 
@app.route("/declare_interests")
def user_interests_form():
    """ present a list of interests that the user can check. Displayes interests checked before"""
    user_id = session['user_id']

    category_names = categories.keys()
    category_names.sort()
    print category_names
    category_list = get_declared_interests(user_id)


    return render_template("declare_interests.html",
                           category_names=category_names,
                           category_list=category_list,
                           )


@app.route("/declare_interests" , methods=['POST'])
def register_interests():
    """"Get the user's interests and put them in the UserCategory Table"""
   

    if db.session.query(UserCategory):
        db.session.query(UserCategory).filter_by(user_id=user_id).delete()
        db.session.commit()

    interests = request.form.getlist("interest_change")
    interest_list = []
    #look up the category id on every category(interest) chosen to put in the association table
    for interest in interests:
        interest_add_on = db.session.query(Category.category_id).filter_by(category_name=interest).first()
        interest_list.append(interest_add_on[0])

    UserCategory.instantiate_usercategory(user_id,interest_list)
    
    return redirect("/")


@app.route("/login")
def login():
    """Log in Form"""


    return render_template("login.html")


@app.route('/login',methods=['POST'])
def login_process():
    """ Process login."""


    email = request.form.get('email')
    password = request.form.get('password')
    user = User.query.filter_by(email=email).first()

    if not user:
        flash ("Please Register First")
        return render_template('homepage.html')
    if user.password != password:
        flash('Incorrect Password. Please try again.')
        return redirect('/login')

    session['user_id'] = user.user_id
    session['user_name'] = personalize_name(user.user_id)
    flash('Logged in')
   
    return redirect('/')



@app.route('/news/<newssource>') 
def show_bbc_hl(newssource):
    """ to get the Headline news from BBC,CNN,API,Google or New York Times"""


    bbc_dict = get_headlines(newssource)
    if newssource == 'bbc-news':
        headline_string = "BBC Headline News"
    elif newssource == 'bloomberg':
        headline_string = "Bloomberg Headline News"
    elif newssource == 'cnn':
        headline_string = "CNN Headline News"
    elif newssource == 'associated-press':
        headline_string = 'Associated Press Headline News'
    elif newssource =='google-news':
        headline_string = "Google Headline News"
   
    url = bbc_dict['url']
    title = bbc_dict['title']
    description = bbc_dict['description']

    return render_template("headlines.html",headline_string=headline_string,url=url,title=title,description=description)
    

@app.route('/logout')
def logout():
    """Log out."""

    del session['user_id']
    del session['user_name']
    flash('Logged out. Please log in to see your news')
    # return render_template('homepage.html',user_name="My")
    return redirect('/')


@app.route("/important")
def important():
    """Important info for logged in users."""
    if "user_id" in session:
        return render_template("important.html")

    else:
        flash("You must be logged in to view the important page")
        return redirect("/login")


if __name__ == '__main__':
    app.debug = True
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    connect_to_db(app) 
    DebugToolbarExtension(app)
    app.run(debug=True, host="0.0.0.0", port=65010)




