from app.extensions import db
from app.models import CommunityComment

def create_comment(post_id, user_id, data):

    comment = CommunityComment(post_id = post_id, user_id=user_id, content=data['content'])

    db.session.add(comment)
    db.session.commit()


    return comment

def get_comment_by_post(post_id):

    return(CommunityComment.query.filter_by(post_id=post_id, status="Active").order_by(CommunityComment.created_at.asc()).all())