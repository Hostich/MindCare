from flask import Blueprint, render_template, request, redirect, flash, url_for
from flask_login import login_required, current_user
from app.models import Conversation, ChatRequest
from app.services.chat.conversation_services import get_conversation
from app.services.chat.message_services import get_messages, send_message
from app.services.chat.chat_request_services import get_seeker_private_chats
from app.services.chat.conversation_services import volunteer_is_busy
from app.services.volunteer.volunteer_services import get_all_volunteers
from app.services.notification.notification_services import get_user_notification

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

    volunteers  = get_all_volunteers()

    for volunteer in volunteers:
        volunteer.is_busy = volunteer_is_busy(
            volunteer.user_id
        )
    notifications = get_user_notification(
        current_user.user_id
    )
    private_chats = get_seeker_private_chats(
        current_user.user_id
    )

    conversation = None
    messages = []

    conversation_id = request.args.get("conversation_id",type=int)

    if conversation_id:
        conversation =  get_conversation(
            conversation_id
        )
        
        if conversation:
            messages = get_messages(
                conversation.conversation_id
            )

    return render_template("seeker/chat.html", volunteers = volunteers, private_chats = private_chats, conversation = conversation, messages = messages, notifications=notifications)

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
