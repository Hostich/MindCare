from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

counselor = Blueprint("counselor", __name__, url_prefix="/counselor")

@counselor.route("/dashboard")
@login_required
def dashboard():
    if current_user.role != "Counselor":
        return redirect(url_for("lpage.home"))
    
    return render_template("counselor/dashboard.html")