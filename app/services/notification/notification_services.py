from app.extensions import db, socketio
from app.models.notification import Notification



def create_notification(
    user_id,
    conversation_id,
    title,
    message,
    notification_type
):
    notification = Notification(
        user_id = user_id,
        conversation_id = conversation_id,
        title = title,
        message = message,
        notification_type = notification_type
    )

    db.session.add(notification)
    db.session.commit()
    print(
        "EMITTING NOTIFICATION TO:",
        f"user_{user_id}"
    )
    socketio.emit(
        "new_notification",
        {
            "notification_id" : notification.notification_id,
            "title" : notification.title,
            "message" : notification.message,
            "notification_type" : notification.notification_type,
            "conversation_id" : notification.conversation_id
        },
        to = f"user_{user_id}"
    )

    return notification


def get_user_notification(user_id):
    return(
        Notification.query
        .filter_by(user_id = user_id)
        .order_by(Notification.created_at.desc())
        .all()
    )


def mark_notification_as_read(notification_id, user_id):
    notification = (
        Notification.query
        .filter_by(
            notification_id = notification_id,
            user_id = user_id
        )
        .first()
    )

    if not notification:
        return False

    notification.is_read = True

    db.session.commit()

    return True