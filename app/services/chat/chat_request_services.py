from datetime import datetime
from app.extensions import db
from app.models import ChatRequest
from app.services.mood.mood_services import get_latest_mood
from app.services.chat.conversation_services import create_conversation

def create_chat_request(seeker_id, volunteer_id):
    request = ChatRequest(seeker_id = seeker_id, volunteer_id = volunteer_id)

    db.session.add(request)
    db.session.commit()

    return request

def has_pending_request(seeker_id, volunteer_id):
    return ChatRequest.query.filter_by(seeker_id = seeker_id, volunteer_id = volunteer_id, request_status = "Pending").first()

def get_peding_requests(volunteer_id):
    requests = ChatRequest.query.filter_by(volunteer_id = volunteer_id, request_status = "Pending").all()
    for request in requests:
        request.seeker_mood = get_latest_mood(request.seeker_id)
    return requests

def accept_chat_request(request_id, supporter_id):
    request = ChatRequest.query.get_or_404(request_id)

    request.request_status = "Accepted"
    request.responded_at = datetime.utcnow()

    db.session.commit()

    conversation = create_conversation(
        request.request_id,
        supporter_id
    )

    return conversation

def reject_chat_request(request_id):
    request = ChatRequest.query.get_or_404(request_id)

    request.request_status = "Rejected"
    request.responded_at = datetime.utcnow()

    db.session.commit()

    

