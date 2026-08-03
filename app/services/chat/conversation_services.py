from app.extensions import db
from app.models import Conversation

def create_conversation(reques_id, supporter_id):
    conversation = Conversation(
        reques_id=reques_id,
        supporter_id = supporter_id,
        conversation_status = "Active"
    )

    db.session.add(conversation)
    db.session.commit()

    return conversation