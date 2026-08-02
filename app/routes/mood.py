from flask import Blueprint, render_template, request, redirect, flash, url_for
from flask_login import login_required, current_user

from app.services.mood.mood_services import create_mood_assessment, has_mood_today, get_latest_mood, get_recent_moods, get_mood_statistics

mood = Blueprint("mood", __name__, url_prefix="/mood")

@mood.route("/entry", methods=['GET', 'POST'])
@login_required
def mood_entry():
    if current_user.role != "Seeker":
        return redirect(url_for("lpage.home"))
    if has_mood_today(current_user.user_id):
        flash("You have already recorded your mood for today.", "info")
        return redirect(url_for("seeker.dashboard"))

    if request.method == 'POST':
        data = {
            "mood": request.form.get("mood"),
            "note": request.form.get("note")
        }

        create_mood_assessment(current_user.user_id, data)
        flash("Mood assessment recorded successfully.", "success")
        return redirect(url_for("seeker.dashboard"))

    return render_template("mood/mood_entry.html")

@mood.route("/tracker")
@login_required
def mood_tracker():
    if current_user.role != "Seeker":
        flash("Unauthorized access.", "danger")
        return redirect(url_for("lpage.home"))

    latest_mood = get_latest_mood(current_user.user_id)
    recent_moods = get_recent_moods(current_user.user_id)
    statistics = get_mood_statistics(current_user.user_id)

    return render_template("mood/mood_tracker.html", latest_mood=latest_mood, recent_moods=recent_moods, statistics=statistics)