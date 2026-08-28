from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.extensions import socketio
from app.models import Conversation, User
from app.services.chat.chat_request_services import get_peding_requests, accept_chat_request, reject_chat_request, get_volunteer_private_chats
from app.services.chat.conversation_services import get_conversation, end_conversation
from app.services.chat.message_services import get_messages, send_message
from app.services.referral.referral_services import create_referral

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

    counselors = (
        User.query
        .filter_by(role = "Counselor")
        .all()
    )

    conversation = None
    messages = []

    conversation_id = request.args.get("conversation_id", type=int)

    if conversation_id:

        conversation = get_conversation(
            conversation_id
        )
    else:

        conversation = (
            Conversation.query
            .filter_by(
                supporter_id = current_user.user_id,
                conversation_status="Active"
            ).first()
        )

    if conversation:

        messages = get_messages(
            conversation.conversation_id
        )

    return render_template("volunteer/chat.html",requests=requests, private_chats=private_chats, conversation=conversation, messages=messages, counselors=counselors)

@volunteer.route("chat/accept/<int:request_id>")
@login_required
def accept_request(request_id):
    print("ACCEPT REQUEST ROUTE CALLED:", request_id)
    if current_user.role != "Volunteer":
        flash("Unauthorized access.", "danger")
        return redirect(url_for("auth.login"))

    conversation, error = accept_chat_request(
        request_id,
        current_user.user_id
    )

    if error:
        flash(error, "warning")
        return redirect(url_for("volunteer.chat"))

    flash("Chat request accepted.", "success")

    return redirect(url_for("volunteer.chat",conversation_id=conversation.conversation_id))
    
@volunteer.route("/chat/reject/<int:request_id>", methods=['POST'])
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

    counselors = (
        User.query
        .filter_by(role="Counselor")
        .all()
    )

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

    return render_template("volunteer/conversation.html", conversation=conversation, messages = messages, counselors = counselors, other_user_label = "Anonymous Seeker")


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

@volunteer.route("/conversation/<int:conversation_id>/refer", methods=['POST'])
@login_required
def refer_seeker(conversation_id):
    if current_user.role != "Volunteer":
        flash("Unauthorized access.", "danger")
        return redirect(url_for("auth.login"))

    conversation = get_conversation(conversation_id)

    if conversation.supporter_id != current_user.user_id:
        flash("Unauthorized access.", "danger")
        return redirect(url_for("volunteer.chat"))

    if conversation.conversation_status != "Active":
        flash("This conversation has already ended.", "warning")
        return redirect(url_for("volunteer.chat", conversation_id = conversation_id))

    counselor_id = request.form.get("counselor_id", type=int)
    reason = request.form.get("reason")
    preferred_session_type = request.form.get("preferred_session_type")
    volunteer_note = request.form.get("volunteer_note")

    counselor = (
        User.query
        .filter_by(
            user_id = counselor_id,
            role = "Counselor"
            )
            .first()
        )

    if not counselor:
        flash("Invalid counselor selected.", "danger")
        return redirect(url_for("volunteer.chat", conversation_id = conversation_id))
    
    if not reason:
        flash("Referral reason is required.", "warning")
        return redirect(url_for("volunteer.chat", conversation_id = conversation_id))

    if preferred_session_type not in ["Chat","Video"]:
        flash("Invalid preferred session type.", "warning")
        return redirect(url_for("volunteer.chat", conversation_id = conversation_id))

    seeker_id = conversation.request.seeker_id

    referral = create_referral(
        conversation_id = conversation_id,
        volunteer_id = current_user.user_id,
        seeker_id = seeker_id,
        counselor_id = counselor_id,
        reason = reason,
        preferred_session_type = preferred_session_type,
        volunteer_note = volunteer_note or None
    )

    flash("referral sent Successfully.", "success")

    return redirect(url_for("volunteer.chat", conversation_id = conversation_id))