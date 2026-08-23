from flask import Blueprint, request, redirect, url_for, flash
from flask_login import login_required, current_user

from app.services.chat.chat_request_services import create_chat_request, has_pending_request, get_active_conversation

chat_request = Blueprint("chat_request", __name__, url_prefix="/chat")

@chat_request.route("/send", methods=['POST'])
@login_required
def send_request():

    volunteer_id = request.form.get("volunteer_id")
    source = request.form.get("source")

    active_conversation = get_active_conversation(current_user.user_id, volunteer_id)

    if active_conversation:
        flash("You already have an active conversation with this volunteer!", "warning")
        if source == "chat":
            return redirect(url_for("seeker.chat", conversation_id=active_conversation.conversation_id))
        return redirect(url_for("community.community_feed"))

    if has_pending_request(current_user.user_id, volunteer_id):
        flash("You already have a pending chat request with this volunteer!", "warning")
        if source == "chat":
            return redirect(url_for("seeker.chat"))
        return redirect(url_for("community.community_feed"))
    
    create_chat_request(current_user.user_id, volunteer_id)

    flash("Chat request sent successfully", "success")
    if source == "chat":
        return redirect(url_for("seeker.chat"))

    return redirect(url_for("community.community_feed"))
