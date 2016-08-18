"""Models and database functions for Ratings project."""

from flask_sqlalchemy import SQLAlchemy
from reddit import get_subreddits_by_interest



# This is the connection to the PostgreSQL database; we're getting
# this through the Flask-SQLAlchemy helper library. On this, we can
# find the `session` object, where we do most of our interactions
# (like committing, etc.)

db = SQLAlchemy()

categories = {
    "Sports": ["sports", "olympics", "pro sports", "college sports", "action sports"],
    "Science": ["science", "askscience", "biotech", "chemistry", "biology", "biochemistry","labrats" ],
    "Pets": ["aww", "cats", "catgifs", "dogs", "pets", "doggifs", "animalsbeingderps"],
    "Wild Animals": ["wildlife", "wildliferehab", "babyelephantgifs", "tigerpics" , "giraffes"],
    "Local News": ["sanfrancisco", "burlingame", "bayarea", "sfbeer", "sfbayhousing"],
    "Life Tips": ["lifeprotips", "eplainlikeimfive"],
    "World News": ["worldnews"],
    "Movie Scuttlebutt": ['movies'],


}


#####################################################################
# Model definitions

class User(db.Model):
    """User of MyNews website."""


    __tablename__ = "users"

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    firstname = db.Column(db.String(64), nullable=True)
    lastname = db.Column(db.String(64),nullable=True)
    email = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(64), nullable=True)
    
    categories = db.relationship("Category",
                                  secondary="users_categories",
                                  backref="users")

    def __repr__(self):
        """Provide helpful representation on a user when printed."""

        return "<User user_id=%s name=%s> lastname=%s" % (self.user_id,
                                               self.email,self.lastname)

    @classmethod
    def instantiate_user(cls, firstname, lastname, email, password):
        """Instantiate a user as a member"""

        new_user = User(firstname=firstname,
                        lastname=lastname,
                        email=email,
                        password=password)
        db.session.add(new_user)
        db.session.commit()
        return new_user


class Category(db.Model):
    """Categories which users can choose from"""

    __tablename__="categories"

    category_id = db.Column(db.Integer,
                            autoincrement=True,
                            primary_key=True)
    category_name = db.Column(db.String(35), nullable=True)
    subreddit_search = db.Column(db.String(300), nullable=True)

    def __repr__(self):
        """Show category and associated id """

        return "<Category ID=%d Category=%s>" % (self.category_id,self.category_name)



class UserCategory(db.Model):
    """A table to link users and their interests"""


    __tablename__ = 'users_categories'

    user_category_id = db.Column(db.Integer,
                     autoincrement=True,
                     primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id'))
    

    def __repr__(self):
        """Table to associate user_id and category_id's...each have their own association id"""

        return "UserCategory=%d User=%d Category=%d" %(self.user_category_id,self.user_id,self.category_id)


    @classmethod
    def instantiate_usercategory(cls,user_id,interest_list):
        """"Make an association table for the member and their interests."""


        for interest in interest_list:
            association = UserCategory(user_id=user_id,category_id=interest)
            db.session.add(association)
        db.session.commit() 
        return association   


        

#####################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///subreddits'
    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will
    # leave you in a state of being able to work with the database
    # directly.

    from server import app
    from server import r

    connect_to_db(app)
    
    print "Connected to DB"

