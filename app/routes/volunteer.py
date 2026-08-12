from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.extensions import socketio
from app.services.chat.chat_request_services import get_peding_requests, accept_chat_request, reject_chat_request, get_volunteer_private_chats
from app.services.chat.conversation_services import get_conversation, end_conversation
from app.services.chat.message_services import get_messages, send_message

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

    private_chats = get_volunteer_private_chats(
        current_user.user_id
    )

    conversation = None
    messages = []

    conversation_id = request.args.get("conversation_id", type=int)

    if conversation_id:

        conversation = get_conversation(
            conversation_id
        )

        if conversation:

            messages = get_messages(
                conversation_id
            )

    return render_template("volunteer/chat.html",requests=requests, private_chats=private_chats, conversation=conversation, messages=messages)

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

    return redirect(url_for("volunteer.chat",conversation_id=conversation.conversation_id))
    
@volunteer.route("/chat/reject/<int:request_id>")
@login_required
def reject_request(request_id):
    if current_user.role != "Volunteer":
        flash("Unauthorized access.", "danger")
        return redirect(url_for("auth.login"))

    reject_chat_request(request_id)

    flash("Chat request rejected.", "info")

    return redirect(url_for("volunteer.chat"))


@volunteer.route("/conversation/<int:conversation_id>", methods=['GET','POST'])
@login_required
def conversation(conversation_id):
    if current_user.role != "Volunteer":
        flash("Unauthorized access.", "danger")
        return redirect(url_for("auth.login"))

    conversation = get_conversation(conversation_id)

    #preventing volunteer to connect to other conversation
    if conversation.supporter_id != current_user.user_id:
        flash("Unauthorized access", "danger")
        return redirect(url_for("volunteer.chat"))

    messages = get_messages(conversation_id)

    if request.method == 'POST':
        content = request.form.get("message")

        if content:
            send_message(
                conversation_id,
                current_user.user_id,
                content
            )
            return redirect(url_for("volunteer.conversation",conversation_id=conversation_id))

    return render_template("volunteer/conversation.html", conversation=conversation, messages = messages, other_user_label = "Anonymous Seeker")


@volunteer.route("conversation/<int:conversation_id>/end", methods=['POST'])
@login_required
def end_conversation_route(conversation_id):

    if current_user.role != "Volunteer":
        return redirect(url_for("auth.login"))

    success = end_conversation(conversation_id)

    if success:

        room = f"conversation_{conversation_id}"

        socketio.emit(
            "conversation_ended",
            {
                "conversation_id": conversation_id
            },
            to=room
        )
        flash("Conversation ended successfully", "success")
    else:
        flash("Conversation not found.", "danger")
    return redirect(url_for("volunteer.chat"))



