from datetime import date
from app.extensions import db
from sqlalchemy import func
from app.models.mood_assessment import MoodAssessment

def create_mood_assessment(user_id, data):

    mood = MoodAssessment(
        user_id=user_id,
        mood = data["mood"],
        note=data.get("note")
    )

    db.session.add(mood)
    db.session.commit()

def get_user_moods(user_id):
    return MoodAssessment.query.filter_by(user_id=user_id).order_by(MoodAssessment.recorded_at.desc()).all()

def has_mood_today(user_id):
    today = date.today()
    return MoodAssessment.query.filter_by(user_id=user_id).filter(db.func.date(MoodAssessment.recorded_at) == today).first() is not None

def get_latest_mood(user_id):
    return MoodAssessment.query.filter_by(user_id=user_id).order_by(MoodAssessment.recorded_at.desc()).first()

def get_recent_moods(user_id, limit=5):
    return MoodAssessment.query.filter_by(user_id=user_id).order_by(MoodAssessment.recorded_at.desc()).limit(limit).all()

def get_mood_statistics(user_id):
    total_entries = MoodAssessment.query.filter_by(user_id=user_id).count()
    most_common_mood = db.session.query(MoodAssessment.mood, func.count(MoodAssessment.mood)).filter_by(user_id=user_id).group_by(MoodAssessment.mood).order_by(func.count(MoodAssessment.mood).desc()).first()
    return {
        "total_entries": total_entries,
        "most_common_mood": most_common_mood[0] if most_common_mood else None
    }