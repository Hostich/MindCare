from app.extensions import db
from app.models import CommunityPost

def create_post(user_id, data):

    post = CommunityPost(
        user_id = user_id,
        content=data["content"]
    )

    db.session.add(post)
    db.session.commit()

    return post

def get_all_posts():
    return CommunityPost.query.filter_by(status="Active").order_by(CommunityPost.created_at.desc()).all()