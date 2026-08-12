from datetime import datetime
from app.extensions import db
from app.models import ChatRequest
from app.services.mood.mood_services import get_latest_mood
from app.services.chat.conversation_services import create_conversation, get_conversation_by_request

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

def get_latest_request(seeker_id):
    return(
        ChatRequest.query
        .filter_by(seeker_id=seeker_id)
        .order_by(ChatRequest.requested_at.desc())
        .first()
    )

def get_seeker_requests(seeker_id):
    return(
        ChatRequest.query
        .filter_by(seeker_id = seeker_id)
        .order_by(ChatRequest.request_at.desc())
        .all()
    )

def get_seeker_private_chats(seeker_id):
    requests = (
        ChatRequest.query
        .filter_by(seeker_id=seeker_id)
        .order_by(ChatRequest.requested_at.desc())
        .all()
    )

    latest_requests = {}

    for chat_request in requests:
        volunteer_id = chat_request.volunteer_id

        if volunteer_id not in latest_requests:
            latest_requests[volunteer_id] = chat_request

    private_chats = []

    for chat_request in latest_requests.values():
        conversation = None

        if chat_request.request_status == "Accepted":
            conversation = get_conversation_by_request(
                chat_request.request_id
            )
        private_chats.append({
            "request": chat_request,
            "conversation": conversation
        })
    return private_chats

