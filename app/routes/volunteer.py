from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.services.chat.chat_request_services import get_peding_requests, accept_chat_request, reject_chat_request


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

@volunteer.route("chat/accept/<int:request_id>")
@login_required
def accept_request(request_id):
    if current_user.role != "Volunteer":
        flash("Unauthorized access.", "danger")
        return redirect(url_for("auth.login"))

    conversation = accept_chat_request(
        request_id,
        current_user.user_id
    )

    flash("Chat request accepted.", "success")

    return redirect(url_for("volunteer.conversation",conversation_id=conversation.conversation_id))
    
@volunteer.route("/chat/reject/<int:request_id>")
@login_required
def reject_request(request_id):
    if current_user.role != "Volunteer":
        flash("Unauthorized access.", "danger")
        return redirect(url_for("auth.login"))

    reject_chat_request(request_id)

    flash("Chat request rejected.", "info")

    return redirect(url_for("volunteer.chat"))
