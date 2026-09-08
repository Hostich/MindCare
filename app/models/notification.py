from app.extensions import db

class Notification(db.Model):
    __tablename__ = "notifications"

    notification_id = db.Column(
        db.Integer,
        primary_key = True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.user_id"),
        nullable = False
    )

    request_id = db.Column(
        db.Integer,
        db.ForeignKey("chat_requests.request_id"),
        nullable=True
    )
    conversation_id = db.Column(
        db.Integer,
        db.ForeignKey("conversations.conversation_id"),
        nullable = True
    )

    session_id = db.Column(
        db.Integer,
        db.ForeignKey("counseling_sessions.session_id"),
        nullable = True
    )

    title = db.Column(
        db.String(150),
        nullable = False
    )

    message = db.Column(
        db.Text,
        nullable = False
    )

    notification_type = db.Column(
        db.Enum(
            "ChatRequestCreated",
            "ChatRequestAccepted",
            "CounselingSessionCreated",
            name = "notification_type_enum"
        ),
        nullable = False
    )

    is_read = db.Column(
        db.Boolean,
        nullable = False,
        default = False
    )

    created_at = db.Column(
        db.DateTime,
        server_default= db.func.now(),
        nullable = False
    )

    user = db.relationship(
        "User",
        foreign_keys = [user_id]
    )

    conversation = db.relationship(
        "Conversation",
        foreign_keys = [conversation_id]
    )

    session = db.relationship(
        "CounselingSession",
        foreign_keys = [session_id]
    )
    request = db.relationship(
        "ChatRequest",
        foreign_keys=[request_id]
    )