from src.extentions import db
from src.models import User

def create_test_user(app):
    with app.app_context():
        new_user = User(name = "Bob")
        db.session.add(new_user)
        db.session.commit()

        salved_user = User.query.filter_by(name="Bob").first()
        
        assert salved_user is not None
        assert salved_user.name == "Bob"
        assert salved_user.id is not None
