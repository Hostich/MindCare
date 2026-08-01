from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.services.chat.chat_request_services import get_peding_requests

volunteer = Blueprint("volunteer", __name__, url_prefix="/volunteer")

@volunteer.route("/dashboard")
@login_required
def dashboard():
    if current_user.role != "Volunteer":
        flash("Unauthorized access.", "danger")
        return redirect(url_for("auth.login"))

    return render_template("volunteer/dashboard.html", community_response_count=0,  active_chat_count=0, referral_count=0,  recent_conversations=[], referrals=[],recent_activities=[])

@volunteer.route("/chat")
@login_required
def chat():
    if current_user.role != "Volunteer":
        flash("Unauthorized access", "danger")
        return redirect(url_for("auth.login"))

    requests = get_peding_requests(current_user.user_id)

    return render_template("volunteer/chat.html",requests=requests)

