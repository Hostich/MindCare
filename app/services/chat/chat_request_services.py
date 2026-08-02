from app.extensions import db
from app.models import ChatRequest
from app.services.mood.mood_services import get_latest_mood

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
