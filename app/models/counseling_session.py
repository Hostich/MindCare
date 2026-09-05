from app.extensions import db

class CounselingSession(db.Model):
    __tablename__ = "counseling_sessions"

    session_id = db.Column(
        db.Integer,
        primary_key = True,
        autoincrement = True
    )

    referral_id = db.Column(
        db.Integer,
        db.ForeignKey("referrals.referral_id"),
        nullable = False
    )

    seeker_id = db.Column(
        db.Integer,
        db.ForeignKey("users.user_id"),
        nullable = False
    )

    counselor_id = db.Column(
        db.Integer,
        db.ForeignKey("users.user_id"),
        nullable = False
    )

    session_type = db.Column(
        db.Enum(
            "Chat",
            "Video",
            name = "session_type_enum"
        ),
        nullable = False
    )

    started_at = db.Column(
        db.DateTime,
        nullable = True,
    )

    ended_at = db.Column(
        db.DateTime,
        nullable = True
    )

    session_status = db.Column(
        db.Enum(
            "Pending",
            "Active",
            "Completed",
            "Cancelled",
            name = "session_status_enum"
        ),
        nullable = False,
        default = "Pending"
    )

    referral = db.relationship(
        "Referral",
        foreign_keys = [referral_id]
    )

    seeker = db.relationship(
        "User",
        foreign_keys = [seeker_id]
    )

    counselor = db.relationship(
        "User",
        foreign_keys = [counselor_id]
    )

    summary = db.relationship(
        "SessionSummary",
        back_populates = "session",
        uselist = False
    )
    conversation = db.relationship(
        "Conversation",
        back_populates = "session",
        uselist = False
    )
