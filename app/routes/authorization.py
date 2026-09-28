from flask import Blueprint, render_template, request, redirect, session, flash, url_for
from flask_login import login_user, logout_user, login_required
from app.services.auth.user_services import (
    create_user,
    get_user_by_email
)
from app.services.auth.auth_services import (
    validate_registration,
    authenticate_user,
    reset_user_password
)
from app.services.auth.verification_services import (
    start_email_verification,
    verify_registration_code,
    clear_verification_session,
    start_password_reset_verification,
    verify_password_reset_code,
    clear_password_reset_session
)
from app.services.mood.mood_services import has_mood_today
from app.models import User
from app import db

auth = Blueprint("auth", __name__, url_prefix="/auth")


# =========================================================
# REGISTER
# =========================================================

@auth.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        data = {
            "username": request.form.get("username"),
            "email": request.form.get("email"),
            "phone_number": request.form.get("phonenumber"),
            "occupation": request.form.get("occupation"),
            "password": request.form.get("password"),
            "confirm_password": request.form.get("confirmpassword")
        }

        errors = validate_registration(data)

        if errors:
            for error in errors:
                flash(error, "danger")

            return render_template("authorize/register.html")

        start_email_verification(data)

        return redirect(url_for("auth.verify_email"))

    return render_template("authorize/register.html")


# =========================================================
# VERIFY EMAIL
# =========================================================

@auth.route("/verify-email", methods=["GET", "POST"])
def verify_email():

    if request.method == "POST":

        entered_code = request.form.get("verification_code")

        success, error_code, message = verify_registration_code(
            entered_code
        )

        if not success:

            if error_code == "expired":

                clear_verification_session()

                flash(message, "danger")

                return redirect(url_for("auth.register"))

            flash(message, "danger")

            return render_template(
                "authorize/verify_email.html"
            )

        data = session["registration_data"]

        create_user(data)

        clear_verification_session()

        flash(
            "Your account has been created successfully. You may now log in.",
            "success"
        )

        return redirect(url_for("auth.login"))

    return render_template(
        "authorize/verify_email.html"
    )


# =========================================================
# LOGIN
# =========================================================

@auth.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        identifier = request.form.get(
            "identifier",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        )

        success, user, message = authenticate_user(
            identifier,
            password
        )

        if not success:

            flash(message, "danger")

            return render_template(
                "authorize/login.html"
            )

        login_user(user)

        # ROLE-BASED REDIRECTION

        if user.role == "Admin":

            return redirect(
                url_for("admin.dashboard")
            )

        elif user.role == "Volunteer":

            return redirect(
                url_for("volunteer.dashboard")
            )

        elif user.role == "Counselor":

            return redirect(
                url_for("counselor.dashboard")
            )

        elif user.role == "Seeker":

            if has_mood_today(user.user_id):

                return redirect(
                    url_for("seeker.dashboard")
                )

            return redirect(
                url_for("mood.mood_entry")
            )

        return redirect(
            url_for("lpage.home")
        )

    return render_template(
        "authorize/login.html"
    )
# =========================================================
# FORGOT PASSWORD
# =========================================================

@auth.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():

    if request.method == "POST":

        email = request.form.get(
            "email",
            ""
        ).strip().lower()

        if not email:

            flash(
                "Please enter your email address.",
                "danger"
            )

            return redirect(
                url_for("auth.forgot_password")
            )

        user = get_user_by_email(email)

        if not user:

            flash(
                "No account found with that email address.",
                "danger"
            )

            return redirect(
                url_for("auth.forgot_password")
            )

        # Generate and send OTP
        start_password_reset_verification(user)

        flash(
            "A verification code has been sent to your email.",
            "success"
        )

        return redirect(
            url_for("auth.verify_reset_otp")
        )

    return render_template(
        "authorize/forgot_password.html"
    )


# =========================================================
# VERIFY RESET OTP
# =========================================================

@auth.route("/verify-reset-otp", methods=["GET", "POST"])
def verify_reset_otp():

    if not session.get("password_reset_user_id"):

        flash(
            "Your password reset session has expired.",
            "danger"
        )

        return redirect(
            url_for("auth.forgot_password")
        )

    if request.method == "POST":

        entered_code = request.form.get(
            "otp",
            ""
        ).strip()

        success, error_code, message = verify_password_reset_code(
            entered_code
        )

        if not success:

            if error_code == "expired":

                clear_password_reset_session()

                flash(
                    message,
                    "danger"
                )

                return redirect(
                    url_for("auth.forgot_password")
                )

            flash(
                message,
                "danger"
            )

            return render_template(
                "authorize/verify_reset_otp.html"
            )

        # OTP is correct
        session["password_reset_verified"] = True

        return redirect(
            url_for("auth.reset_password")
        )

    return render_template(
        "authorize/verify_reset_otp.html"
    )


# =========================================================
# RESET PASSWORD
# =========================================================

@auth.route("/reset-password", methods=["GET", "POST"])
def reset_password():

    user_id = session.get(
        "password_reset_user_id"
    )

    otp_verified = session.get(
        "password_reset_verified"
    )

    # User must verify OTP first
    if not user_id or not otp_verified:

        flash(
            "Please verify the OTP first.",
            "danger"
        )

        return redirect(
            url_for("auth.forgot_password")
        )

    user = User.query.get(user_id)

    if not user:

        clear_password_reset_session()

        flash(
            "User not found.",
            "danger"
        )

        return redirect(
            url_for("auth.forgot_password")
        )

    if request.method == "POST":

        password = request.form.get(
            "password",
            ""
        )

        confirm_password = request.form.get(
            "confirm_password",
            ""
        )

        if not password:

            flash(
                "Password is required.",
                "danger"
            )

            return render_template(
                "authorize/reset_password.html"
            )

        if password != confirm_password:

            flash(
                "Passwords do not match.",
                "danger"
            )

            return render_template(
                "authorize/reset_password.html"
            )

        reset_user_password(
            user,
            password
        )

        db.session.commit()

        # Clear password reset session
        clear_password_reset_session()

        flash(
            "Your password has been successfully reset. You may now log in.",
            "success"
        )

        return redirect(
            url_for("auth.login")
        )

    return render_template(
        "authorize/reset_password.html"
    )

# =========================================================
# LOGOUT
# =========================================================

@auth.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect(
        url_for("auth.login")
    )
