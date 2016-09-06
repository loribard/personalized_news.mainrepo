"""tests for ratings project"""

from unittest import TestCase
import doctest

from model import db, connect_to_db, make_test_data, User, Category, UserCategory
from server import app
from main_program import get_declared_interests
from flask import session
import seed
import reddit
import main_program
from main_program import get_news
# to test:
# python testing.py
# coverage:
# coverage run --omit=seed.,env/* testing.py
# for report:
# coverage report -m
# coverage html



def load_tests(loader,tests,ignore):
    """ to run doctests"""

    tests.addTests(doctest.DocTestSuite(reddit))
    tests.addTests(doctest.DocTestSuite(main_program))
    return tests
    

class FlaskTestsBasic(TestCase):
    """Flask tests."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

    def test_index(self):
        """Test homepage page."""

        result = self.client.get("/")
        self.assertIn("My News", result.data)



class DatabaseTests(TestCase):
    """database tests """

    def setUp(self):
        # self.client = app.test_client()
        # app.config['TESTING'] = True
        connect_to_db(app, db_uri = "postgresql:///testsubreddits")
        db.create_all()
        make_test_data()

    def tearDown(self):
        """after every test"""

        db.session.close()
        db.drop_all()

    def test_get_category_for_user(self):
        """get the category names for user_id 1"""

        user_category_id = 1
        category = UserCategory.query.get(1).category_id
        self.assertEqual(Category.query.get(category).category_name, 'Pets')


    def test_to_get_declared_interests_by_user(self):
      

        result = get_declared_interests(1) 
        self.assertEqual(['Pets'] ,result)
             
   
    def test_user_table(self):
        """ get the information on a user"""

        
        result = User.query.get(1).firstname
        self.assertEqual(result, "lori")   



class FlaskDatabaseTests(TestCase):

    def setUp(self):
        """before every test"""
        self.client = app.test_client()
        app.config['TESTING'] = True
        connect_to_db(app, db_uri = 'postgresql:///testsubreddits')
        db.create_all()
        make_test_data()


    def tearDown(self):
        """after every test"""

        db.session.close()
        db.drop_all()


    def test_categories(self):


        result = self.client.get("/news/google-news")
       
        self.assertIn("Google Headline News",result.data)


    def test_register(self):
        """test registration"""

        email = 'melissa@bardfamily.org'

        registration_data = {
                            'firstname': 'melissa',
                            'lastname': 'bard',
                            'email': email,
                            'password': 'melissa'
                          }

        result = self.client.post('/register_form',
                              data=registration_data,
                              follow_redirects=True
                              )

        self.assertEqual(result.status_code, 200)




    def test_login(self):
        """test login page"""

        result = self.client.post("/login", 
                                  data={"email": "lori@bardfamily.org", "password": "lori"},
                                  follow_redirects=True)
        self.assertIn('Logged in', result.data)

    def test_get_user(self):


        email = "lori@bardfamily.org"
        user = User.query.filter_by(email = email).one()

        self.assertEqual(user.firstname,"lori")


        

class MyAppIntegrationTestCase(TestCase):
    """ test integration with flask and routes"""


    def test_index(self):
        client = app.test_client()
        app.config['TESTING'] = True
        result = client.get('/login')
        self.assertIn('<h1>Login</h1>',result.data)

    def test_registration_form(self):
        client = app.test_client()
        app.config['TESTING'] = True
        result = client.get('/register_form')
        self.assertIn('<h1>Register</h1>', result.data)

    def test_newssource_info(self):
        client = app.test_client()
        app.config['TESTING'] = True
        result = client.get('/news/bbc-news')
        self.assertIn('<div id="headlines">', result.data)





class FlaskTestsLoggedOut(TestCase):
    """Flask tests with user logged in to session."""

    def setUp(self):
        """Stuff to do before every test."""

        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_important_page(self):
        """Test that user can't see important page when logged out."""

        result = self.client.get("/important", follow_redirects=True)
        self.assertNotIn("You are a valued user", result.data)
        self.assertIn("My News", result.data)
 


if __name__ == "__main__":
    import unittest

    unittest.main()

