from sqlalchemy import func
import json

from model import  db, User, Subreddit, connect_to_db


"""Utility file to seed MyNews database"""


users_dict = {"user1":
            {"name":"lori","password":"hi there"}
            }

def load_users(users_dict):
    print "Users"

    for key in users_dict.keys():
        print "Key ", key
        print "Value", users_dict[key]
        name = users_dict[key]["name"]
        print "Name: ", name
        password = users_dict[key]["password"]
        print "Password: ", password
        user=User(name=name,password=password)
    
        db.session.add(key)
    db.session.commit()



def load_subreddits(sub):
    """Load seed subreddit...first 5 articles under the "funny" subreddit. """

 
    category = sub.keys()
    category = category[0]
    values = sub[category]
    print values
    for key,value in values.items():
        item = key
        title=values[key]["title"]
        url = values[key]["url"]
        subr=Subreddit(subr_num=item,category=category,title=title,url=url)
        print item,category,title,url
        db.session.add(key)
    db.session.commit()
       




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

    load_users(users_dict)
    load_subreddits(sub)
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
