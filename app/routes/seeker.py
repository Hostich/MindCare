from flask import Blueprint, render_template, request, redirect, session, flash, url_for
from flask_login import login_required, current_user
from app.services.chat.conversation_services import get_conversation
from app.services.chat.message_services import get_messages, send_message
from app.services.chat.chat_request_services import get_latest_request
from app.services.chat.conversation_services import get_conversation_by_request, get_latest_conversation

seeker = Blueprint("seeker", __name__, url_prefix="/seeker")

@seeker.route("/dashboard")
@login_required
def dashboard():
    if current_user.role != "Seeker":
        return redirect(url_for("lpage.home"))
    
    return render_template("seeker/dashboard.html")

@seeker.route("/chat")
@login_required
def chat():
    if current_user.role != "Seeker":
        return redirect(url_for("lpage.home"))

    conversation = get_latest_conversation(current_user.user_id)

    return render_template("seeker/chat.html", conversation = conversation)

@seeker.route("/conversation/<int:conversation_id>",methods=['GET','POST'])
@login_required
def conversation(conversation_id):
    if current_user.role != "Seeker":
        flash("Unauthorized access.", "danger")
        return redirect(url_for("auth.login"))

    conversation = get_conversation(conversation_id)

    if conversation.request.seeker_id != current_user.user_id:
        flash("Unauthorized access.", "danger")
        return redirect(url_for("seeker.chat"))

    if request.method == 'POST':
        content = request.form.get("message")

        if content:
            send_message(
                conversation_id,
                current_user.user_id,
                content
            )

            return redirect(url_for("seeker.conversation", conversation_id=conversation_id))

    messages = get_messages(conversation_id)

    return render_template("seeker/conversation.html", conversation=conversation, messages = messages, other_user_label = "Volunteer")
