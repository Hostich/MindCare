import re
from werkzeug.security import check_password_hash
from app.models import User
from app.services.auth.user_services import get_user_by_email, get_user_by_username


def validate_registration(data):
    errors=[]
    
    username = data.get("username", "").strip()
    email = data.get("email", "").strip()
    phone_number = data.get("phone_number", "").strip()
    occupation = data.get("occupation", "").strip()
    password = data.get("password", "")
    confirm_password = data.get("confirm_password", "")
    
    if not username:
        errors.append("username is required.")
        
    if not email:
        errors.append("Email is required.")

    if not phone_number:
        errors.append("Phone number is required.")
    
    if not occupation:
        errors.append("Occupation is required.")
        
    if not password:
        errors.append("Password is required.")
        
    if password != confirm_password:
        errors.append("Passwords do not match.")
        
    if username and User.query.filter_by(username=username).first():
        errors.append("User name is already taken.")
    
    if email and User.query.filter_by(email=email).first():
        errors.append("Email is already registered.")
        
    if phone_number and User.query.filter_by(phone_number=phone_number).first():
        errors.append("Phone number is already registered.")
    
    return errors
    
def authenticate_user(identifier, password):
    if "@" in identifier:
        user = get_user_by_email(identifier)
    else:
        user = get_user_by_username(identifier)
        
    if not user:
        return False, None, "User Not Found."
    
    if not check_password_hash(user.password, password):
        return False, None, "Incorrect password."
    
    return True, user, None
    
def get_dashboard_route(role):
    if role == 'Admin':
        return "admin.dashboard"
    elif role == 'Volunteer':
        return "volunteer.dashboard"
    elif role == 'Counselor':
        return "counselor.dashboard"
    elif role == 'Seeker':
        return "seeker.dashboard"
    else:
        return "lpage.home"
        
        