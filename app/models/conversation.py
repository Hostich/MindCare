from app.extensions import db

class Conversation(db.Model):
    __tablename__ = 'conversations'

    conversation_id = db.Column(
        db.Integer, 
        primary_key=True
    )

    request_id = db.Column(
        db.Integer,
        db.ForeignKey('chat_requests.request_id'),
        nullable=True
    )

    session_id = db.Column(
        db.Integer,
        db.ForeignKey('counseling_sessions.session_id'),
        nullable = True
    )

    supporter_id = db.Column(
        db.Integer,
        db.ForeignKey('users.user_id'),
        nullable=  True
    )

    conversation_status = db.Column(
        db.Enum(
            'Active',
            'Closed',
            name='conversation_status_enum'
        ),
        nullable=False,
        default='Active'
    )

    started_at = db.Column(
        db.DateTime,
        server_default=db.func.now(),
        nullable=False
    )

    ended_at = db.Column(
        db.DateTime,
        nullable=True
    )

    request = db.relationship(
        'ChatRequest',
        backref='conversations'
    )

    session = db.relationship(
        "CounselingSession",
        back_populates = 'conversation',
    )

    supporter = db.relationship(
        'User',
        foreign_keys=[supporter_id]
    )