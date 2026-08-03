from app.extensions import db

class Message(db.Model):
    __tablename__ = 'messages'

    message_id = db.Column(
        db.Integer,
        primary_key=True
    )

    conversation_id = db.Column(
        db.Integer,
        db.ForeignKey('conversations.conversation_id'),
        nullable=False
    )

    sender_id = db.Column(
        db.Integer,
        db.ForeignKey('users.user_id'),
        nullable=False
    )

    message = db.Column(
        db.Text,
        nullable=False
    )

    sent_at = db.Column(
        db.DateTime,
        server_default=db.func.now(),
        nullable=False
    )

    is_read = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )

    conversation = db.Column(
        "Conversation",
        backref="messages"
    )

    sender_id = db.Column(
        "User"
    )