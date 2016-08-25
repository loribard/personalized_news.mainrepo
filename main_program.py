import random

from flask import session

from model import connect_to_db, db, User, Category, UserCategory
from reddit import get_subreddits_by_interest

NEWS_QUOTES= ['We relish news of our heroes, forgetting that we are extraordinary to somebody too.', 'In the business world, bad news is usually good news---for somebody else.',"If it's bad news, we just have to get on and deal with it.", "Evening news is where they begin with 'Good Evening' and then proceed to tell you why it isn\'t.", 'News is to the mind what sugar is to the body.', 'Bad news travels fast. Good news takes the scenic route.', 'BREAKING NEWS: You\'re awesome and designed for success; live this day accordingly!', 'The bad news is time flies. The good news is you\'re the pilot.']


def get_news():
    """ get the newsfeed that will print out on thenews.html"""



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
            thumbnail=posts['thumbnail']
            preview=posts['preview']
            i+=1
            titles.append((title, url,thumbnail,preview))
            
        dictionary_to_unpack_in_html[category]=titles


    return dictionary_to_unpack_in_html


def get_declared_interests():
    """ get a list of the interests the user has. If the user has interests registered, they appear checked
        """

    user_id = session['user_id']
    category_list = []
    users_category_ids = db.session.query(UserCategory.category_id).filter_by(user_id=user_id).all()
   
    if len(users_category_ids) > 0:
    
        for user_category_id in users_category_ids:
            category_id = user_category_id[0]
            user_category_obj=Category.query.get(category_id)
            category_list.append(user_category_obj.category_name)
             

    return category_list




def get_news_quote():
    """print out a quote about news"""
    print random.choice(NEWS_QUOTES)
    
    return random.choice(NEWS_QUOTES)


def personalize_name(user_id):
    """make user's name appear on the navbar when the user is logged in"""

    user_id=session['user_id']
    user = User.query.get(user_id)
    user_name = user.firstname
    user_name = str(user_name) + "'s"
    
    return user_name












