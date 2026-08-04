from flask import Blueprint, render_template, request, redirect, session, flash, url_for
from flask_login import login_required, current_user
from app.services.chat.conversation_services import get_conversation
from app.services.chat.message_services import get_messages, send_message
from app.services.chat.chat_request_services import get_latest_request
from app.services.chat.conversation_services import get_conversation_by_request

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

    chat_request = get_latest_request(current_user.user_id)

    conversation = None

    if chat_request and chat_request.request_status == "Accepted":
        conversation = get_conversation_by_request(chat_request.request_id)
    
    return render_template("seeker/chat.html", chat_request=chat_request, conversation = conversation)

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

    return render_template("seeker/conversation.html", conversation=conversation, messages = messages)
