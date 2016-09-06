import json

from sqlalchemy import func

from model import  db, connect_to_db, Category, User, UserCategory, categories
from server import app


"""Utility file to seed MyNews database"""

def store_categories(categories_dict):
    """Seed the categories which the user will see news from"""


    for category_name,subreddit_search_list in categories.iteritems():
        subreddit_search = '+'.join(subreddit_search_list) 
        new_category = Category(category_name=category_name, subreddit_search=subreddit_search)
        db.session.add(new_category)
    db.session.commit()
    print "Categories loaded"

def set_val_user_id():
    """Set value for the next user_id after seeding database"""

   
    if len(db.session.query(User.user_id).all()) > 0: 
    # Get the Max user_id in the database
        result = db.session.query(func.max(User.user_id)).one()
        max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
        query = "SELECT setval('users_user_id_seq', :new_id)"
        db.session.execute(query, {'new_id': max_id + 1})
        db.session.commit()



if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    store_categories(categories)
    set_val_user_id()
    
   