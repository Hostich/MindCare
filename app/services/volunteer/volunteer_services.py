from app.models import User

def get_all_volunteers():
    return User.query.filter_by(role="Volunteer").all()

