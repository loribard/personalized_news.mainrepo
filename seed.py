from sqlalchemy import func
import json
from server import app

from model import  db, connect_to_db, Category


"""Utility file to seed MyNews database"""


category_choice_list = ['AskReddit','funny','todayilearned','pics','science', 'worldnews', 'IAmA', 'announcements',
                    'videos', 'gaming','blog', 'movies','Music','aww','news','gifs', 'explainlikeimfive','askscience','books','television', 
                    'LifeProTips']

def load_categories(category_list):   

    """Seed the categories which the user will see news from"""
    for category in category_list:
        category = Category(category=category)
        db.session.add(category)
    db.session.commit()






# def load_subreddits(sub):
#     """Load seed subreddit...first 5 articles under the "funny" subreddit. """

 
#     category = sub.keys()
#     category = category[0]
#     values = sub[category]
#     print values
#     for key,value in values.items():
#         item = key
#         title=values[key]["title"]
#         url = values[key]["url"]
#         subr=Subreddit(subr_num=item,category=category,title=title,url=url)
#         print item,category,title,url
#         db.session.add(key)
#     db.session.commit()
       




# def set_val_user_id():
#     """Set value for the next user_id after seeding database"""

#     # Get the Max user_id in the database
#     result = db.session.query(func.max(User.user_id)).one()
#     max_id = int(result[0])

#     # Set the value for the next user_id to be max_id + 1
#     query = "SELECT setval('users_user_id_seq', :new_id)"
#     db.session.execute(query, {'new_id': max_id + 1})
#     db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    # load_users(users_dict)
    load_categories(category_choice_list)
    # load_subreddits()
    # load_ratings()
    # set_val_user_id()

    # def fetch_listing(url):
#     response = requests.get(url)
#     return response.text

# def decode_listing_str(listing_str):
#     listing_dict = json.loads(listing_str)
#     return listing_dict

# def print_titles(listing_dict):
#     posts = listing_dict["data"]["children"]
#     for post in posts:
#         print post["data"]["title"]

# def main():
#     listing_str = fetch_listing(URL)
#     listing_dict = decode_listing_str(listing_str)
#     print_titles(listing_dict)

# if __name__ == '__main__':
#     main()
