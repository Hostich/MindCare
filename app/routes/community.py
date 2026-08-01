from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.services.community.post_services import create_post, get_all_posts
from app.services.community.comment_services import create_comment, get_comment_by_post

community = Blueprint("community", __name__, url_prefix="/community")

@community.route("/", methods=['GET','POST'])
@login_required
def community_feed():

    if request.method == 'POST':
        data = { 
            "content": request.form.get("content")
        }

        create_post(current_user.user_id, data)

        flash("Your post has been published", "success")

        return redirect(url_for("community.community_feed"))

    posts = get_all_posts()

    for post in posts:
        post.comments = get_comment_by_post(post.post_id)
    
    return render_template("community/community.html",posts=posts)


@community.route("/comment/<int:post_id>", methods=['POST'])
@login_required
def create_comment_route(post_id):

    data = {
        "content" : request.form.get("content")
    }

    create_comment(
        post_id,
        current_user.user_id,
        data
    )

    flash("Comment added", "success")

    return redirect(url_for("community.community_feed"))
