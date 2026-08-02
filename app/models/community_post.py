from app.extensions import db

class CommunityPost(db.Model):
    __tablename__ = "community_post"

    post_id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.user_id"),
        nullable = False
    )

    mood_id = db.Column(
        db.Integer,
        db.ForeignKey("mood_assessments.mood_id"),
        nullable= False
    )

    content = db.Column(
        db.Text,
        nullable=False
    )

    is_anonymous = db.Column(
        db.Boolean,
        nullable =  False,
        default = True
    )

    status = db.Column(
        db.Enum(
            "Active",
            "Remove",
            name = "community_post_status_enum"
        ),
        nullable=False,
        default="Active"
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now(),
        nullable=False
    )

    updated_at = db.Column(
        db.DateTime,
        server_default=db.func.now(),
        onupdate=db.func.now()
    )

    mood = db.relationship(
        "MoodAssessment",
        backref="community_post"
    )
