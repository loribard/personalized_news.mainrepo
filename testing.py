"""tests for ratings project"""

from unittest import TestCase
from model import db, connect_to_db, make_test_data, User, Category, UserCategory
from server import app
from db_func import get_category

# class DatabaseTests(TestCase):
#     """database tests """

#     def setUp(self):
#         """before every test"""
#         self.client = app.test_client()
#         app.config['TESTING'] = True
#         connect_to_db(app, 'postgresql:///subreddittest')
#         db.create_all()
#         make_test_data()

#     def tearDown(self):
#         """after every test"""

#         db.session.close()
#         db.drop_all()

#     def test_get_rating_for_user(self):
#         """get the category from category_id 1, user_id 1"""

#         user_category_id = 1
        

#         category = get_category(user_category_id)
#         self.assertEqual(category.category_name, 'Pets')



class FlaskDatabaseTests(TestCase):

    def setUp(self):
        """before every test"""
        client = app.test_client()
        app.config['TESTING'] = True
        connect_to_db(app, 'postgresql:///subreddittest')
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
                            'password': 'melissa',
                          }

        result = self.client.post("'/register_form'",
                              data=registration_data,
                              )

        self.assertEqual(result.status_code, 200)
        self.assertIn(email, result.data)


if __name__ == "__main__":
    import unittest

    unittest.main()

