from app.extensions import db
from app.models import Referral

def create_referral(conversation_id, volunteer_id, seeker_id, counselor_id, reason, preferred_session_type, volunteer_note=None):
    referral = Referral(
        conversation_id = conversation_id,
        volunteer_id = volunteer_id,
        seeker_id = seeker_id,
        counselor_id = counselor_id,
        preferred_session_type = preferred_session_type,
        reason = reason,
        volunteer_note = volunteer_note,
        referral_status = "Pending"
    )

    db.session.add(referral)
    db.session.commit()

    return referral

def get_referral(referral_id):
    return Referral.query.get(referral_id)

def get_volunteer_referrals(volunteer_id):
    return(
        Referral.query.filter_by(
            volunteer_id = volunteer_id
        ).order_by(
            Referral.referred_at.desc()
        ).all()
    )

def get_counselor_referrals(counselor_id):
    return(
        Referral.query
        .filter_by(
            counselor_id = counselor_id
        ).order_by(
            Referral.referred_at.desc()
        ).all()
    )