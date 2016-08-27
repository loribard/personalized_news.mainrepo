"""tests for ratings project"""

from unittest import TestCase
from model import db, connect_to_db, make_test_data, User, Category, UserCategory
from server import app
from db_func import get_category

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

    def test_get_rating_for_user(self):
        """get the category names for user_id 1"""

        user_category_id = 1
        

        category = get_category(user_category_id)
        self.assertEqual(Category.query.get(category).category_name, 'Pets')

       



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
        

class MyAppIntegrationTestCase(TestCase):
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

   

if __name__ == "__main__":
    import unittest

    unittest.main()

