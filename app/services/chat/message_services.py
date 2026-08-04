from app.extensions import db
from app.models import Message

def get_messages(conversation_id):
    return(
        Message.query
        .filter_by(conversation_id=conversation_id)
        .order_by(Message.sent_at.asc())
        .all()
    )

def send_message(conversation_id, sender_id, content):
    message = Message(
        conversation_id = conversation_id,
        sender_id = sender_id,
        message=content
    )

    db.session.add(message)
    db.session.commit()

    return message



