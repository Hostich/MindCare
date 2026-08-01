from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.services.profile.profile_services import update_profile

profile = Blueprint("profile", __name__, url_prefix="/profile")

@profile.route("/")
@login_required
def view_profile():
    return render_template("profile/profile.html", user=current_user)

@profile.route("/edit", methods=['GET','POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        data = {
            "first_name": request.form.get("first_name"),
            "last_name": request.form.get("last_name"),
            "phone_number": request.form.get("phone_number"),
            "gender": request.form.get("gender")
        }

        update_profile(current_user, data)

        flash("Profile updated successfully.", "success")

        return redirect(url_for("profile.view_profile"))
    
    return render_template("profile/edit_profile.html", user=current_user)

