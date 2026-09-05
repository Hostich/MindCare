from app.extensions import db

class SessionSummary(db.Model):
    __tablename__ = "session_summaries"

    session_id = db.Column(
        db.Integer,
        db.ForeignKey("counseling_sessions.session_id"),
        primary_key = True,
        nullable = False
    )

    outcome = db.Column(
        db.Text,
        nullable = False
    )

    counselor_note = db.Column(
        db.Text,
        nullable = True
    )

    completed_at = db.Column(
        db.DateTime,
        nullable = False,
        server_default = db.func.now()
    )

    session = db.relationship(
        "CounselingSession",
        back_populates = "summary"
    )

