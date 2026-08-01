from app.extensions import db

class MoodAssessment(db.Model):
    __tablename__ = "mood_assessments"

    mood_id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.user_id"),
        nullable=False
    )
    mood = db.Column(
        db.Enum(
            "Happy",
            "Calm",
            "Neutral",
            "Anxious",
            "Sad",
            "Angry",
            name="mood_enum"
        ),
        nullable=False
    )

    note = db.Column(
        db.Text,
        nullable = True
    )

    recorded_at = db.Column(
        db.DateTime,
        server_default=db.func.now(),
        nullable = False
    )
    updated_at = db.Column(
        db.DateTime,
        server_default=db.func.now(),
        onupdate=db.func.now()
    )
    
    user = db.relationship(
        "User",
        backref="mood_assessments"
    )