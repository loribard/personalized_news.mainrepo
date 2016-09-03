"""tests for ratings project"""

from unittest import TestCase
from model import db, connect_to_db, make_test_data, User, Category, UserCategory
from server import app
from db_func import get_category
from main_program import get_declared_interests
from flask import session

# to test:
# python testing.py
# coverage:
# coverage run --omit=env/* testing.py
# for report:
# coverage report -m
# coverage html

# def load_tests(loader, tests, ignore):
#     """Also run our doctests and file-based doctests."""

#     tests.addTests(doctest.DocTestSuite(server))
#     tests.addTests(doctest.DocFileSuite("tests.txt"))
#     return tests

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
        category = get_category(user_category_id)
        self.assertEqual(Category.query.get(category).category_name, 'Pets')


    def test_to_get_declared_interests_by_user(self):
       
      
        result = get_declared_interests(1)
        print result,"^^^^^^^^^^^^^^^"
        
        # user_category_ids = db.session.query(UserCategory.category_id).filter_by(user_id=user_id).all()
        # print user_category_ids,"**************************"
        # for user_category_id in user_category_ids:
        #     category_id = user_category_ids[0]
        #     user_category_obj=Category.query.get(category_id)
        #     category_list.append(str(user_category_obj.category_name))
        
        self.assertEqual(['Pets'] ,result)
             
    

   
    def test_user_table(self):
        """ get the information on a user"""

        user_id = 1
        self.assertEqual(User.query.get(user_id).firstname,"lori")   



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

    # def test_category_database(self):

    #     """in test database:pets = Category(category_name='Pets', subreddit_search=["aww", "cats", "catgifs", "dogs", "pets", "doggifs", "animalsbeingderps"])"""

    #     category = Category.query.get(1)
    #     categoryname = category.category_name
       
    #     category_search_url = category.subreddit_search
    

    #     result = self.client.get(data={categoryname: "Pets"})
    #     self.assertEqual(result.data)


    def test_login(self):
        """test login page"""

        result = self.client.post("/login", 
                                  data={"email": "lori@bardfamily.org", "password": "lori"},
                                  follow_redirects=True)
        self.assertIn('Logged in', result.data)


        

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


class FlaskTestsLoggedIn(TestCase):
    """Flask tests with user logged in to session."""

    def setUp(self):
        """Stuff to do before every test."""

        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'ABC'
      
        self.client = app.test_client()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1

    # def test_declared_interests(self):
    #     """test to see if the correct interests comeback"""



    #     result = get_declared_interests(1)
    #     print result 
        
    #     self.assertIn("Pets", result)


    def test_important_page(self):
        """Test important page."""

        result = self.client.get("/important")
        self.assertIn("You are a valued user", result.data)  


if __name__ == "__main__":
    import unittest

    unittest.main()

