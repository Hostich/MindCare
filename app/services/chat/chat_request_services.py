from app.extensions import db
from app.models import ChatRequest

def create_chat_request(seeker_id, volunteer_id):
    request = ChatRequest(seeker_id = seeker_id, volunteer_id = volunteer_id)

    db.session.add(request)
    db.session.commit()

    return request

def has_pending_request(seeker_id, volunteer_id):
    return ChatRequest.query.filter_by(seeker_id = seeker_id, volunteer_id = volunteer_id, request_status = "Pending").first()

def get_peding_requests(volunteer_id):
    return(ChatRequest.query.filter_by(volunteer_id = volunteer_id, request_status = "Pending").order_by(ChatRequest.requested_at.desc()).all())

