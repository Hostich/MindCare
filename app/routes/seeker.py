from flask import Blueprint, render_template, request, redirect, session, flash, url_for
from flask_login import login_required, current_user

seeker = Blueprint("seeker", __name__, url_prefix="/seeker")

@seeker.route("/dashboard")
@login_required
def dashboard():
    if current_user.role != "Seeker":
        return redirect(url_for("lpage.home"))
    
    return render_template("seeker/dashboard.html")

