from sqlalchemy import func

from model import connect_to_db,db,User
from reddit_example_server import app

"""Utility file to seed MyNews database"""

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

def load_users():
    print "Users"
    Users= {"user1":
            {"name":"lori","password":"hi there"}
            }
    
    for key in Users.keys():
        print "Key ", key
        print "Value", Users[key]
        name = Users[key]["name"]
        print "Name: ", name
        password = Users[key]["password"]
        print "Password: ", password
        user=User(name=name,password=password)
    
        db.session.add(key)
    db.session.commit()



# def load_movies():
#     """Load movies from u.item into database."""

#     print "Movies"

#     for i, row in enumerate(open("seed_data/u.item")):
#         row = row.rstrip()

#         # clever -- we can unpack part of the row!
#         movie_id, title, released_str, junk, imdb_url = row.split("|")[:5]

#         # The date is in the file as daynum-month_abbreviation-year;
#         # we need to convert it to an actual datetime object.

#         if released_str:
#             released_at = datetime.datetime.strptime(released_str, "%d-%b-%Y")
#         else:
#             released_at = None

#         # Remove the (YEAR) from the end of the title.

#         title = title[:-7]   # " (YEAR)" == 7

#         movie = Movie(title=title,
#                       released_at=released_at,
#                       imdb_url=imdb_url)

#         # We need to add to the session or it won't ever be stored
#         db.session.add(movie)

#         # provide some sense of progress
#         if i % 100 == 0:
#             print i

#     # Once we're done, we should commit our work
#     db.session.commit()


# def load_ratings():
#     """Load ratings from u.data into database."""

#     print "Ratings"

#     for i, row in enumerate(open("seed_data/u.data")):
#         row = row.rstrip()

#         user_id, movie_id, score, timestamp = row.split("\t")

#         user_id = int(user_id)
#         movie_id = int(movie_id)
#         score = int(score)

#         # We don't care about the timestamp, so we'll ignore this

#         rating = Rating(user_id=user_id,
#                         movie_id=movie_id,
#                         score=score)

#         # We need to add to the session or it won't ever be stored
#         db.session.add(rating)

#         # provide some sense of progress
#         if i % 1000 == 0:
#             print i

#             # An optimization: if we commit after every add, the database
#             # will do a lot of work committing each record. However, if we
#             # wait until the end, on computers with smaller amounts of
#             # memory, it might thrash around. By committing every 1,000th
#             # add, we'll strike a good balance.

#             db.session.commit()

#     # Once we're done, we should commit our work
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


# if __name__ == "__main__":
#     connect_to_db(app)
#     db.create_all()

    # load_users()
    # load_movies()
    # load_ratings()
    # set_val_user_id()
