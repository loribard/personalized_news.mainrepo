import random

from flask import session

from model import connect_to_db, db, User, Category, UserCategory
from reddit import get_posts_by_interest


def get_news(limit=3):
    """ get the newsfeed that will print out on thenews.html
        """

    user_id= session['user_id']
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
        posts = get_posts_by_interest(subreddit_url,limit)
        dictionary_to_unpack_in_html[category] = posts

    return dictionary_to_unpack_in_html


def get_declared_interests(user_id):
    """ get a list of the interests the user has. If the user has interests registered, they appear checked
    """
    
    # user_id = session['user_id']
    category_list = []
    users_category_ids = db.session.query(UserCategory.category_id).filter_by(user_id=user_id).all()
   
    if len(users_category_ids) > 0:
    
        for user_category_id in users_category_ids:
            category_id = user_category_id[0]
            user_category_obj=Category.query.get(category_id)
            category_list.append(user_category_obj.category_name)
             
    
    category_list.sort()
       
    return category_list



def personalize_name(user_id):
    """make user's name appear on the navbar when the user is logged in"""


    user_id=session['user_id']
    user = User.query.get(user_id)
    user_name = user.firstname
    user_name = str(user_name) + "'s"
    
    return user_name












