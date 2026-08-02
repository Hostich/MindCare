from flask import Blueprint, render_template, request, redirect, session, flash, url_for
from flask_login import login_user
from app.services.auth.user_services import create_user
from app.services.auth.auth_services import validate_registration, authenticate_user
from app.services.auth.verification_services import start_email_verification, verify_registration_code, clear_verification_session
from app.services.mood.mood_services import has_mood_today


auth = Blueprint("auth", __name__, url_prefix = "/auth")

@auth.route("/register", methods=['GET','POST'])
def register():
    if request.method == "POST":
        data = {
            "username" : request.form.get("username"),
            "email" : request.form.get("email"),
            "phone_number" : request.form.get("phonenumber"),
            "occupation" : request.form.get("occupation"),
            "password" : request.form.get("password"),
            "confirm_password" : request.form.get("confirmpassword")
        }
       
        errors = validate_registration(data)
        
        if errors:
            for error in errors:
                flash(error, "danger")
       
            return render_template("authorize/register.html")
            
        start_email_verification(data)
        
        return redirect("/auth/verify-email")

    return render_template("authorize/register.html")
    
    
@auth.route("/verify-email", methods=['GET', 'POST'])
def verify_email():
    if request.method == "POST":     
        entered_code = request.form.get("verification_code")
        
        success, error_code, message = verify_registration_code(entered_code)
        
        if not success:
            if error_code == "expired":
                clear_verification_session()
                flash(message, "danger")
                return redirect(url_for("auth.register"))
            
            flash(message, "danger")
            return render_template("authorize/verify_email.html")
            
        data = session["registration_data"]
        
        create_user(data)
        
        clear_verification_session()
        
        flash(
            "Your account has been created successfully. You may now log in.",
            "success"
        )

        return redirect(url_for("auth.login"))

    return render_template("authorize/verify_email.html")
    
    
@auth.route("/login", methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        identifier = request.form.get("identifier")
        password = request.form.get("password")

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

        flash("Welcome Back!", "success")

        # ==========================
        # ROLE-BASED REDIRECTION
        # ==========================

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
            return redirect(url_for("mood.mood_entry"))

        # Fallback
        return redirect(
            url_for("lpage.home")
        )

    return render_template(
        "authorize/login.html"
    )
    
    
    
        