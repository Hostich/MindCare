from datetime import datetime
from app.extensions import db
from app.models import Conversation, ChatRequest

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

def end_conversation(conversation_id):
    conversation = Conversation.query.get(conversation_id)

    if not conversation:
        return False

    conversation.conversation_status = "Closed"
    conversation.ended_at = datetime.utcnow()

    db.session.commit()

    return True

def get_latest_conversation(seeker_id):
    return(
        Conversation.query
        .join(ChatRequest)
        .filter(ChatRequest.seeker_id == seeker_id)
        .order_by(Conversation.started_at.desc())
        .first()
    )