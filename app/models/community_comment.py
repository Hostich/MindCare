from app.extensions import db

class CommunityComment(db.Model):
    __tablename__="community_comment"

    comment_id = db.Column(
        db.Integer,
        primary_key = True
    )

    post_id = db.Column(
        db.Integer,
        db.ForeignKey("community_post.post_id"),
        nullable = False
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.user_id"),
        nullable = False
    )

    content = db.Column(
        db.Text,
        nullable = False
    )

    status = db.Column(
        db.Enum(
            "Active",
            "Remove",
            name = "community_comment_status_enum"
        ),
        nullable = False,
        default = "Active"
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now(),
        nullable = False
    )

    updated_at = db.Column(
        db.DateTime,
        server_default = db.func.now(),
        onupdate = db.func.now()
    )

    user = db.relationship(
        "User",
        backref="community_comments"
    )