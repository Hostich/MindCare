from app.extensions import db
from app.models import Conversation

def create_conversation(request_id, supporter_id):
    conversation = Conversation(
        request_id=request_id,
        supporter_id = supporter_id,
        conversation_status = "Active"
    )

    db.session.add(conversation)
    db.session.commit()

    return conversation

def get_conversation(conversation_id):
    return Conversation.query.get_or_404(conversation_id)

def get_conversation_by_request(request_id):
    return Conversation.query.filter_by(request_id=request_id).first()
