from flask import Blueprint, redirect, url_for
from flask_login import login_required, current_user
from app.services.notification.notification_services import mark_notification_as_read
from app.models import Notification
notification = Blueprint("notification", __name__, url_prefix='/notification')


@notification.route("/read/<int:notification_id>")
@login_required
def read_notification(notification_id):
    mark_notification_as_read(
        notification_id,
        current_user.user_id
    )

    return "Notification marked as read"


@notification.route("/chat/<int:notification_id>")
@login_required
def notification_chat(notification_id):
    notification = (
        Notification.query
        .filter_by(
            notification_id = notification_id,
            user_id = current_user.user_id
        )
        .first()
    )

    if not notification:
        return "Notification not Found",404

    if notification.notification_type != "ChatRequestAccepted":
        return "Invalid notification type", 404

    if not notification.conversation:
        return "Conversation not found",404

    if notification.conversation.conversation_status != "Active":
        return "Conversation has already ended",404

    mark_notification_as_read(
        notification.notification_id,
        current_user.user_id
    )

    return redirect(url_for("seeker.chat",conversation_id = notification.conversation_id))
