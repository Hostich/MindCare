from app.extensions import db

class Referral(db.Model):
    __tablename__ = "referrals"

    referral_id = db.Column(
        db.Integer,
        primary_key = True,
        autoincrement = True
    )

    conversation_id = db.Column(
        db.Integer,
        db.ForeignKey("conversations.conversation_id"),
        nullable = False
    )

    volunteer_id = db.Column(
        db.Integer,
        db.ForeignKey("users.user_id"),
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

    preferred_session_type = db.Column(
        db.Enum(
            "Chat",
            "Video",
            name = "preferred_session_type_enum"
        ),
        nullable = False
    )

    reason = db.Column(
        db.Text,
        nullable = False
    )

    volunteer_note = db.Column(
        db.Text,
        nullable = True
    )

    referral_status = db.Column(
        db.Enum(
            "Pending",
            "Accepted",
            "Rejected",
            "Completed",
            name = "referral_status_enum"
        ),
        nullable = False,
        default = "Pending"
    )

    referred_at = db.Column(
        db.DateTime,
        server_default = db.func.now(),
        nullable = False
    )

    responded_at = db.Column(
        db.DateTime,
        nullable = True
    )


    conversation = db.relationship(
        "Conversation",
        foreign_keys = [conversation_id]
    )

    volunteer = db.relationship(
        "User",
        foreign_keys = [volunteer_id]
    )

    seeker = db.relationship(
        "User",
        foreign_keys = [seeker_id]
    )

    counselor = db.relationship(
        "User",
        foreign_keys = [counselor_id]
    )