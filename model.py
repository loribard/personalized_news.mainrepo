"""Models and database functions for Ratings project."""

from flask_sqlalchemy import SQLAlchemy
from reddit import get_subreddits_by_interest


# This is the connection to the PostgreSQL database; we're getting
# this through the Flask-SQLAlchemy helper library. On this, we can
# find the `session` object, where we do most of our interactions
# (like committing, etc.)

db = SQLAlchemy()


#####################################################################
# Model definitions

class User(db.Model):
    """User of ratings website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    firstname = db.Column(db.String(64), nullable=True)
    lastname = db.Column(db.String(64),nullable=True)
    email = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(64), nullable=True)
    interest = db.Column(db.Array(Integer))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id=%s name=%s> lastname=%s" % (self.user_id,
                                               self.email,self.lastname)

class Category(db.Model):
    """Categories which users can choose from"""

    __tablename__="categories"

    category_id = db.Column(db.Integer,
                            autoincrement=True,
                            primary_key=True)
    category = db.Column(db.String(35), nullable=True)

    def __repr__(self):

        return "<Category ID=%d Category=%s>" % (self.category_id,self.category)


class Association_table(db.Model):
    """A table to link users and their interests"""

    __tablename__ = 'user_category_link'

    association_id = db.Column(db.Integer,
                     autoincrement=True,
                     primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id'))

    def __repr__(self):

        return "Association=%d User=%d Category=%d" %(self.association_id,self.user_id,self.category_id)




        

#####################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///subreddits'
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will
    # leave you in a state of being able to work with the database
    # directly.

    from server import app
    from server import r

    connect_to_db(app)
    print "Connected to DB."



# class Subreddit(db.Model):
#     """Movie on ratings website."""

#     __tablename__ = "subreddits"

#     # sub = get_subreddits_by_interest('funny')
#     #load_subreddits(sub)

#     subr_num = db.Column(db.Integer,
#                          autoincrement=False,
#                          primary_key=True)
#     category = db.Column(db.String(30))
#     title= db.Column(db.String(100))
#     url = db.Column(db.String(200))

#     def __repr__(self):
#         """Provide helpful representation when printed."""
#         return "<Subreddit category=%s  title=%s  url=%s>"% (self.category,self.title, self.url)

