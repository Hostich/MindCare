from app.extensions import db

class ChatRequest(db.Model):
    __tablename__ = "chat_requests"

    request_id = db.Column(
        db.Integer,
        primary_key = True
    )

    seeker_id = db.Column(
        db.Integer,
        db.ForeignKey("users.user_id"),
        nullable = False
    )

    volunteer_id = db.Column(
        db.Integer,
        db.ForeignKey("users.user_id"),
        nullable = False
    )

    request_status = db.Column(
        db.Enum(
            "Pending",
            "Accepted",
            "Rejected",
            name = "chat_request_status_enum"
        ),
        nullable = False,
        default = "Pending"
    )

    requested_at = db.Column(
        db.DateTime,
        server_default= db.func.now(),
        nullable = False
    )

    responded_at = db.Column(
        db.DateTime,
        nullable = True
    )

    seeker = db.relationship(
        "User",
        foreign_keys=[seeker_id]
    )

    volunteer = db.relationship(
        "User",
        foreign_keys= [volunteer_id]
    )

