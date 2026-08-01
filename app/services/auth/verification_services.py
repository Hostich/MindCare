from datetime import datetime, timedelta
from flask import session
from app.services.auth.email_services import (
        generate_verification_code,
        send_verification_email
    )
    
    
def start_email_verification(data):
    code = generate_verification_code()
        
    session["verification_code"] = code
    session["registration_data"] = data
    session["verification_time"] = datetime.utcnow().isoformat()
    send_verification_email(
        email=data["email"],
        username=data["username"],
        code=code
        )
    return code
    
    
def verify_registration_code(entered_code):
    verification_time = session.get("verification_time")

    if not verification_time:
        return "Verification session expired."

    verification_time = datetime.fromisoformat(verification_time)
    
    if datetime.utcnow() > verification_time + timedelta(minutes=10):
        return False, "expired", "Your verification code has expired. Please register again."
        
    if entered_code != session.get("verification_code"):
        return False, "invalid", "Invalid verification code."
    
    return True, None, None
    
    
def clear_verification_session():
    session.pop("verification_code", None)
    session.pop("registration_data", None)
    session.pop("verification_time", None)
    