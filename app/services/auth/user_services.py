from werkzeug.security import generate_password_hash
from app.extensions import db
from app.models import User

def create_user(data):
    hashed_password = generate_password_hash(data["password"])
        
    new_user = User(
        username=data["username"],
        email=data["email"],
        phone_number = data["phone_number"],
        occupation = data["occupation"],
        password=hashed_password
    )
        
    db.session.add(new_user)
    db.session.commit()
    
    return new_user
    
    
def get_user_by_email(email):
    return User.query.filter_by(email=email).first()
    
def get_user_by_username(username):
    return User.query.filter_by(username=username).first()