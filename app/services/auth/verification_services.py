from datetime import datetime, timedelta
from flask import session

from app.services.auth.email_services import (
    generate_verification_code,
    send_verification_email
)


# =========================================================
# REGISTRATION EMAIL VERIFICATION
# =========================================================

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

    verification_time = session.get(
        "verification_time"
    )

    if not verification_time:

        return (
            False,
            "expired",
            "Verification session expired."
        )

    verification_time = datetime.fromisoformat(
        verification_time
    )

    # OTP expires after 10 minutes
    if datetime.utcnow() > verification_time + timedelta(minutes=10):

        return (
            False,
            "expired",
            "Your verification code has expired. Please register again."
        )

    # Check OTP
    if entered_code != session.get(
        "verification_code"
    ):

        return (
            False,
            "invalid",
            "Invalid verification code."
        )

    return (
        True,
        None,
        None
    )


# =========================================================
# FORGOT PASSWORD OTP
# =========================================================

def start_password_reset_verification(user):

    code = generate_verification_code()

    session["password_reset_code"] = code
    session["password_reset_user_id"] = user.user_id
    session["password_reset_time"] = datetime.utcnow().isoformat()

    send_verification_email(
        email=user.email,
        username=user.username,
        code=code
    )

    return code


def verify_password_reset_code(entered_code):

    verification_time = session.get(
        "password_reset_time"
    )

    if not verification_time:

        return (
            False,
            "expired",
            "Your OTP session has expired. Please request a new code."
        )

    verification_time = datetime.fromisoformat(
        verification_time
    )

    # OTP expires after 10 minutes
    if datetime.utcnow() > verification_time + timedelta(minutes=10):

        return (
            False,
            "expired",
            "Your OTP has expired. Please request a new code."
        )

    # Check OTP
    if entered_code != session.get(
        "password_reset_code"
    ):

        return (
            False,
            "invalid",
            "Invalid OTP. Please try again."
        )

    return (
        True,
        None,
        None
    )


# =========================================================
# CLEAR REGISTRATION VERIFICATION
# =========================================================

def clear_verification_session():

    session.pop(
        "verification_code",
        None
    )

    session.pop(
        "registration_data",
        None
    )

    session.pop(
        "verification_time",
        None
    )


# =========================================================
# CLEAR PASSWORD RESET VERIFICATION
# =========================================================

def clear_password_reset_session():

    session.pop(
        "password_reset_code",
        None
    )

    session.pop(
        "password_reset_user_id",
        None
    )

    session.pop(
        "password_reset_time",
        None
    )

    session.pop(
        "password_reset_verified",
        None
    )