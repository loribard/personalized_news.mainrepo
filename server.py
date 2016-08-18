import json


from jinja2 import StrictUndefined
from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Category, UserCategory, categories
from reddit import r,get_authorize_reddit_link, authorized, get_subreddits_by_interest

app = Flask(__name__)
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def homepage():
    """ home page, going to ask pass in secret key and code to reddit in order to get OAuth code to use in authorized"""

    # if logged_in:
    #    return render_template("homepage.html")
    # else :
    
    reddit_auth_url = get_authorize_reddit_link()
    return redirect(reddit_auth_url)
    
@app.route('/authorize_callback')
def get_authorized():
    """actually get into the api after getting the callback information"""


    state = request.args.get('state', '')
    code = request.args.get('code', '')
    authorized(state, code)
    return render_template("homepage.html")


@app.route('/see-news')
def get_news_page():
    """display the news according to the users interests"""

    user_id = session['user_id']
    users_w_categories_obj = UserCategory.query.filter_by(user_id=user_id).all()
    category_id_list = []
    for user in users_w_categories_obj:
        category_id_list.append(user.category_id)
    dictionary_to_unpack_in_html = {}
    subreddit_to_query=[]
    for category_id in category_id_list:
        subreddit_obj = Category.query.get(category_id)
        category = subreddit_obj.category_name
        subreddit_url = subreddit_obj.subreddit_search
        subreddit_dict = get_subreddits_by_interest(subreddit_url)
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
   
    flash("Welcome %s %s. Please check the categories you're interested in." % (firstname,lastname))

    #instantiate a user in the User database.
    new_user = User.instantiate_user(firstname,lastname,email,password)
    session['user_id'] = new_user.user_id 
    
    return redirect('/declare_interests')

 
@app.route("/declare_interests")
def user_interests_form():
    """take care of users who want to change what their interests are"""

    category_names = categories.keys()
    category_names.sort()
    user_id = session['user_id']
    # user = UserCategory.query.filter_by(user_id=user_id).all()
    #if user_id=1:[<User user_id=1 name=lori@bardfamily.org> lastname=bard]
    # user = User.query.filter_by(user_id=user_id).first()
    # is user_id=1:[UserCategory=1 User=1 Category=1, UserCategory=2 User=1 Category=2]
    # users_categories = UserCategory.query.filter_by(user_id=user_id).all()
    category_list = []
    users_category_ids = db.session.query(UserCategory.category_id).filter_by(user_id=user_id).all()
    #notes on above:db.session.query(UserCategory.category_id).filter_by(user_id=1).all()
    #yields [(1,), (2,)]
    if len(users_category_ids) > 0:
    
        for user_category_id in users_category_ids:
            category_id = user_category_id[0]
            user_category_obj=Category.query.get(category_id)
            category_list.append(user_category_obj.category_name)
    

    return render_template("declare_interests.html",
                           category_names=category_names,
                           category_list=category_list
                           )


@app.route("/declare_interests" , methods=['POST'])
def register_interests():
    user_id = session['user_id']
    if db.session.query(UserCategory):
        db.session.query(UserCategory).filter_by(user_id=user_id).delete()
        db.session.commit()
    interests = request.form.getlist("interest_change")
    interest_list = []
    #look up teh category id on every category(interest) chosen to put in the association table
    for interest in interests:
        interest_add_on = db.session.query(Category.category_id).filter_by(category_name=interest).first()
        interest_list.append(interest_add_on[0])
    UserCategory.instantiate_usercategory(user_id,interest_list)

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
    return redirect('/declare_interests')

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




