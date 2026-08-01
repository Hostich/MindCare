from app.extensions import db

def update_profile(user, data):
    user.first_name = data["first_name"]
    user.last_name = data["last_name"]
    user.phone_number = data["phone_number"]
    user.gender = data["gender"]

    db.session.commit()

    

