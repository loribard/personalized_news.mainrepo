from model import db, connect_to_db, make_test_data, User, Category, UserCategory

def get_category(user_category_id):
    category =  UserCategory.query.filter_by(
             user_category_id=user_category_id).first()

    return category.category_name